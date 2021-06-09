from flask import render_template, url_for
from carreta_tools import app


@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')


@app.route("/meta")
def meta_page():
    return render_template('meta.html')


@app.route("/meta/hc")
def meta_hc_page():
    return render_template('meta_hc.html')


@app.route("/meta/mid")
def meta_mid_page():
    return render_template('meta_mid.html')


@app.route("/meta/off")
def meta_off_page():
    return render_template('meta_off.html')


@app.route("/meta/sup")
def meta_sup_page():
    return render_template('meta_sup.html')


@app.route("/meta/hsup")
def meta_hsup_page():
    return render_template('meta_hsup.html')
