import celery
from flask import Flask
import flask_monitoringdashboard as dashboard
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_login import login_manager
from flask_mail import Mail, Message
from decouple import config
from na_service.flask_celery import make_celery

app = Flask(__name__)
dashboard.config.init_from(file='/home/honest113/GitHub/NA_project/config.cfg')
dashboard.bind(app)

app.config['SECRET_KEY'] = '08886dd2e696be3767fbd3540fe1a3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['CELERY_BROKER_URL'] = 'redis://0.0.0.0:6379/0'
app.config['result_backend'] = 'db+sqlite:///db.sqlite3'

celery = make_celery(app=app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = config('EMAIL_USER')
app.config['MAIL_PASSWORD'] = config('EMAIL_PASS')
mail = Mail(app)

from na_service.users.routes import users
from na_service.main.routes import main
from na_service.posts.routes import posts

app.register_blueprint(users)
app.register_blueprint(main)
app.register_blueprint(posts)