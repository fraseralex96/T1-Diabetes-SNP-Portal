#important packages- see requirements.txt for versions
from app import app
from models import *
from functions import *
from db_init import init_db, session, engine
from flask import Flask, jsonify, redirect, url_for, render_template, request, send_file, make_response
import rpy2
import rpy2.robjects as robjects
from rpy2.rinterface_lib.embedded import RRuntimeError
import json
import io

#####################################################################

#rpy2 object that allows R code to be executed in Python
r = robjects.r
r.source("manfunction.R") #connects to manhattan plot function 'manfunction.R'
r('using')("manhattanly") # installs the manhattanly package

####### Home Page ###################################################

@app.route('/', methods = ['GET', 'POST'])
def index():
	return render_template('homepage.html')

####### About Page ##################################################

@app.route('/about')
def about():
	return render_template('about_page.html')

####### SNP search ##################################################

@app.route('/search/SNP')
def snpSearch():
	return render_template('snp.html')

@app.route('/result/SNP', methods=['GET', 'POST'])
def snpSearchResult():
	if request.method == 'POST' and ('snpname' in request.form): # checks if the POST request is from the searchbar variable 'snpname'
		global search, x, y # global variables are required to render the HTML template when the POST reqeust is from 'GO'
		search = request.form.get('snpname')
		r = rsCheck(search) # rsCheck checks if the search variable starts with 'rs'

		if r==True:
			# functions called below assigned to *JSON variables query the database and return JSON
			# functions called below assigned x, y, z convert JSON format data into lists to be passed into the HTML template
			rafJSON = variantJoin() 
			geneJSON = geneJoin()
			x = variants(search, rafJSON, geneJSON)
			y = clinSif(search)
			goJSON = goJoin()
			z = goTerms(search, goJSON, 'variant_name')
			
			#manhattan plot 
			highlight_snps=y[0] # SNPs highlighted in the plot
			r = robjects.r 
			r.source("manfunction.R")
			r('man_function')(highlight_snps) # calls the specific plot 

			return render_template('snpResult.html', option=None, search = search, count = len(x[0]), # renders the homepage template assigning values in the x,y,z lists to new variables
				result1=x[0], result2=x[1], result3=x[2], result4=x[3], 
				result5=x[4], result6=x[5], result7=x[6], count2 = len(y[0]),
				result8=y[0],result9=y[1], result11=y[2], result10=y[3],
				result12=y[4], result13=y[5], result14=y[6], count3 = len(z[0]),
				result15=z[0], result16=z[1], result17=z[2], result18=z[3], result19=z[4]
				)

		else:
			return redirect(url_for('noResult')) # noResult template returned if 'rs' is not found in the search

	elif request.method == 'POST' and ('GO' in request.form): # check if the POST request is from the Gene Ontology dropdown list
		option = request.form.get('GO')
		goJSON = goJoin(option) # GO_terms table is remade with the dropdown list option
		z = goTerms(search, goJSON, 'variant_name')

		highlight_snps=y[0]
		r = robjects.r
		r.source("manfunction.R")
		r('man_function')(highlight_snps)

		return render_template('snpResult.html', option=option, search = search, count = len(x[0]), 
			result1=x[0], result2=x[1], result3=x[2], result4=x[3],
			result5=x[4], result6=x[5], result7=x[6], count2 = len(y[0]),
			result8=y[0],result9=y[1], result11=y[2], result10=y[3],
			result12=y[4], result13=y[5], result14=y[6], count3 = len(z[0]),
			result15=z[0], result16=z[1], result17=z[2], result18=z[3], result19=z[4]
			)		

####### gene search #################################################

@app.route('/search/gene')
def geneSearch():
	return render_template('gene.html')

@app.route('/result/gene', methods=['GET', 'POST'])
def geneSearchResult():
	if request.method == 'POST' and ('genename' in request.form):
		global search, x, y
		search = request.form.get('genename') # checks if the POST request is from the searchbar variable 'genename'
		g = geneCheck(search) # geneCheck checks if search variable is a valid gene name

		if g==True:
			option = request.form.get('GO')
			variantJSON = variantJoin2()
			x = variants2(search, variantJSON)
			clinJSON = clinJoin()
			y = clinSif2(search, clinJSON)
			goJSON = goJoin()
			z = goTerms(search, goJSON, 'gene_name')

			highlight_snps=y[0]
			r = robjects.r
			r.source("manfunction.R")
			r('man_function')(highlight_snps)

			return render_template('geneResult.html', option=None, search = search, count = len(x[0]), # prior to the gene ontology checkbox request option=None 
				result1=x[0], result2=x[1], result3=x[2], result4=x[3],
				result5=x[4], result6=x[5], result7=x[6], count2 = len(y[0]),
				result8=y[0],result9=y[1], result11=y[2], result10=y[3],
				result12=y[4], result13=y[5], result14=y[6], count3 = len(z[0]),
				result15=z[0], result16=z[1], result17=z[2], result18=z[3], result19=z[4])

		else:
			return redirect(url_for('noResult'))

	elif request.method == 'POST' and ('GO' in request.form):
		option = request.form.get('GO')
		goJSON = goJoin(option)
		z = goTerms(search, goJSON, 'gene_name')

		highlight_snps=y[0]
		r = robjects.r
		r.source("manfunction.R")
		r('man_function')(highlight_snps)

		return render_template('geneResult.html', option=option, search = search, count = len(x[0]), # option passes into the template to alter checkbox default value once request has been sent
			result1=x[0], result2=x[1], result3=x[2], result4=x[3],
			result5=x[4], result6=x[5], result7=x[6], count2 = len(y[0]),
			result8=y[0],result9=y[1], result11=y[2], result10=y[3],
			result12=y[4], result13=y[5], result14=y[6], count3 = len(z[0]),
			result15=z[0], result16=z[1], result17=z[2], result18=z[3], result19=z[4])

####### chromosome search ###########################################

@app.route('/search/chromosome')
def chromoSearch():
	return render_template('chromo.html')

@app.route('/result/chromosome', methods=['GET', 'POST'])
def chromoSearchResult():
	if request.method == 'POST' and ('chromoloc1' in request.form): # checks if the POST request is from the searchbar variable 'chromoloc1'
		global cMax, cMin, x, y, query
		cMin = request.form.get('chromoloc1') # two request variables are produced from two entry bars
		cMax = request.form.get('chromoloc2')

		variantJSON = variantJoin2()
		query = f'{cMin} - {cMax}' # query range is set to be passed into the top of the result template
		variantJSON2 = rangeMaker(cMin, cMax, variantJSON) # rangeMaker takes JSON and filters out locations that aren't included in the search range
		x = variants3(variantJSON2)

		clinJSON = clinJoin2()
		clinJSON2 = rangeMaker(cMin, cMax, clinJSON)
		y = clinSif3(clinJSON2)

		goJSON = goJoin2()
		goJSON2 = rangeMaker(cMin, cMax, goJSON)
		z = goTerms2(goJSON2)

		highlight_snps=y[0]
		r = robjects.r
		r.source("manfunction.R")
		r('man_function')(highlight_snps)

		return render_template('chromoResult.html', option = None, search = query, count = len(x[0]), 
			result1=x[0], result2=x[1], result3=x[2], result4=x[3],
			result5=x[4], result6=x[5], result7=x[6], count2 = len(y[0]),
			result8=y[0],result9=y[1], result11=y[2], result10=y[3],
			result12=y[4], result13=y[5], result14=y[6], count3 = len(z[0]),
			result15=z[0], result16=z[1], result17=z[2], result18=z[3], result19=z[4]) 

	elif request.method == 'POST' and ('GO' in request.form):
		option = request.form.get('GO')
		goJSON = goJoin2(option)
		goJSON2 = rangeMaker(cMin, cMax, goJSON)
		z = goTerms2(goJSON2)

		highlight_snps=y[0]
		r = robjects.r
		r.source("manfunction.R")
		r('man_function')(highlight_snps)

		return render_template('chromoResult.html', option=option, search = query, count = len(x[0]), 
			result1=x[0], result2=x[1], result3=x[2], result4=x[3],
			result5=x[4], result6=x[5], result7=x[6], count2 = len(y[0]),
			result8=y[0],result9=y[1], result11=y[2], result10=y[3],
			result12=y[4], result13=y[5], result14=y[6], count3 = len(z[0]),
			result15=z[0], result16=z[1], result17=z[2], result18=z[3], result19=z[4]) 

####### downloads ###################################################

@app.route('/download/')
def download():
	return render_template('download.html')

@app.route('/download/<file>')
def download_file(file): # takes a file name variable from the downloads template
	return send_file(file, as_attachment=True) #send_file creates a download for the file name

####### main search #################################################

@app.route('/result', methods=['GET', 'POST'])
def result():
	if request.method == 'POST' and ('SEARCH' in request.form): # checks POST comes from main search bar
		global search
		search = request.form.get('SEARCH')
		r = rsCheck(search)
		g = geneCheck(search)

		if r==True:
			rafJSON = variantJoin()
			geneJSON = geneJoin()
			x = variants(search, rafJSON, geneJSON)
			y = clinSif(search)
			goJSON = goJoin()
			z = goTerms(search, goJSON, 'variant_name')

			highlight_snps=y[0]
			r = robjects.r
			r.source("manfunction.R")
			r('man_function')(highlight_snps)

			return render_template('result.html', option = None, search = search, count = len(x[0]), 
				result1=x[0], result2=x[1], result3=x[2], result4=x[3],
				result5=x[4], result6=x[5], result7=x[6], count2 = len(y[0]),
				result8=y[0],result9=y[1], result11=y[2], result10=y[3],
				result12=y[4], result13=y[5], result14=y[6], count3 = len(z[0]),
				result15=z[0], result16=z[1], result17=z[2], result18=z[3], result19=z[4]
				)

		if g==True:
			variantJSON = variantJoin2()
			x = variants2(search, variantJSON)
			clinJSON = clinJoin()
			y = clinSif2(search, clinJSON)
			goJSON = goJoin()
			z = goTerms(search, goJSON, 'gene_name')

			highlight_snps=y[0]
			r = robjects.r
			r.source("manfunction.R")
			r('man_function')(highlight_snps)

			return render_template('result.html', option=None, search = search, count = len(x[0]), 
				result1=x[0], result2=x[1], result3=x[2], result4=x[3],
				result5=x[4], result6=x[5], result7=x[6], count2 = len(y[0]),
				result8=y[0],result9=y[1], result11=y[2], result10=y[3],
				result12=y[4], result13=y[5], result14=y[6], count3 = len(z[0]),
				result15=z[0], result16=z[1], result17=z[2], result18=z[3], result19=z[4])
		
		else:
			return redirect(url_for('noResult'))	

	elif request.method == 'POST' and ('GO' in request.form):
		option = request.form.get('GO')
		r = rsCheck(search)
		g = geneCheck(search)

		if r==True:
			rafJSON = variantJoin()
			geneJSON = geneJoin()
			x = variants(search, rafJSON, geneJSON)
			y = clinSif(search)
			goJSON = goJoin(option)
			z = goTerms(search, goJSON, 'variant_name')

			highlight_snps=y[0]
			r = robjects.r
			r.source("manfunction.R")
			r('man_function')(highlight_snps)

			return render_template('result.html', option = option, search = search, count = len(x[0]), 
				result1=x[0], result2=x[1], result3=x[2], result4=x[3],
				result5=x[4], result6=x[5], result7=x[6], count2 = len(y[0]),
				result8=y[0],result9=y[1], result11=y[2], result10=y[3],
				result12=y[4], result13=y[5], result14=y[6], count3 = len(z[0]),
				result15=z[0], result16=z[1], result17=z[2], result18=z[3], result19=z[4]
				)

		if g==True:
			variantJSON = variantJoin2()
			x = variants2(search, variantJSON)
			clinJSON = clinJoin()
			y = clinSif2(search, clinJSON)
			goJSON = goJoin(option)
			z = goTerms(search, goJSON, 'gene_name')

			highlight_snps=y[0]
			r = robjects.r
			r.source("manfunction.R")
			r('man_function')(highlight_snps)

			return render_template('result.html', option = option, search = search, count = len(x[0]), 
				result1=x[0], result2=x[1], result3=x[2], result4=x[3],
				result5=x[4], result6=x[5], result7=x[6], count2 = len(y[0]),
				result8=y[0],result9=y[1], result11=y[2], result10=y[3],
				result12=y[4], result13=y[5], result14=y[6], count3 = len(z[0]),
				result15=z[0], result16=z[1], result17=z[2], result18=z[3], result19=z[4])

####### Linkage disequilibrium ######################################

@app.route('/result/LD', methods=['GET', 'POST'])
def resultLD():
	if request.method == 'POST': 
		global df # global dataframe variable needed for the download_file1 function 
		pop = request.form.get('population') # population dropdown POST request
		ld = request.form.getlist('ld') # rs value checkbox POST request
		count = ldCheck(ld) # ldCheck returns a count of the number of rs values in 'ld' that are represented in the linkage disequilibrium database

		if count>1: # count is relevant for error messages
			d = dictMaker(ld, pop) # returns the LD data from the SQL database as a dictionary
			df = dfMaker(d) # produces a pandas dataframe from the dict
			plot_data = plotMaker(df) # produces a heatmap to be passed into the template
			return render_template('LD.html', plot_url=plot_data, ld=ld, count=count)

		else: # returns an error message for insufficient data
			return render_template('LD.html', plot_url=None, ld=ld, count=count)

@app.route('/downloadLD')
def download_file1(): 
	global df
	table_string = df.to_csv(sep='\t') # writes the dataframe to a string
	buffer = io.StringIO(table_string) # Create a file-like buffer and write the string to it
	buffer.seek(0) 	# Set the buffer's position to the beginning of the file
	response = make_response(buffer.getvalue()) # Create a response object that will return the file
	response.headers.set('Content-Disposition', 'attachment', filename='ld.txt') # Set the appropriate headers to trigger a file download
	response.headers.set('Content-Type', 'text/plain')
	return response

####### No result error message #####################################

@app.route('/noResult')
def noResult():
	return render_template('no_result.html')	

####### resources page ##############################################		

@app.route('/resources')
def resources():
	return render_template('resources_page.html')

#allows the app to run when called
if __name__=='__main__':
	init_db()
	app.run(debug=True)

