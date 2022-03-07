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
        if request.form['action'] == "Nastepne":
            zadanie.wyswietl()
            zadanie.wylosuj()
            zadanie.wynik()
            zadanie.litery_los()
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
            index=request.args.getlist('type', type=int)
            print("Indexy",index)




    return render_template('zadanie1.html',  zadanie=zadanie, wynik=wynik, x=x)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5122', debug=True)
