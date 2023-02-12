from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///IE9.db'
# initialize the app with the extension
db.init_app(app)


class Variants(db.Model):
    __tablename__ = 'Variants'

    Variant_ID = db.Column('Variant_ID', db.Integer, primary_key = True)
    Variant_name = db.Column('Variant_name', db.String)
    P_Value = db.Column('P_value', db.Float)
    Chromosome = db.Column('Chromosome', db.Integer)
    Location_On_Chromosome= db.Column('Location_on_chromosome', db.Integer)

#create an instance of an engine
#then create a session object 
engine = create_engine('sqlite:///IE9.db', echo=True)
Session = scoped_session(sessionmaker(bind=engine))

#create a Base object and assign the query function the output from Session.query_property()
#query_property() creates an object that acts as a factory to construct a query
#with the session we created, by assigning this to the Base.query object we can perform 
#this function with all derivates of Base by using Model.query
Base = declarative_base()
Base.query = Session.query_property()

Base.metadata.create_all(engine)


# #create a route decorator 
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     result = Variants.query.all()
#     return result

# #allows the app to run when called
# if __name__=='__main__':
#     init_db()
#     app.run(debug=True)
