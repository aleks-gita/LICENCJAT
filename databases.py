from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Lic.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(50), index=True, unique = True)
  email = db.Column(db.String(150), unique = True, index = True)
  password_hash = db.Column(db.String(150))
  joined_at = db.Column(db.DateTime(), default = datetime.utcnow, index = True)
  zadanie1 = db.relationship('Zadanie1', backref='user', lazy='dynamic')
  zadanie2 = db.relationship('Zadanie2', backref='user', lazy='dynamic')
  zadanie3 = db.relationship('Zadanie3', backref='user', lazy='dynamic')

  def set_password(self, password):
        self.password_hash = generate_password_hash(password)

  def check_password(self,password):
      return check_password_hash(self.password_hash,password)

class Zadanie1(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    date= db.Column(db.DateTime(), default = datetime.utcnow, index = True)
    dobre_wyniki = db.Column(db.Integer, index = True)
    zle_wyniki = db.Column(db.Integer, index=True)
    litery_max = db.Column(db.Integer, index=True)
    litery_wynik = db.Column(db.Integer, index=True)
    wynik = db.Column(db.Integer, index=True)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'))

class Zadanie2(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    date= db.Column(db.DateTime(), default = datetime.utcnow, index = True)
    wynik_n_1=db.Column(db.FLOAT, index = True)
    wynik_n_2=db.Column(db.FLOAT, index = True)
    wynik_n_3=db.Column(db.FLOAT, index = True)
    wynik_cal=db.Column(db.FLOAT, index = True)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'))

class Zadanie3(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    date= db.Column(db.DateTime(), default = datetime.utcnow, index = True)
    wynik=db.Column(db.Integer, index = True)
    max=db.Column(db.Integer, index = True)
    bledy = db.Column(db.Integer, index=True)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'))