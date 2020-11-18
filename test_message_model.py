"""User model tests."""

# run these tests like:
#
#    python -m unittest test_message_model.py


from app import app
import os
from unittest import TestCase
from datetime import datetime

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# Now we can import app


# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class MessageModelTestCase(TestCase):
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

        m1 = Message(
            text="testmessage1",
            user_id = uid1
        )
        mid1 = 1111
        m1.id = mid1

        m2 = Message(
            text="testmessage2",
            user_id = uid1
        )
        mid2 = 1112
        m2.id = mid2

        db.session.add(m1)
        db.session.add(m2)
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

    def test_message_model(self):
        """Does basic model work?"""

        m = Message(
            text = "testmessage3",
            user_id = self.uid1
        )
        mid = 1113
        m.id = mid
        m_time = datetime.utcnow()
        m.timestamp = m_time

        db.session.add(m)
        db.session.commit()

        # User test1 should have three message
        self.assertEqual(len(self.u1.messages), 3)
        # User test2 should have no messages
        self.assertEqual(len(self.u2.messages), 0)
        # Repr method should work
        self.assertEqual(
            m.__repr__(), 
            f"Message Message_id {mid} User_id {self.uid1} Time {m_time}")

    def test_message_model_throws_exception(self):
        """Does Message model fail if any of the validations (e.g. uniqueness, non-nullable fields)"""

        # Message without user_id
        m = Message(
            text="testmessageFail",
        )
        m_time = datetime.utcnow()
        m.timestamp = m_time

        db.session.add(m)

        # Should raise exception if message fails validation
        self.assertRaises(TypeError, db.session.add(m))
