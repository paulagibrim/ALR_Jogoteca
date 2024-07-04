import os

from wtforms import StringField, FileField, SubmitField, validators, PasswordField
from jogoteca import app, designPATH, db
from flask_wtf import FlaskForm


class JogosForm(FlaskForm):
    nome = StringField('Nome do Jogo', [validators.DataRequired(), validators.Length(min=2, max=50)]) # Mesmo máximo que o banco
    categoria = StringField('Categoria', [validators.DataRequired(), validators.Length(min=1, max=40)])
    console = StringField('Console', [validators.DataRequired(), validators.Length(min=1, max=20)])
    # file = FileField('Banner')
    salvar = SubmitField('Salvar')


class UsersForm(FlaskForm):
    nickname = StringField('Nickname', [validators.DataRequired(), validators.Length(min=2, max=8)])
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=2, max=100)])
    login = SubmitField('Login')


def recover_img(id):
    for filename in os.listdir(app.config['UPLOAD_PATH']):
        if f'banner_{id}' in filename:
            return filename

    return 'default_banner.jpg'


def delete_old_imgs(id):
    file = recover_img(id)
    if file != 'default_banner.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], file))

    # return 'default_banner.jpg'
