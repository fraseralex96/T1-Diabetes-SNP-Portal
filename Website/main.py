from app import app, db
from models import Variants, Clinical_significance, GO_terms, RAFs
from db_init import Session, init_db
from flask_sqlalchemy import SQLAlchemy


#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///IE5.db'
#db = SQLAlchemy(app)

#create a route decorator 
@app.route('/', methods=['GET', 'POST'])
def index():
	result = Variants.query
	return result.all()

#allows the app to run when called
if __name__=='__main__':
	init_db()
	app.run(debug=True)

