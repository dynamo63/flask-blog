import pymysql
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from .config import Development, Production
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config.from_object(Production() if os.environ.get('ENV') == 'production' else Development())
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# import utils functions
from .utils import *
# Add Forms 
from flaskBlog import forms

# Add Model 
from flaskBlog import models
from flaskBlog import routes