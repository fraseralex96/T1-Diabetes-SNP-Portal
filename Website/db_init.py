from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#create an instance of an engine
#then create a session object 
engine = create_engine('sqlite:///IE5.db')
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
    Base.metadata.create_all(bind=engine)