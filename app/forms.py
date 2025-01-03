from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, PasswordField, IntegerField, BooleanField, SubmitField, FileField
from wtforms.validators import NumberRange, Length, DataRequired, ValidationError, Email, EqualTo
from wtforms.fields import DateField  # Use DateField instead of DateTimeField
from app.models import User
#7
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Create Account')
#19
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
#24
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
#30

class EditProfileForm(FlaskForm):
#stringfield, etc. imported above
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    profile_photo = FileField('Update Profile Photo', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ChurchSignupForm(FlaskForm):
    church_name = StringField('Church Name', validators=[DataRequired()])
    contact_person = StringField('Contact Person', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone')
    address = StringField('Address')
#    trip_type = SelectField('Mission Trip Type', choices=[
 #       ('medical', 'Medical Mission'),
  #      ('construction', 'Construction Project'),
   #     ('evangelism', 'Evangelism Outreach'),
    #], validators=[DataRequired()])
    num_participants = IntegerField('Number of Participants', validators=[DataRequired(), NumberRange(min=1, message="At least one participant is required")])
    arrival_date = DateField('Arrival Date', format='%Y-%m-%d', validators=[DataRequired()])
    departure_date = DateField('Departure Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_departure_date(self, field):
        # Ensure that the departure date is after the arrival date
        if self.arrival_date.data and field.data < self.arrival_date.data:
            raise ValidationError('Departure date must be after the arrival date.')


class Tb(FlaskForm):
    lodging = IntegerField('Lodging')
    food = IntegerField('Food')
    transportation = IntegerField('Transportation')
    translators = IntegerField('Translators')

class QuoteForm(FlaskForm):
    heading = StringField('Quote', default="Quote", validators=[DataRequired()])
