'''
Manage DB configuration and setup module
'''
# standard library
import os
import json

# 3rd party libraries
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# locals
from app import app, db


app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
