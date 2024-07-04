import os

SECRET_KEY = 'mamou'  # Chave secreta para o Flask

SQLALCHEMY_DATABASE_URI = \
    '{SGDB}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGDB='mysql+mysqlconnector',
        usuario='jogoteca',
        senha='jogoteca',
        servidor='localhost',
        database='jogoteca'
    )

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '\\uploads'  # Define o diretório de uploads