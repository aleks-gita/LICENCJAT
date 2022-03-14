from flask import Flask
from flask import render_template
from zadanie import Zadanie
from flask import request, redirect
import time

app = Flask(__name__)

zadanie = None
wynik = 0
x = None


@app.route('/start', methods=['POST', 'GET'])
def start():
    global zadanie
    if request.method == 'POST':
        zadanie = Zadanie()
        zadanie.wylosuj()
        zadanie.wynik()
        return redirect("/zadanie1")

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
        return redirect("/start")
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

    return render_template('zadanie1.html',  zadanie=zadanie, wynik=wynik, x=x)

@app.route('/dzialanie', methods=['POST', 'GET'])
def dzialanie():
    global zadanie, wynik, x #= Zadanie()
    if zadanie is None:
        return redirect("/start")
    if request.method == 'POST':

        zadanie.czyszczenie()
        x = None
        if request.form['action'] == "Nastepne":
            zadanie.wyswietl()
            #zadanie.wylosuj()
            #zadanie.wynik()
            #zadanie.litery_los()
            print("ilosz prawdy", zadanie.dobrze)
            print("ilosz zlych", zadanie.zle)
    return render_template('dzialanie.html', zadanie=zadanie, wynik=wynik, x=x)

@app.route('/wynik', methods=['POST', 'GET'])
def wynik():
    global zadanie, wynik, x  # = Zadanie()
    #if request.method == 'GET':
    return render_template('wynik.html', zadanie=zadanie, wynik=wynik, x=x)


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


    return render_template('litera.html', zadanie=zadanie, wynik=wynik, x=x)


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

    return render_template('litera_tabela.html', zadanie=zadanie, wynik=wynik, x=x)

@app.route('/tabela', methods=['POST', 'GET'])
def tabela():
    global zadanie, wynik, x
    return render_template('tabela.html', zadanie=zadanie, wynik=wynik, x=x)

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

    return render_template('podsumowanie.html', zadanie=zadanie, wynik=wynik, x=x)

@app.route('/nowa', methods=['POST', 'GET'])
def nowa():
    global zadanie, wynik, x
    if request.method == 'GET':
        zadanie.wyzerowanie_odp()

        redirect('/dzialanie')
    return render_template('nowa.html', zadanie=zadanie, wynik=wynik, x=x)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5122', debug=True)
