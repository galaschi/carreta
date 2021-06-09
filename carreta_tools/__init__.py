from flask import Flask


app = Flask(__name__)


from carreta_tools import routes

