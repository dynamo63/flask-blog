import os
class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'CnBIZtOBkzpDYkIWUJ44DuLfDe8PAOO4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Development(BaseConfig):
    DEBUG = True
    ENV = 'dev'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://dynamo74:sabil2000@localhost/flaskBlogData'

class Production(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SECRET_KEY = os.environ.get('SECRET_KEY')