from flask import Flask
from flask import render_template
from zadanie import Zadanie
from flask import request, redirect

app = Flask(__name__)

zadanie = None
wynik = 0
x = None


@app.route('/start', methods=['POST', 'GET'])
def start():
    global zadanie
    if request.method == 'POST':
        zadanie = Zadanie()
        return redirect("/zadanie1")

    return render_template("start.html")

@app.route('/click', methods=['POST', 'GET'])
def click():

    return render_template("click.html")

@app.route('/zadanie1', methods=['POST', 'GET'])
def zadanie1():
    global zadanie, wynik, x #= Zadanie()
    if zadanie is None:
        return redirect("/start")
    if request.method == 'POST':
        zadanie.czyszczenie()
        x = None
        if request.form['action'] == "Nastepne":
            zadanie.wylosuj()
            zadanie.wynik()
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




    return render_template('zadanie1.html',  zadanie=zadanie, wynik=wynik, x=x)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5122', debug=True)
