from app import app, db
from models import Variants, Clinical_significance, GO_terms, RAFs
from db_init import Session, init_db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///IE9.db'
db = SQLAlchemy(app)
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
engine = create_engine('sqlite:///IE9.db')
Session = scoped_session(sessionmaker(bind=engine))

#create a Base object and assign the query function the output from Session.query_property()
#query_property() creates an object that acts as a factory to construct a query
#with the session we created, by assigning this to the Base.query object we can perform 
#this function with all derivates of Base by using Model.query
Base = declarative_base()
Base.query = Session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    print('Hello')
    Base.metadata.create_all(bind=engine)

#create a route decorator 
@app.route('/', methods=['GET', 'POST'])
def index():
	result = Variants.query
	return result.all()

#allows the app to run when called
if __name__=='__main__':
	init_db()
	app.run(debug=True)

