from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

DB_NAME = 'sqlite:///test2.db'

# Create DB
engine = create_engine(DB_NAME)
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

class Variants(Base):
    __tablename__ = 'Variants'

    id = Column('Variant_ID', Integer, primary_key = True)
    name = Column('Variant_name', String)
    # P_Value = Column('P_value', Float)
    # Chromosome = Column('Chromosome', Integer)
    # Location_On_Chromosome = Column('Location_on_chromosome', Integer)

    def __init__(self, name=None, id=None):
        self.id = id    
        self.name = name

    def __repr__(self):
        return f'<Variant {self.name!r}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
            }

def init_db():
    Base.metadata.create_all(bind=engine)


# CREATE APP
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_NAME
db = SQLAlchemy(app)

#create a route decorator 
@app.route('/', methods=['GET', 'POST'])
def index():
	result = Variants.query.all()
	return jsonify(results=[e.serialize() for e in result])

# Main

init_db()
app.run(debug=True)
