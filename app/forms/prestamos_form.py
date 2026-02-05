from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

class PrestamosForm(FlaskForm):
    socio_id = SelectField(
        "Seleccionar Socio",
        coerce=int,
        validators=[DataRequired(message="Debes seleccionar un socio para realizar el préstamo")]
    )
    
    submit = SubmitField("Confirmar Préstamo")
    