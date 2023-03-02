from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///./database/DB.db', convert_unicode=True) # create an instance of an engine
session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False)) # then create a session object 

#create a Base object and assign the query function the output from Session.query_property()
#query_property() creates an object that acts as a factory to construct a query
#with the session we created, by assigning this to the Base.query object we can perform 
#this function with all derivates of Base by using Model.query
Base = declarative_base()
Base.query = session.query_property()

#create a Metadata object to be used to map tables below and to reflect the matrix tables found at the bottom of models.py 
metadata = MetaData()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata. Otherwise
    # you will have to import them first before calling init_db()
    import models # import models to be mapped
    Base.metadata.create_all(bind=engine) # creates a mapping of the tables based on our models