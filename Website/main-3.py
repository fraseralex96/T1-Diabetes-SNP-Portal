from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import mapper

# Config
DB_NAME = 'sqlite:///test4.db'

# Create DB
engine = create_engine(DB_NAME)
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return f'<User {self.name!r}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
            }

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    Base.metadata.create_all(bind=engine)

# CREATE APP
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_NAME
db = SQLAlchemy(app)

#create a route decorator 
@app.route('/', methods=['GET', 'POST'])
def index():
    users = User.query.all()
    return jsonify(eqtls=[e.serialize() for e in users])

# Main

init_db()
app.run(debug=True)


# INSERT INTO Variants VALUES(1, "Micah")