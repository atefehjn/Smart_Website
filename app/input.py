from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class PredictionForm(FlaskForm):
    mean_radius = FloatField('Mean Radius', validators=[DataRequired(), NumberRange(min=0)])
    mean_texture = FloatField('Mean Texture', validators=[DataRequired(), NumberRange(min=0)])
    mean_perimeter = FloatField('Mean Perimeter', validators=[DataRequired(), NumberRange(min=0)])
    mean_area = FloatField('Mean Area', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Submit')
