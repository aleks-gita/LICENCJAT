import json
import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objs import *
import plotly.io as pio
from IPython.display import Image
from flask import Flask
from flask import render_template,request,url_for,redirect,flash
from markupsafe import Markup
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os
from zadanie2 import Zadanie2_class
from zadanie import Zadanie
from zadanie3 import Zadanie3_class
from databases import User, Zadanie1, Zadanie2, Zadanie3
from flask import request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask,render_template,request,url_for
from flask_sqlalchemy import SQLAlchemy
from flask import json


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Lic.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)

zadanie2 = None
zadanie = None
zadanie3 = None
wylosowana = None
wynik = 0
wynik3=0
x = None
decyzja = None
czas = 0
koniec_licznik = 0
cos = 0



@login_manager.user_loader
def load_user(user_id):

    return User.query.get(user_id)

#@app.route('/home')
#def home():
#    return render_template('index.html')

@app.route('/register', methods = ['POST','GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username =form.username.data, email = form.email.data)
        user.set_password(form.password1.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            next = request.args.get("next")
            return redirect(next or url_for('index'))
        flash('Invalid email address or Password.')
    return render_template('login.html', form=form)

@app.route("/forbidden",methods=['GET', 'POST'])

@login_required
def protected():
    return redirect(url_for('forbidden.html'))

@app.route("/logout")
# @login_required
def logout():
    logout_user()
    return redirect(url_for('start_page'))

@app.route('/start_page', methods=['POST', 'GET'])
def start_page():
    return render_template("start_page.html")

@app.route('/index', methods=['POST', 'GET'])
def index():
    global zadanie, zadanie2, zadanie3, cos
    if current_user.is_anonymous:
        return redirect(url_for('start_page'))
    if request.method == 'POST':
        if current_user.is_anonymous:
            return redirect(url_for('start_page'))
        if request.form['action'] == "Zadanie 1":
            zadanie = Zadanie()
            #do zadania1 (ospan)
            zadanie.losuj_dlugosc_bloku()
            zadanie.pomieszanie()
            zadanie.wylosuj()
            zadanie.wynik()
            return redirect(url_for('ospan'))
        if request.form['action'] == "Zadanie 2":
            zadanie2 = Zadanie2_class()
            zadanie2.generowanie()
            zadanie2.losowanie()
            return redirect(url_for('nback'))
        if request.form['action'] == "Zadanie 3":
            zadanie3 = Zadanie3_class()
            zadanie3.losowanie()
            cos = zadanie3.wylosowana
            return redirect(url_for("digit"))
        if request.form['action'] == "Wykres OSPAN":
            return redirect(url_for("wykres1"))
        if request.form['action'] == "Wykres N-back":
            return redirect(url_for('wykres2'))
        if request.form['action'] == "Wykres Digit Backward":
            return redirect(url_for("wykres3"))

    return render_template("start.html")

@app.route('/click', methods=['POST', 'GET'])
def click():
    global zadanie
    zadanie = Zadanie()
    if request.method == 'POST':
        for key in request.form:
            if key.startswith('comment.'):
                value = key.partition('.')[-1]
                index = request.form.get(key, type=int)
                #index = index - 1
                print("Value", value)
                print("INDEX", index)
                zadanie.lista(index, value)
    return render_template("click.html")

@app.route('/ospan',  methods=['POST', 'GET'])
def ospan():
    global zadanie
    if request.method == 'POST':
        if request.form['action'] == "Zadanie 1":
            zadanie = Zadanie()
            # do zadania1 (ospan)
            zadanie.losuj_dlugosc_bloku()
            zadanie.pomieszanie()
            zadanie.wylosuj()
            zadanie.wynik()
            return redirect(url_for("dzialanie"))

    wykres1 = Zadanie1.query.filter_by(user_id=current_user.id).all()
    wynik = [i.wynik for i in wykres1]
    date = [i.date for i in wykres1]
    df = pd.DataFrame({
        'Punkty': wynik,
        'Data': date
    })

    fig = px.line(df,x='Data', y='Punkty', template="plotly_dark", markers=True,  width=1000, height=500)
    fig.add_trace(go.Scatter(x=date, y=wynik, mode='lines+markers', name='Wyniki'))
    #fig.add_trace(go.Scatter(x=date, y=bledy, mode='lines+markers', name='Bledy'))
    graphJSON1 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('zadanie1/Ospan.html', graphJSON1=graphJSON1, layout=layout)
@app.route('/ospan2', methods=['POST', 'GET'])
def ospan2():
    global zadanie
    if request.method == 'POST':
        if request.form['action'] == "Zadanie 1":
            zadanie = Zadanie()
            # do zadania1 (ospan)
            zadanie.losuj_dlugosc_bloku()
            zadanie.pomieszanie()
            zadanie.wylosuj()
            zadanie.wynik()
            return redirect(url_for("dzialanie"))
    return render_template('zadanie1/Ospan2.html')

@app.route('/dzialanie', methods=['POST', 'GET'])
def dzialanie():
    global zadanie, wynik, x #= Zadanie()
    if zadanie is None:
        return redirect(url_for('start_page'))
    if request.method == 'POST':
        zadanie.czyszczenie()
        x = None
        if request.form['action'] == "Przejdź dalej":
            zadanie.wyswietl()
            #zadanie.wylosuj()
            #zadanie.wynik()
            #zadanie.litery_los()
            print("ilosz prawdy", zadanie.dobrze)
            print("ilosz zlych", zadanie.zle)
    return render_template('zadanie1/dzialanie.html', zadanie=zadanie, wynik=wynik, x=x)

@app.route('/wynik', methods=['POST', 'GET'])
def wynik():
    global zadanie, wynik, x  # = Zadanie()
    #if request.method == 'GET':
    return render_template('zadanie1/wynik.html', zadanie=zadanie, wynik=wynik, x=x)


@app.route('/litera', methods=['POST', 'GET'])
def litera():
    global zadanie, wynik, x  # = Zadanie()
    if request.method == 'GET':
        if request.args.get('action') == "Prawda":
            status = request.args.get('action')
            zadanie.sprawdzenie(status)
            #komunikat = zadanie.sprawdzenie(status)
            #if komunikat == 'Zgadza sie':
            #    x = 1
        if request.args.get('action') == "Falsz":
            status = request.args.get('action')
            zadanie.sprawdzenie(status)
            #komunikat = zadanie.sprawdzenie(status)
            #if komunikat == 'Zgadza sie':
             #   x = 1
            #else:
            #    x = 0
        if len((zadanie.litery_wylosowane)) == (zadanie.dlugosc_bloku - 1):
            return redirect(url_for('litera_tabela'))
        zadanie.litery_los()
        zadanie.czyszczenie()
        zadanie.wylosuj()
        zadanie.wynik()
    return render_template('zadanie1/litera.html', zadanie=zadanie, wynik=wynik, x=x)


@app.route('/litera_tabela', methods=['POST', 'GET'])
def litera_tabela():
    global zadanie, wynik, x  # = Zadanie()
    if request.method == 'GET':
        if request.args.get('action') == "Prawda":
            status = request.args.get('action')
            zadanie.sprawdzenie(status)
            #komunikat = zadanie.sprawdzenie(status)
            #if komunikat == 'Zgadza sie':
            #    x = 1
        if request.args.get('action') == "Falsz":
            status = request.args.get('action')
            zadanie.sprawdzenie(status)
            #komunikat = zadanie.sprawdzenie(status)
            #if komunikat == 'Zgadza sie':
            #    x = 1
            #else:
            #    x = 0
        zadanie.litery_los()
        #zadanie.czyszczenie()
        #zadanie.wylosuj()
        zadanie.wynik()
    return render_template('zadanie1/litera_tabela.html', zadanie=zadanie, wynik=wynik, x=x)

@app.route('/tabela', methods=['POST', 'GET'])
def tabela():
    global zadanie, wynik, x
    if zadanie is None:
        return redirect(url_for('start_page'))
    return render_template('zadanie1/tabela.html', zadanie=zadanie, wynik=wynik, x=x)

@app.route('/podsumowanie', methods=['POST', 'GET'])
def podsumowanie():
    global zadanie, wynik, x, koniec_licznik
    if zadanie is None:
        return redirect(url_for('start_page'))
    if request.method == 'GET':
        if request.args.get('action') == "Zapisz":
            for key in request.args:
                if key.startswith('comment.'):
                    value = key.partition('.')[-1]
                    index = request.args.get(key, type=int)
                    if index != None:
                        index = index - 1
                    # print("Value", value)
                    # print("INDEX", index)
                    zadanie.lista(index, value)
                    zadanie.litery_sprawdzenie()
            #zadanie.wylosuj()
            #zadanie.wynik()
        zadanie.procent()
        zadanie.czyszczenie_tabela()
        zadanie.czyszczenie()
        zadanie.wylosuj()
        zadanie.wynik()
        zadanie.losuj_dlugosc_bloku()
        zadanie.statystyka()

        koniec_licznik += 1
        licznik = json.dumps(koniec_licznik)
        #if koniec_licznik == 3:
        #    return redirect("/koniec")

    return render_template('zadanie1/podsumowanie.html', zadanie=zadanie, wynik=wynik, x=x, koniec_licznik=koniec_licznik, licznik=licznik)

@app.route('/nowa', methods=['POST', 'GET'])
def nowa():
    global zadanie, wynik, x
    if request.method == 'GET':
        zadanie.wyzerowanie_odp()
        redirect(url_for('dzialanie'))
    return render_template('nowa.html', zadanie=zadanie, wynik=wynik, x=x)

@app.route('/koniec', methods=['POST', 'GET'])
def koniec():
    global zadanie, wynik, x
    if zadanie is None:
        return redirect(url_for('start_page'))
    if request.method == 'POST':
        if request.form['action'] == "Zobacz podsumowanie":
            wynik_dobry = zadanie.dobrze_statystyka
            wynik_zly = zadanie.zle_statystyka
            litera_wynik= zadanie.punkty_do_statystyki
            litera_max = zadanie.wszystkie_do_statystyki
            wynik = zadanie.punkty_nowe
            zadanie1 = Zadanie1(dobre_wyniki=wynik_dobry, zle_wyniki=wynik_zly, user_id=current_user.id, litery_max=litera_max, litery_wynik=litera_wynik, wynik= wynik)
            db.session.add(zadanie1)
            db.session.commit()
    return render_template('zadanie1/koniec.html', zadanie=zadanie, wynik=wynik, x=x)

#ZADANIE 2

@app.route('/instrukcja', methods=['POST', 'GET'])
def instrukcja():
    global zadanie2
    if request.method == 'POST':
        if request.form['action'] == "Zadanie 2":
            zadanie2 = Zadanie2_class()
            zadanie2.generowanie()
            zadanie2.losowanie()
            return redirect(url_for('plansza'))
    return render_template('zadanie2/instrukcja.html', zadanie2=zadanie2)

@app.route('/nback', methods=['POST', 'GET'])
def nback():
    global zadanie2
    if request.method == 'POST':
        if request.form['action'] == "Instrukcja":
            zadanie2 = Zadanie2_class()
            #        zadanie2.generowanie()
            #        zadanie2.losowanie()
            return redirect(url_for('instrukcja'))
    wykres2 = Zadanie2.query.filter_by(user_id=current_user.id).all()
    wykres_z2= Zadanie2.query.with_entities(Zadanie2.wynik_n_1).all()
    wykres_n1 = [i.wynik_n_1 for i in wykres2]
    wykres_n2 = [i.wynik_n_2 for i in wykres2]
    wykres_n3 = [i.wynik_n_3 for i in wykres2]
    wykres_cal = [i.wynik_cal for i in wykres2]
    date= [i.date for i in wykres2]

    df = pd.DataFrame({
        'N=1': wykres_n1,
        'N=2': wykres_n2,
        'N=3': wykres_n3,
        'Punkty':wykres_cal,
        'Data': date
    })
    fig = px.line(df,x='Data', y='Punkty', template="plotly_dark", markers=True,  width=1000, height=500)
    fig.add_trace(go.Scatter( x=date, y=wykres_n1,  mode='lines+markers', name='N=1'))
    fig.add_trace(go.Scatter(x=date, y=wykres_n2, mode='lines+markers', name='N=2'))
    fig.add_trace(go.Scatter(x=date, y=wykres_n3, mode='lines+markers', name='N=3'))
    fig.add_trace(go.Scatter(x=date, y=wykres_cal, mode='lines+markers', name='Wszystkie'))

    graphJSON2 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('zadanie2/Nback.html', graphJSON2=graphJSON2, layout=layout)

@app.route('/nback2', methods=['POST', 'GET'])
def nback2():
    global zadanie2
    if request.method == 'POST':
        if request.form['action'] == "Instrukcja":
            zadanie2 = Zadanie2_class()
    #        zadanie2.generowanie()
    #        zadanie2.losowanie()
            return redirect(url_for('instrukcja'))
    return render_template('zadanie2/Nback2.html')

@app.route('/plansza', methods=['POST', 'GET'])
def plansza():
    global zadanie2
    if zadanie2 is None:
        return redirect(url_for('start_page'))
    if request.method == 'POST':
        #zadanie2.generowanie()
        zadanie2.losowanie()

    return render_template('zadanie2/plansza.html', zadanie2=zadanie2)

@app.route('/decyzja', methods=['POST', 'GET'])
def decyzja():
    global zadanie2, decyzja, czas
    if zadanie2 is None:
        return redirect(url_for('start_page'))
    if request.method == 'POST':
        name = request.form['action']
        if name == "TAK" or name == "NIE" or name == "BRAK":
            print(request.form['action'])
            decyzja = request.form['action']
            czas = request.form['czas'] # do zapisania do bazy danych
            zadanie2.porownanie(decyzja)
            if len(zadanie2.lista) == 25:
                if zadanie2.n==3:
                    zadanie2.obliczenie_wyniku()
                    zadanie2.obliczenie_wyniku_calkowitego()
                    print("---------------",
                          "comm:", zadanie2.commissions,
                          "omm", zadanie2.omissions,
                          "corr", zadanie2.correct,
                          'wynik', zadanie2.wynik,
                          "WYNIK CALKOWITY", zadanie2.wynik_cal)
                    zadanie2db = Zadanie2(wynik_n_1=zadanie2.wynik1, wynik_n_2=zadanie2.wynik2, wynik_n_3=zadanie2.wynik3, wynik_cal=zadanie2.wynik_cal, user_id=current_user.id)
                    db.session.add(zadanie2db)
                    db.session.commit()
                    zadanie2.czyszczenie()
                    return redirect(url_for('koniec2'))
                #zadanie2.lvl()
                #zadanie2.generowanie()
                zadanie2.obliczenie_wyniku()
                print("---------------",
                      "comm:", zadanie2.commissions,
                      "omm", zadanie2.omissions,
                      "corr", zadanie2.correct,
                      'wynik', zadanie2.wynik)
                zadanie2db = Zadanie2(wynik_n_1=zadanie2.wynik1, wynik_n_2=zadanie2.wynik2, wynik_n_3=zadanie2.wynik3,
                                    user_id=current_user.id)
                zadanie2.lvl()
                zadanie2.generowanie()
                zadanie2.czyszczenie()
                zadanie2.liczenie = 0
                zadanie2.punkty=0
                zadanie2.punkty_zle=0
                return redirect(url_for('nowy_lvl'))

            zadanie2.losowanie()
            print(czas)
            return redirect(url_for('plansza'))
        if name == '':
            print('asdadsd')
    return render_template('zadanie2/decyzja.html', zadanie2=zadanie2)

@app.route('/nowy_lvl', methods=['POST', 'GET'])
def nowy_lvl():
    global zadanie2
    if zadanie2 is None:
        return redirect(url_for('start_page'))
    if request.method == 'POST':
        #zadanie2.czyszczenie()
        #zadanie2.czyszczenie()
        zadanie2.losowanie()

    return render_template('zadanie2/nowy_lvl.html', zadanie2=zadanie2)

@app.route('/koniec2', methods=['POST', 'GET'])
def koniec2():
    global zadanie2
    if zadanie2 is None:
        return redirect(url_for('start_page'))
    #if request.method == 'POST':
    return render_template('zadanie2/koniec2.html', zadanie2=zadanie2)

#ZADANIE 3
@app.route('/digit', methods=['POST', 'GET'])
def digit():
    pio.templates
    global zadanie3
    if request.method == 'POST':
        if request.form['action'] == "Zadanie 3":
            zadanie3 = Zadanie3_class()
            zadanie3.losowanie()
            cos = zadanie3.wylosowana
            return redirect(url_for('zadanie3'))
    wykres3 = Zadanie3.query.filter_by(user_id=current_user.id).all()
    wykres_wynik = [i.wynik for i in wykres3]
    bledy = [i.bledy for i in wykres3]
    date = [i.date for i in wykres3]
    df = pd.DataFrame({
        'Punkty': wykres_wynik,
        'Bledy': bledy,
        'Data': date
    })
    fig = px.line(df, x='Data', y='Punkty', template="plotly_dark", markers=True, width=1000, height=500)
    # fig = go.Figure(template="plotly_dark")
    fig.add_trace(go.Scatter(x=date, y=wykres_wynik, mode='lines+markers', name='Wyniki'))
    fig.add_trace(go.Scatter(x=date, y=bledy, mode='lines+markers', name='Bledy'))

    fig.update_layout({
        # 'plot_bgcolor': '#ffe54c',
        # 'paper_bgcolor': '#ffe54c',
    })
    graphJSON3 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('zadanie3/Digit.html', graphJSON3=graphJSON3, layout=layout)

@app.route('/digit2', methods=['POST', 'GET'])
def digit2():
    global zadanie3
    if request.method == 'POST':
        if request.form['action'] == "Zadanie 3":
            zadanie3 = Zadanie3_class()
            zadanie3.losowanie()
            cos = zadanie3.wylosowana
            return redirect(url_for('zadanie3'))
    return render_template('zadanie3/Digit2.html')

@app.route('/zadanie3', methods=['POST', 'GET'])
def zadanie3():
    global zadanie3, wylosowana, cos
    if zadanie3 is None:
        return redirect(url_for('start_page'))
    if request.method == 'POST':
        if request.form['action'] == "Sprawdź":
            lista = request.form.get('lista')
            print("O", lista)
            zadanie3.sprawdzenie(lista)
            if zadanie3.bledy == 2:
                return redirect(url_for('koniec3'))
            zadanie3.losowanie()
            cos = zadanie3.wylosowana
            #cos = json.dumps(cos)

    return render_template('zadanie3/zadanie3.html', zadanie3=zadanie3, wylosowana= wylosowana, cos=cos)

@app.route('/zadanie3_klik', methods=['POST', 'GET'])
def zadanie3_klik():
    global zadanie3, wylosowana
    if zadanie3 is None:
        return redirect(url_for('start_page'))
    if request.method == 'POST':
        wylosowana = json.dumps(zadanie3.wylosowana)

    return render_template('zadanie3/zadanie3_klik.html', zadanie3=zadanie3, wylosowana=wylosowana)

@app.route('/koniec3', methods=['POST', 'GET'])
def koniec3():
    global zadanie3
    if zadanie3 is None:
        return redirect(url_for('start_page'))
    if zadanie3.bledy == 2:
        wynik3 = zadanie3.wynik
        bledy = zadanie3.bledy
        max = 8
        zadanie3 = Zadanie3(wynik=wynik3, max=max, bledy=bledy, user_id=current_user.id)
        db.session.add(zadanie3)
        db.session.commit()
    #if request.method == 'POST':
    return render_template('zadanie3/koniec3.html', zadanie3=zadanie3)

@app.route('/podsumowanie3', methods=['POST', 'GET'])
def podsumowanie3():
    global zadanie3, wynik3
    if zadanie3 is None:
        return redirect(url_for('start_page'))
    if request.method == 'POST':
        if zadanie3.bledy == 2:
            wynik3 = zadanie3.wynik
            bledy= zadanie3.bledy
            max = 8
            zadanie3 = Zadanie3(wynik=wynik3, max=max, bledy=bledy, user_id=current_user.id)
            db.session.add(zadanie3)
            db.session.commit()
    return render_template('zadanie3/podsumowanie3.html', zadanie3=zadanie3)



@app.route('/bibliografia')
def bibliografia():
    return render_template('bibliografia.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5122', debug=True)
