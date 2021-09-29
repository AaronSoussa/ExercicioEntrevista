from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
import os
from flask import request
from flask import redirect

meudir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(meudir, 'teste.db')
db = SQLAlchemy(app)



class Contact(db.Model):
    __tablename__ = "contacts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    tel = db.Column(db.String(50), unique=True, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return '<Contacts %r>' % self.name



@app.route("/")
def testando_tabela():
    contatos = Contact.query.all()

    return render_template("index.html", contatos=contatos)

@app.route("/cadastro", methods=["GET","POST"])
def cadastro():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form["email"]
        tel = request.form['tel']
        age = request.form['age']

        contact = Contact(name=name, email=email, tel=tel, age=age)
        db.session.add(contact)
        db.session.commit()
    return redirect('/')

@app.route("/editar/<id>", methods=["GET","POST"])
def editar(id):
    contato = Contact.query.get(id)
    if request.method == 'POST':
        contato.name = request.form['name']
        contato.email = request.form["email"]
        contato.tel = request.form['tel']
        contato.age = request.form['age']
        db.session.commit()
        return redirect('/')

    return render_template("editar.html", item=contato)

@app.route("/deletar/<id>", methods = ["DELETE","GET","POST"])
def deletar(id):
    contato = Contact.query.get(id)
    db.session.delete(contato)
    db.session.commit()
    return redirect('/')
