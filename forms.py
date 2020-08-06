from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional


class MessageForm(FlaskForm):
    """Form for adding/editing messages."""

    text = TextAreaField('text', validators=[DataRequired()])


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class UserEditForm(UserAddForm):
    """Form for editing users.
    TODO: Should we refactor to use UserAddForm to show this instead of using a separate class
    """

    bio = TextAreaField('(Optional) Bio', validators=[Optional()])
    header_image_url = StringField('(Optional) Header Image URL')
    location = StringField('(Optional) Location', validators=[Optional()])

# CODEREVIEW: in larger codebases, a baseUserForm could serve as common; Code should be truthful