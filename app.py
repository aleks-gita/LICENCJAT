import json
from flask import Flask
from flask import render_template
from zadanie import Zadanie
from zadanie2 import Zadanie2
from zadanie import Zadanie
from zadanie3 import Zadanie3
from flask import request, redirect
import os
import time

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

zadanie2 = None
zadanie = None
zadanie3 = None
wylosowana = None
wynik = 0
x = None
decyzja = None
czas = 0

@app.route('/', methods=['POST', 'GET'])
def index():
    global zadanie, zadanie2, zadanie3
    if request.method == 'POST':
        if request.form['action'] == "Zadanie 1":
            zadanie = Zadanie()
            #do zadania1 (ospan)
            zadanie.wylosuj()
            zadanie.wynik()
            return redirect("/dzialanie")
        if request.form['action'] == "Zadanie 2":
            zadanie2 = Zadanie2()
            zadanie2.losowanie()
            return redirect("/plansza")
        if request.form['action'] == "Zadanie 3":
            zadanie3 = Zadanie3()
            zadanie3.losowanie()
            return redirect("/zadanie3")

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

@app.route('/zadanie1', methods=['POST', 'GET'])
def zadanie1():
    global zadanie, wynik, x #= Zadanie()
    if zadanie is None:
        return redirect("/")
    if request.method == 'POST':
        zadanie.czyszczenie()
        x = None
        '''if request.form['action'] == "Nastepne":
            zadanie.wyswietl()
            zadanie.wylosuj()
            zadanie.wynik()
            zadanie.litery_los() '''
            #zadanie.wylosuj()
            #zadanie.wynik()
            #wynik = 1
            #zadanie.sprawdzenie()
            #zadanie.rezultat()
        #print("SPR", zadanie.sprawdzenie())

    if request.method == 'GET':
        if request.args.get('action') == "Prawda":
            status = request.args.get('action')
            zadanie.sprawdzenie(status)
            komunikat = zadanie.sprawdzenie(status)
            if komunikat == 'Zgadza sie':
                x = 1

        if request.args.get('action') == "Falsz":
            status = request.args.get('action')
            zadanie.sprawdzenie(status)
            komunikat = zadanie.sprawdzenie(status)
            if komunikat == 'Zgadza sie':
                x = 1
            else:
                x = 0
        if request.args.get('action') == "Zapisz":
            for key in request.args:
                if key.startswith('comment.'):
                    value = key.partition('.')[-1]
                    index = request.args.get(key, type=int)
                    if index != None:
                        index = index - 1
                    #print("Value", value)
                    #print("INDEX", index)
                    zadanie.lista(index, value)
                    zadanie.litery_sprawdzenie()

    return render_template('zadanie1/zadanie1.html', zadanie=zadanie, wynik=wynik, x=x)

@app.route('/dzialanie', methods=['POST', 'GET'])
def dzialanie():
    global zadanie, wynik, x #= Zadanie()
    if zadanie is None:
        return redirect("/")
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
        if len((zadanie.litery_wylosowane)) == 2:
            return redirect('/litera_tabela')
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
    return render_template('zadanie1/tabela.html', zadanie=zadanie, wynik=wynik, x=x)

@app.route('/podsumowanie', methods=['POST', 'GET'])
def podsumowanie():
    global zadanie, wynik, x
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

    return render_template('zadanie1/podsumowanie.html', zadanie=zadanie, wynik=wynik, x=x)

@app.route('/nowa', methods=['POST', 'GET'])
def nowa():
    global zadanie, wynik, x
    if request.method == 'GET':
        zadanie.wyzerowanie_odp()
        redirect('/dzialanie')
    return render_template('nowa.html', zadanie=zadanie, wynik=wynik, x=x)

#ZADANIE 2
@app.route('/plansza', methods=['POST', 'GET'])
def plansza():
    global zadanie2
    if zadanie2 is None:
        return redirect("/")
    if request.method == 'POST':
        zadanie2.losowanie()

    return render_template('zadanie2/plansza.html', zadanie2=zadanie2)

@app.route('/decyzja', methods=['POST', 'GET'])
def decyzja():
    global zadanie2, decyzja, czas
    if zadanie2 is None:
        return redirect("/")
    if request.method == 'POST':
        if request.form['action'] == "TAK" or request.form['action'] == "NIE":
            decyzja = request.form['action']
            czas = request.form['czas'] # do zapisania do bazy danych
            zadanie2.porownanie(decyzja)
            zadanie2.lvl()
            zadanie2.losowanie()

            print(czas)
            return redirect('/plansza')
    return render_template('zadanie2/decyzja.html', zadanie2=zadanie2)

#ZADANIE 3
@app.route('/zadanie3', methods=['POST', 'GET'])
def zadanie3():
    global zadanie3
    if zadanie3 is None:
        return redirect("/")
    if request.method == 'POST':
        if request.form['action'] == "Sprawdz":
            lista = request.form.get('lista')
            print("O", lista)
            zadanie3.sprawdzenie(lista)
            zadanie3.losowanie()

    return render_template('zadanie3/zadanie3.html', zadanie3=zadanie3)

@app.route('/zadanie3_klik', methods=['POST', 'GET'])
def zadanie3_klik():
    global zadanie3, wylosowana
    if zadanie3 is None:
        return redirect("/")
    if request.method == 'POST':
        wylosowana = json.dumps(zadanie3.wylosowana)
    return render_template('zadanie3/zadanie3_klik.html', zadanie3=zadanie3, wylosowana=wylosowana)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5122', debug=True)
