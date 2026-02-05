from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email

class SocioForm(FlaskForm):
    nombre = StringField('Nombre Completo', validators=[DataRequired()])
    email = EmailField('Correo Electrónico', validators=[DataRequired(), Email()])
    submit = SubmitField('Guardar Socio')