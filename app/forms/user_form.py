from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TelField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional
import re
from app.models.user import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Se souvenir de moi')
    submit = SubmitField('Se connecter')

class RegistrationForm(FlaskForm):
   
    username = StringField('Nom d\'utilisateur', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=6)])
    phone_number = TelField('Numéro de téléphone', validators=[DataRequired()])
    password2 = PasswordField('Répéter le mot de passe', validators=[DataRequired(), EqualTo('password')])
    user_type = SelectField('Type de compte', 
                          choices=[('client', 'Client'), ('vendeur', 'Vendeur')],
                          validators=[DataRequired()])
    submit = SubmitField('S\'inscrire')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Ce nom d\'utilisateur est déjà utilisé.')

    def validate_email(self, email):
        # Validation basique du format email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email.data):
            raise ValidationError('Format d\'email invalide.')
        
        # Vérification si l'email existe déjà
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Cette adresse email est déjà utilisée.')

class ProfileForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Nouveau mot de passe', validators=[Optional(), Length(min=6)])
    password2 = PasswordField('Confirmer le nouveau mot de passe', validators=[Optional(), EqualTo('password')])
    submit = SubmitField('Mettre à jour le profil')

    def __init__(self, original_username=None, original_email=None, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('Ce nom d\'utilisateur est déjà utilisé.')

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('Cette adresse email est déjà utilisée.') 