from flask import Flask, flash, redirect, render_template, request, session, abort

import oilyma
import utilz
import json

app = Flask(__name__)

APPLICATION_NAME = 'oilyma'

@app.route("/result")
def results():
    oto = oilyma.Oilyma()
    result = oto.j_data()
    return result

@app.route("/")
def index():
    toto = utilz.Utilz()
    countries = toto.get_countries()
    return render_template('search.html', countries=countries)

@app.route('/', methods=['POST'])
def post_index():
    surname = request.form['surname']
    grade = request.form['grade']
    approval = request.form['approval'].replace(' ', '')
    mileage = request.form['mileage']
    ocons = request.form['ocons']
    country = request.form['country']
    auto = request.form['auto']
    
    toto = oilyma.Oilyma()
    data, error_name = toto.j_sdata(auto=auto, ocons=ocons, mileage=mileage, country=country, grades=[grade], approvals=[approval])
    if data is None:
        return render_template('error.html', error=str(error_name))
    return render_template('results.html', country=country, surname=surname, grade=grade, approval=approval, data=json.loads(data))

@app.route("/test")
def do_test():
    return render_template('test.html', dicto={'name':APPLICATION_NAME})

@app.route("/documents")
def documents():
    return render_template('documents.html', dicto={'name':APPLICATION_NAME})

@app.route("/literature")
def literature():
    return render_template('literature.html', dicto={'name':APPLICATION_NAME})

@app.route("/n52")
def n52():
    return render_template('n52.html', dicto={'name':APPLICATION_NAME})

@app.route("/n42")
def n42():
    return render_template('n42.html', dicto={'name':APPLICATION_NAME})

@app.route("/valvetronic")
def valvetronic():
    return render_template('valvetronic.html', dicto={'name':APPLICATION_NAME})

@app.route("/contact")
def contact_us():
    return render_template('contact.html', dicto={'name':APPLICATION_NAME})

@app.route("/hello/<string:name>/")
def hello(name):
    return render_template('index.html', name=name)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
