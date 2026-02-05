from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class LibroForm(FlaskForm):
    titulo = StringField(
        "Título",
        validators=[DataRequired(message="El título es obligatorio"), Length(max=200)]
    )

    autor = StringField(
        "Autor",
        validators=[DataRequired(), Length(max=100)]
    )

    año = StringField (
        "Año",validators=[Length(max=4)]
    )
    
    categoria = StringField(
        "Categoría", validators=[Length(max=100)]
    ) 
    
    id_socio = StringField(
        "ID Socio", validators=[Length(max=50)] 
    )

    submit = SubmitField("Guardar")
