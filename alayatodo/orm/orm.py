from flask import Flask
from models import db

orm = Flask(__name__)

# load config from the config file we created earlier
orm.config.from_object('config')

# initialize and create the database
db.init_app(orm)
db.create_all(app=orm)

@orm.route('/')
def home():
    return 'hello world'

if __name__ == '__main__':
    orm.run()