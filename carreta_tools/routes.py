from flask import render_template, url_for, redirect
from carreta_tools import app, grafico, data


@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')


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
