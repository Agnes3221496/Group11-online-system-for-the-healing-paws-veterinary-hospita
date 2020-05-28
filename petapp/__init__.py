import smtplib
import sys,importlib

from flask_mail import Mail, Message

importlib.reload(sys)

from flask import Flask
from petapp.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
babel = Babel(app)


# MAIL_USE_TLS:端口号587
# MAIL_USE_SSL:端口号465
# QQ邮箱不支持非加密方式发送邮件
app.config['MAIL_SERVER'] = "smtp.126.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "shenlingwudi@126.com"
app.config['MAIL_PASSWORD'] = "IFTWTAGYADBJUVYP"
app.config['MAIL_DEFAULT_SENDER'] = '2724747876@qq.com'
mail = Mail(app)


from petapp import routes, models

