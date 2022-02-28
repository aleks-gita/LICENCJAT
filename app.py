from flask import Flask
from flask import render_template
from zadanie import Zadanie
from flask import request, redirect

app = Flask(__name__)

zadanie = None



@app.route('/start', methods=['POST', 'GET'])
def start():
    global zadanie
    if request.method == 'POST':
        zadanie = Zadanie()
        return redirect("/zadanie1")

    return render_template("start.html")


@app.route('/zadanie1', methods=['POST', 'GET'])
def zadanie1():
    global zadanie #= Zadanie()
    if zadanie is None:
        return redirect("/start")
    if request.method == 'POST':
        if request.form['action'] == "Nastepne":
            zadanie.wylosuj()
            #zadanie.wyswietl()

    return render_template('zadanie1.html',  zadanie=zadanie)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5122', debug=True)
