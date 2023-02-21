from flask import Flask, render_template
import rpy2
import rpy2.robjects as robjects
from rpy2.rinterface_lib.embedded import RRuntimeError





app = Flask(__name__)

#installs manhattanly package if required
r = robjects.r
r.source("manfunction.R")
r('using')("manhattanly")






@app.route("/")
def hello_world():

	#list of snps that need to be highlighted
	highlight_snps=["rs1770"]

	#call manhattan plot function including argument to highlight specific snps
	r = robjects.r
	r.source("manfunction.R")
	r('man_function')(highlight_snps)

	
	return render_template('results.html')



if __name__=='__main__':
	app.run(debug=True)