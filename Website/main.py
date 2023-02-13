from app import app
from models import Variants
from db_init import init_db
from flask import Flask, jsonify


#create a route decorator 
@app.route('/', methods=['GET', 'POST'])
def index():
	result = Variants.query.all()
	return jsonify(results=[e.serialize() for e in result])

#allows the app to run when called
if __name__=='__main__':
	init_db()
	app.run(debug=True)

