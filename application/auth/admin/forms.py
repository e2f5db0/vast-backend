from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length

class AdminLoginForm(FlaskForm):
    username = PasswordField('Username', validators=[DataRequired(), Length(min=2), Length(max=30)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2), Length(max=30)])
    submit = SubmitField('')

class LineForm(FlaskForm):
    filename = StringField('Filename', validators=[DataRequired(), Length(min=2), Length(max=30)])
    duration = StringField('Duration', validators=[DataRequired(), Length(min=1), Length(max=3)])
    text = StringField('Text', validators=[DataRequired(), Length(min=1), Length(max=500)])
    choice1 = StringField('Choice 1', validators=[DataRequired(), Length(min=1), Length(max=100)])
    choice2 = StringField('Choice 2', validators=[DataRequired(), Length(min=1), Length(max=100)])
    choice3 = StringField('Choice 3', validators=[DataRequired(), Length(min=1), Length(max=100)])
    submit = SubmitField('Upload')