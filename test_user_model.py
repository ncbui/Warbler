"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test model for users."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        u1 = User.signup("test1", "email1@email.com", "password", None)
        uid1 = 1111
        u1.id = uid1

        u2 = User.signup("test2", "email2@email.com", "password", None)
        uid2 = 2222
        u2.id = uid2

        db.session.commit()

        u1 = User.query.get(uid1)
        u2 = User.query.get(uid2)

        self.u1 = u1
        self.uid1 = uid1

        self.u2 = u2
        self.uid2 = uid2

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

        # Repr method should work
        self.assertEqual(
            u.__repr__(), 
            "<User #1: testuser, test@test.com>"
            )

    def test_is_following(self):
        """Does is_following method work?"""
        self.u1.following.append(self.u2)
        db.session.commit()

        # u1 should be following u2
        self.assertTrue(self.u1.is_following(self.u2))
        # u2 should not be following u1
        self.assertFalse(self.u2.is_following(self.u1))

    def test_is_followed_by(self):
        """Does is_followed_by work?"""
        self.u1.following.append(self.u2)
        db.session.commit()

        # u2 should be followed by u1
        self.assertTrue(self.u2.is_followed_by(self.u1))
        # u1 should not be followed by u2
        self.assertFalse(self.u1.is_followed_by(self.u2))

    def test_user_sign_up(self):
        """Does User.signup work?"""

        u3 = User.signup("u3", "u3@email.com", "password", None)
        uid3 = 3333
        u3.id = uid3

        # Should successfilly create a new user given valid credentials?
        self.assertTrue(u3)

        # Should fail if any of the validations (e.g. uniqueness, non-nullable fields)
        with self.assertRaises(ValueError):
            User.signup("testFail", None, None, None)
        self.assertRaises(
            ValueError, lambda: User.signup("testFail", None, None, None))


    def test_user_authenticate(self):
        """Does User.authenticate method work?"""

        # Should return true if user credentials are valid
        self.assertTrue(User.authenticate("test1", "password"))
        # Should return false if user password is invalid
        self.assertFalse(User.authenticate("test1", "passwordFail"))
        # Should return false if username is invalid valid
        self.assertFalse(User.authenticate("testFail", "password"))
