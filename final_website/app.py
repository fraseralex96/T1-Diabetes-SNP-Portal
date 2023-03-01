from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#create a flask instance
app = Flask(__name__)
#configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database/DB.db'

#create an instance of the SQLalchemy class and associate it with our flask app
db = SQLAlchemy(app)
db.init_app(app)




