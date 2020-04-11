from flask import Flask
from petapp.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
babel = Babel(app)

from petapp import routes, models

