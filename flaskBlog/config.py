import os
class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Development(BaseConfig):
    DEBUG = True
    ENV = 'dev'
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://dynamo63:#Sabil2000@localhost:3306/flaskBlog'

class Production(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SECRET_KEY = os.environ.get('SECRET_KEY')