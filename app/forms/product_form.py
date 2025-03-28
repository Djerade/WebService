from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, FloatField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, NumberRange

class ProductForm(FlaskForm):
    name = StringField('Nom du produit', validators=[DataRequired()])
    category = SelectField('Catégorie', choices=[
        ('fruits', 'Fruits'),
        ('legumes', 'Légumes'),
        ('viandes', 'Viandes'),
        ('fromages', 'Fromages'),
        ('autres', 'Autres')
    ], validators=[DataRequired()])
    description = TextAreaField('Description')
    price = FloatField('Prix', validators=[DataRequired(), NumberRange(min=0)])
    stock = IntegerField('Stock', validators=[DataRequired(), NumberRange(min=0)])
    image = FileField('Image du produit', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images uniquement!')
    ])
    submit = SubmitField('Enregistrer') 