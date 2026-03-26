from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, FloatField
from wtforms.validators import DataRequired, Email, Length, NumberRange


class RegisterForm(FlaskForm):
    full_name = StringField("Full Name", validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    role = SelectField(
        "Role",
        choices=[("tenant", "Tenant"), ("landlord", "Landlord")],
        validators=[DataRequired()]
    )
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class ListingForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=3, max=150)])
    description = TextAreaField("Description", validators=[DataRequired(), Length(min=10)])
    location = StringField("Location", validators=[DataRequired(), Length(min=2, max=150)])
    price = FloatField("Price", validators=[DataRequired(), NumberRange(min=0)])
    room_type = SelectField(
        "Room Type",
        choices=[
            ("single", "Single Room"),
            ("shared", "Shared Room"),
            ("studio", "Studio"),
            ("apartment", "Apartment")
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField("Save Listing")


class RequestForm(FlaskForm):
    message = TextAreaField("Message", validators=[DataRequired(), Length(min=5, max=500)])
    submit = SubmitField("Send Request")