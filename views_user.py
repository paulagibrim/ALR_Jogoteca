from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from jogoteca import app
from models import Usuarios
from helpers import UsersForm
from flask_bcrypt import check_password_hash

@app.route('/login')
def login():
    form = UsersForm()

    if request.args.get('proxima'):
        proxima = request.args.get('proxima')
    else:
        proxima = url_for('index')

    return render_template('login.html',
                           titulo="Faça seu login", proxima=proxima, form=form)


@app.route('/auth', methods=['POST', ])
def auth():
    form = UsersForm(request.form)
    user = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    senha = check_password_hash(user.senha, form.senha.data)

    if user and senha:
        session['usuario_logado'] = user.nickname
        flash(user.nickname + ' logou com sucesso!')

        prox_pagina = request.form['proxima']

        return redirect(prox_pagina or url_for('index'))

    else:
        flash('Não logado, tente novamente!')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com successo!')
    return redirect(url_for('index'))

