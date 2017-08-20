from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms.fields import HiddenField, TextAreaField

class New_Question(FlaskForm):
    text = TextAreaField("text", validators=[DataRequired()])

class New_Answer(FlaskForm):
    text = TextAreaField("text", validators=[DataRequired()])
    id = HiddenField("id")
