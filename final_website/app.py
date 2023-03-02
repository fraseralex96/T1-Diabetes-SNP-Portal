from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) # create a flask instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database/DB.db' # configure the SQLAlchemy database our DB.db SQLite database


#create an instance of the SQLalchemy class and associate it with our flask app
db = SQLAlchemy(app)
db.init_app(app) # initialise the flask app




