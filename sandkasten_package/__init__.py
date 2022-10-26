from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__, template_folder='templates')
app.secret_key = 'D8MPuw4OF5ZUEQUdsXnsQc79roXLMWNo'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///dbsand.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
manager = LoginManager(app)


from sandkasten_package import models, routes


with app.app_context():
    db.create_all()
