from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class InputForm(FlaskForm):
    mean_radius = FloatField(label ='Mean Radius', validators=[DataRequired('This feature cannot be empty'), NumberRange(min=0)])
    mean_texture = FloatField(label ='Mean Texture', validators=[DataRequired('This feature cannot be empty'), NumberRange(min=0)])
    mean_perimeter = FloatField(label ='Mean Perimeter', validators=[DataRequired('This feature cannot be empty'), NumberRange(min=0)])
    mean_area = FloatField(label ='Mean Area', validators=[DataRequired('This feature cannot be empty'), NumberRange(min=0)])
    predict = SubmitField('Predict')
