from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt



app = Flask(__name__)  # Cria uma instância do Flask - referência nesse próprio arquivo
app.config.from_pyfile('config.py')  # Configura o Flask a partir do arquivo config.py

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)

designPATH = 'static/bootstrap.css'


from views_game import *
from views_user import *

if __name__ == '__main__':
    app.run(debug=True)  # Inicia o servidor web do Flask
