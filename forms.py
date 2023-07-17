from flask_wtf import FlaskForm
from wtforms import FileField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class ImageForm(FlaskForm):
    image = FileField('Image', validators=[DataRequired()])
    width = IntegerField('Width', validators=[DataRequired(), NumberRange(min=1)])
    height = IntegerField('Height', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Resize')
