from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify, send_from_directory
import os

import oilyma
import utilz
import json

app = Flask(__name__)

APPLICATION_NAME = 'oilyma'
debug= False

@app.route("/hello/<string:name>/")
def hello(name):
    return render_template('index.html', name=name)

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

@app.route("/n46")
def n46():
    return render_template('n42.html', dicto={'name':APPLICATION_NAME})

@app.route("/m54")
def m54():
    return render_template('m54.html', dicto={'name':APPLICATION_NAME})

@app.route("/m52")
def m52():
    return render_template('m54.html', dicto={'name':APPLICATION_NAME})

@app.route("/valvetronic")
def valvetronic():
    return render_template('valvetronic.html', dicto={'name':APPLICATION_NAME})

@app.route("/about")
def about():
    return render_template('about.html', dicto={'name':APPLICATION_NAME})

@app.route("/services")
def services():
    return render_template('services.html', dicto={'name':APPLICATION_NAME})

@app.route("/references")
def references():
    return render_template('references.html', dicto={'name':APPLICATION_NAME})

@app.route("/n53")
def n53():
    return render_template('n53.html', dicto={'name':APPLICATION_NAME})

@app.route("/contact")
def contact():
    return render_template('contact.html', dicto={'name':APPLICATION_NAME})

@app.route("/tools")
def tools():
    ptitle = 'Tools'
    return render_template('tools.html', **locals())

@app.route("/vehicles")
def vehicles():
    return render_template('vehicles.html', dicto={'name':APPLICATION_NAME})

@app.route("/cars")
def car_search():
    return render_template('car_search.html', dicto={'name':APPLICATION_NAME})

@app.route("/diagnosis")
def diagnosis():
    return render_template('diagnosis.html', dicto={'name':APPLICATION_NAME})

@app.route("/coding")
def coding():
    return render_template('coding.html', dicto={'name':APPLICATION_NAME})

@app.route("/programing")
def programing():
    return render_template('programing.html', dicto={'name':APPLICATION_NAME})


@app.route('/favicon.png')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.png', mimetype='image/png')
@app.route('/favicon.ico')
def favicon_ico():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/calc", methods=['PUT', 'POST', 'GET'])
def calc():
    hp, cc, weight = 80, 1.0, 900
    if debug:
        print('REQUEST', len(request.args), len(request.form), request.data, request.method, request.json)
    if str(request.method) == 'GET':
        return render_template('calc.html', dicto={'name':APPLICATION_NAME})
    if str(request.method) == 'POST':
        if request.form:
            hp = request.form['hp_input']
            cc = request.form['cp_range']
            weight = request.form['vw_input']
        if request.args.get('hp_input'):
            hp = request.args.get('hp_input')
        if request.args.get('cp_range'):
            cc = request.args.get('cp_range')
        if request.args.get('vw_input'):
            weight = request.args.get('vw_input')
        if debug:
            print('ARGS', weight, hp, cc)
        toto = utilz.Utilz()
        pwr, target_torque = toto.pw_ratio(weight=weight, power=hp, cylinder=cc)
        if debug:
            print(pwr, target_torque)
        #return jsonify({'data': render_template('calc_results.html', pwr=pwr, target_torque=target_torque, dicto={'name':APPLICATION_NAME})})
        return jsonify({'data': {'pwr':pwr, 'target_torque':target_torque}})

@app.route("/fuelcons", methods=['PUT', 'POST', 'GET'])
def fuel_cons():
    f_tank, exp_mileage, t_cons, exp_cost = 0.0, 0.0, 0.0, 0.0
    toto = utilz.Utilz()
    if request.form:
        mileage = request.form['mileage']
        up = request.form['up']
        cost = request.form['cost']
        cons = request.form['cons']
    if request.args.get('up'):
        up = request.args.get('up')
    if request.args.get('mileage'):
        mileage = request.args.get('mileage')
    if request.args.get('cost'):
        cost = request.args.get('cost')
    if request.args.get('cons'):
        cost = request.args.get('cons')
    if cost is None or cost == '':
        f_tank, exp_mileage, t_cons, exp_cost = toto.fuel_cons(mileage=mileage, cost=cost, up=up, cons=cons)
        return jsonify({'data': {'f_tank':f_tank, 'exp_mileage':exp_mileage, 't_cons':t_cons, 'exp_cost':exp_cost}})
    f_tank, exp_mileage, t_cons = toto.fuel_cons(mileage=mileage, cost=cost, up=up, cons=cons)
    return jsonify({'data': {'f_tank':f_tank, 'exp_mileage':exp_mileage, 't_cons':t_cons}})

############################################# MAIN ############################
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
