"""SQLAlchemy models for Warbler."""

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class Follows(db.Model):
    """Connection of a follower <-> followed_user."""

    __tablename__ = 'follows'

    # two-component primary key! 
    # other person
    user_being_followed_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade"),
        primary_key=True,
    )

    # me
    user_following_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade"),
        primary_key=True,
    )
    # ondelete="cascade"; if a user's record is deleted from User table, delete the user's record in Follows table

class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    image_url = db.Column(
        db.Text,
        default="/static/images/default-pic.png",
    )

    header_image_url = db.Column(
        db.Text,
        default="/static/images/warbler-hero.jpg"
    )

    bio = db.Column(
        db.Text,
    )

    location = db.Column(
        db.Text,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    # calling user.messages() will return user's message ordered by timestamp in descending order
    # added a backref to messages table
    messages = db.relationship('Message', 
                                order_by='Message.timestamp.desc()')

    # user.followers returns a list of user instances of users that follow this user
    # primaryjoin & secondaryjoin to connect two-component primary key to access the user table twice
    followers = db.relationship(
        "User",
        secondary="follows",
        primaryjoin=(Follows.user_being_followed_id == id),
        secondaryjoin=(Follows.user_following_id == id)
    )

    # user.following returns a list of user instances that this user is following
    following = db.relationship(
        "User",
        secondary="follows",
        primaryjoin=(Follows.user_following_id == id),
        secondaryjoin=(Follows.user_being_followed_id == id)
    )

    #TODO: Complete this relationship   
    liked_messages = db.relationship(
        "Message", 
        secondary="likes", 
        backref="users"
       ) #instance user -- its id


    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    # user.is_followed_by(other_user) return False if not followed by; returns True
    def is_followed_by(self, other_user):
        """Is this user followed by `other_user`?"""

        found_user_list = [user for user in self.followers if user == other_user]
        return len(found_user_list) == 1 
    
    # user.is_following returns T/F
    def is_following(self, other_user):
        """Is this user following `other_user`?""" 

        found_user_list = [user for user in self.following if user == other_user]
        return len(found_user_list) == 1
    
    # check if a user has liked a message with user.is_message_liked(...)
    def is_message_liked(self, message):
        """Is this message `liked` by user?"""

        found_message_list = [m for m in self.liked_messages if m == message]
        return len(found_message_list) == 1
    # TODO: current list comprehension goes over all messages. Python `any()` (equivalent to JS' some())
    
    @classmethod
    def signup(cls, username, email, password, image_url):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            image_url=image_url,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False



class Message(db.Model):
    """An individual message ("warble")."""

    __tablename__ = 'messages'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    text = db.Column(
        db.String(140),
        nullable=False,
    )

    timestamp = db.Column(
        db.DateTime, 
        # TODO: what is the timezone for this? If our default is stored in UTC, should we programatically convert all date times to UTC?
        nullable=False,
        default=datetime.utcnow(),
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )

    user = db.relationship('User')

    def __repr__(self):
        """ Information about message instance."""

        return f"Message Message_id {self.id} User_id {self.user_id} Time {self.timestamp}"

class Like(db.Model):
    """ Connection of a message <-> user who liked the message. """
    # TODO: we haven't prevented the same user from liking the same message. 
    #  Could have a two-component primary key OR unique constraint on user & msg
    __tablename__ = "likes"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    msg_id = db.Column(
        db.Integer,
        db.ForeignKey('messages.id',
        ondelete="cascade"),
        nullable=False)

    user_liked_id =  db.Column(
        db.Integer,
        db.ForeignKey('users.id',
        ondelete="cascade"),
        nullable=False)

    def __repr__(self):
        """ Information about message Liked by user."""

        return f"Like Message_id {self.msg_id} User_id {self.user_liked_id}"


    
def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
