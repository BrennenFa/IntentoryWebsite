from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager



app = Flask(__name__)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

app.config['SECRET_KEY'] = '9202f690fd62852f67ea836e503a6acf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'



from flaskblog import routes
from flaskblog.models import User
