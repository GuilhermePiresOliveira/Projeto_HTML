from flask import Flask,render_template,request,redirect,url_for,flash

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine, MetaData

from sqlalchemy.ext.automap import automap_base
from aluno import Aluno

app = Flask(__name__)

import urllib.parse

user = 'root'
password = urllib.parse.quote_plus('senai@123')

host = 'localhost'
database = 'projetodiario1'
connection_string = f'mysql+pymysql://{user}:{password}@{host}/{database}'

engine = create_engine(connection_string)
metadata = MetaData()
metadata.reflect(engine)

Base = automap_base(metadata=metadata)
Base.prepare()

Aluno = Base.classes.aluno

Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro')
def cadastrar_aluno():
    return render_template('novoaluno.html')

@app.route('/diario')
def abirdiario():
    return render_template('dirariobordo.html')


@app.route('/logar', methods=['POST'])
def logar():
    ra = request.form['ra']
    aluno = session.query(Aluno).filter_by(ra=ra).first()
    
    if aluno:
        nome = aluno.nome  # Extrai o nome do aluno
        return render_template('diariobordo.html', ra=ra, nome=nome)
    else:
        mensagem = "RA INVALIDA"
        return render_template('index.html', mensagem=mensagem)


@app.route('/criaraluno', methods=['POST'])
def criar():
    
    ra = request.form['ra']
    nome = request.form['nome']
    tempoestudo = int(request.form['tempoestudo'])
    rendafamiliar = float(request.form['rendafamiliar'])
    aluno = Aluno(ra=ra,nome=nome,tempoestudo=tempoestudo,rendafamiliar=rendafamiliar)

    aluno_existente = session.query(Aluno).filter_by(ra=ra).first()

    if aluno_existente:
        mensagem = "RA já cadastrado no sistema."
        return render_template('index.html', msgbanco=mensagem)

    aluno = Aluno(ra=ra,nome=nome,tempoestudo=tempoestudo,rendafamiliar=rendafamiliar)
    try:
        session.add(aluno)
    except:
        session.rollback()
        raise  
    finally:
        session.close()
        return redirect(url_for('listar_alunos'))


app.run(debug=True)