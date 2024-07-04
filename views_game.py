from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory
from jogoteca import app, designPATH, db
from models import Jogos, Usuarios
import os
from helpers import recover_img, delete_old_imgs, JogosForm, UsersForm
import time


@app.route('/')  # Define a rota para a página inicial
def index():  # Função que será executada quando a rota for acessada
    lista_jogos = Jogos.query.order_by(Jogos.id)

    return render_template('lista.html', titulo="Jogos", jogos=lista_jogos,
                           design=designPATH)  # Retorna o conteúdo da página home.html


@app.route('/cadastro')  # Define a rota para a página cadastro
def cadastro():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('cadastro')))

    form = JogosForm()
    return render_template('cadastro.html', titulo="Cadastro de Jogo", form=form)  # Retorna o conteúdo da página cadastro.html


@app.route('/criar', methods=['POST', ])
def criar():
    form = JogosForm(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('cadastro'))

    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data

    jogo = Jogos.query.filter_by(nome=nome).first()
    if jogo:
        flash('Jogo já cadastrado!')
        return redirect(url_for('index'))

    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()

    file = request.files['file']
    os.makedirs(app.config['UPLOAD_PATH'], exist_ok=True)    # Cria o diretório caso não exista
    timestamp = time.time()
    file.save(f'{app.config['UPLOAD_PATH']}\\banner_{novo_jogo.id}_{timestamp}.jpg')

    return redirect(url_for('index'))


@app.route('/editar/<int:id>')  # Define a rota para a página cadastro
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))

    jogo = Jogos.query.filter_by(id=id).first()

    form = JogosForm()

    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console

    jogo_banner = recover_img(id)

    return render_template('editar.html', titulo="Edição de Jogo", id=id, jogo_banner=jogo_banner,
                           form=form)  # Retorna o conteúdo da página editar.html


@app.route('/atualizar', methods=['POST', ])
def atualizar():
    form = JogosForm(request.form)

    if form.validate_on_submit():

        jogo = Jogos.query.filter_by(id=request.form['id']).first()

        jogo.nome = form.nome.data
        jogo.categoria = form.categoria.data
        jogo.console = form.console.data

        db.session.add(jogo)
        db.session.commit()

        file = request.files['file']
        timestamp = time.time()
        delete_old_imgs(jogo.id)
        file.save(f'{app.config['UPLOAD_PATH']}\\banner_{jogo.id}_{timestamp}.jpg')

    return redirect(url_for('index'))


@app.route('/deletar/<int:id>')  # Define a rota para a página cadastro
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))
    jogo = Jogos.query.filter_by(id=id).delete()

    db.session.commit()

    flash('Jogo deletado com sucesso!')
    return redirect(url_for('index'))


@app.route('/uploads/<filename>')
def imagem(filename):
    return send_from_directory('uploads', filename)
