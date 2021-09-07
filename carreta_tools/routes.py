from flask import render_template, url_for, redirect, request, flash
from flask_login import current_user, login_user, logout_user
from carreta_tools import app, grafico, data, user, api_key, db
from carreta_tools.pySteamSignIn import SteamSignIn
from carreta_tools.models import Hero
import requests


@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    steam_login = SteamSignIn()
    return steam_login.redirect_user(steam_login.construct_url('http://127.0.0.1:5000/process_login'))


@app.route('/process_login', methods=['GET', 'POST'])
def process_login():
    steam_login = SteamSignIn()

    steam_id = steam_login.validate_results(request.values)
    usuario = user.User(steam_id)
    login_user(usuario, remember=True)

    return redirect(url_for('home_page'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home_page'))


@app.route("/meta/update")
def meta_update():
    new_data = data.Data()
    new_data.data_to_json()
    del new_data
    return redirect(url_for('meta_page'))


@app.route("/meta")
def meta_page():
    return render_template('meta.html')


@app.route("/meta/hc")
def meta_hc_page():
    return render_template('meta_hc.html', graph_img=get_graph(1))


@app.route("/meta/mid")
def meta_mid_page():
    return render_template('meta_mid.html', graph_img=get_graph(2))


@app.route("/meta/off")
def meta_off_page():
    return render_template('meta_off.html', graph_img=get_graph(3))


@app.route("/meta/sup")
def meta_sup_page():
    return render_template('meta_sup.html', graph_img=get_graph(4))


@app.route("/meta/hsup")
def meta_hsup_page():
    return render_template('meta_hsup.html', graph_img=get_graph(5))


def get_graph(pos):
    hero, matches, winrate = data.prepare_data(pos)
    grafico.generate_graph(hero, matches, winrate, pos)
    return url_for('static', filename=f'graph_{pos}.jpg')


@app.route("/perfil")
def perfil_page():
    if current_user is None:
        return render_template('home.html')
    return render_template('perfil.html')


@app.route("/import_heroes", methods=['GET', 'POST'])
def import_heroes():
    json_url = f"https://api.steampowered.com/IEconDOTA2_570/GetHeroes/v0001/?format=JSON&key={api_key}"
    data = parse_json(json_url)

    heroes = data['result']['heroes']
    for hero in heroes:
        hero_db = Hero(
            hero_id=hero['id'],
            steamdb_name=hero['name'])
        try:
            if Hero.query.filter_by(hero_id=hero['id']).first().hero_id == hero['id']:
                flash(f'{hero["name"][14:]} já importado!', 'danger')
            else:
                db.session.add(hero_db)
                db.session.commit()
                flash(f'{hero["name"][14:]} importado com sucesso!', 'success')
        except:
            pass
    return redirect(url_for('admin_page'))


def parse_json(json_url):
    response = requests.get(json_url)
    data = response.json()
    return data
