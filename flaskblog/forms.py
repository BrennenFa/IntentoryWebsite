from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError
from flaskblog.models import User

class RegistrationForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
  password = PasswordField('Password', validators=[DataRequired()])
  submit = SubmitField('Sign Up')
  
  
  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
      raise ValidationError("Pick a different username")

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  submit = SubmitField('Login')


class ItemForm(FlaskForm):
  content = StringField('Content', validators=[DataRequired()])
  number = IntegerField('Number', validators = [DataRequired()])
  submit = SubmitField('Submit Item')
