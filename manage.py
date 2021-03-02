from flaskBlog import db, app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from dotenv import load_dotenv, find_dotenv

db.init_app(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    load_dotenv(find_dotenv())
    manager.run()