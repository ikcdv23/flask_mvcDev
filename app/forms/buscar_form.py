from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length

class BuscarForm(FlaskForm):
    # Campo de texto para buscar
    busqueda = StringField(
        'Buscar', 
        validators=[Length(max=100)],
        render_kw={"placeholder": "Buscar por título o autor..."} # Atributo HTML
    )
    
    submit = SubmitField('Buscar')

    # Desactivar CSRF solo para este form
    class Meta:
        csrf = False