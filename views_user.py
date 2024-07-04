from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from jogoteca import app, db
from models import Usuarios
from helpers import UsersForm
from flask_bcrypt import check_password_hash, generate_password_hash

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
    if not user:
        flash('Usuário não cadastrado!')
        return redirect(url_for('login'))

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


@app.route('/signup')
def signup():
    form = UsersForm()
    return render_template('signup.html', titulo='Crie sua conta', form=form)


@app.route('/create_user', methods=['POST', ])
def create_user():
    form = UsersForm(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('signup'))

    user = Usuarios(nome=form.name.data, nickname=form.nickname.data,
                    senha=generate_password_hash(form.senha.data))
    db.session.add(user)
    db.session.commit()

    flash('Usuário cadastrado com sucesso!')
    return redirect(url_for('login'))
