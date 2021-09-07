from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
login_manager = LoginManager(app)
app.config['SECRET_KEY'] = '4ecd1da2c26abd5fdb366d9c94a95fff'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api_key = '867FB447FE65F77F5377BDAF7EE82E73'

from carreta_tools import routes

