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

r = robjects.r
r.source("manfunction.R")
r('using')("manhattanly")

@app.route('/', methods = ['GET', 'POST'])
def index():
	#qry = db_session.query(GO_terms, Variant_gene_relationship).filter(GO_terms.gene_name == Variant_gene_relationship.gene_name).all()
	#return jsonify(results=[e.serialize() for e in qry])
	return render_template('homepage.html')

@app.route('/about')
def about():
	return render_template('about_page.html')

@app.route('/search/SNP')
def snpSearch():
	return render_template('snp.html')

@app.route('/result/SNP', methods=['GET', 'POST'])
def snpSearchResult():
	if request.method == 'POST' and ('snpname' in request.form):
		global search, x, y
		search = request.form.get('snpname')
		r = rsCheck(search)
		if r==True:
			rafJSON = variantJoin()
			geneJSON = geneJoin()
			x = variants(search, rafJSON, geneJSON)
			y = clinSif(search)
			goJSON = goJoin()
			z = goTerms(search, goJSON, 'variant_name')
			#list of snps that need to be highlighted
			highlight_snps=y[0]
			#call manhattan plot function including argument to highlight specific snps
			r = robjects.r
			r.source("manfunction.R")
			r('man_function')(highlight_snps)
			return render_template('snpResult.html', option=None, search = search, count = len(x[0]), 
				result1=x[0], result2=x[1], result3=x[2], result4=x[3],
				result5=x[4], result6=x[5], result7=x[6], count2 = len(y[0]),
				result8=y[0],result9=y[1], result11=y[2], result10=y[3],
				result12=y[4], result13=y[5], result14=y[6], count3 = len(z[0]),
				result15=z[0], result16=z[1], result17=z[2], result18=z[3], result19=z[4]
				)
		else:
			return redirect(url_for('noResult'))	
	elif request.method == 'POST' and ('GO' in request.form):
		option = request.form.get('GO')
		goJSON = goJoin(option)
		z = goTerms(search, goJSON, 'variant_name')
		#list of snps that need to be highlighted
		highlight_snps=y[0]
		#call manhattan plot function including argument to highlight specific snps
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

@app.route('/search/gene')
def geneSearch():
	return render_template('gene.html')

@app.route('/result/gene', methods=['GET', 'POST'])
def geneSearchResult():
	if request.method == 'POST' and ('genename' in request.form):
		global search, x, y
		search = request.form.get('genename')
		g = geneCheck(search)
		if g==True:
			option = request.form.get('GO')
			variantJSON = variantJoin2()
			x = variants2(search, variantJSON)
			clinJSON = clinJoin()
			y = clinSif2(search, clinJSON)
			goJSON = goJoin()
			z = goTerms(search, goJSON, 'gene_name')
			#list of snps that need to be highlighted
			highlight_snps=y[0]
			#call manhattan plot function including argument to highlight specific snps
			r = robjects.r
			r.source("manfunction.R")
			r('man_function')(highlight_snps)
			return render_template('geneResult.html', option=None, search = search, count = len(x[0]), 
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
		#list of snps that need to be highlighted
		highlight_snps=y[0]
		#call manhattan plot function including argument to highlight specific snps
		r = robjects.r
		r.source("manfunction.R")
		r('man_function')(highlight_snps)
		return render_template('geneResult.html', option=option, search = search, count = len(x[0]), 
			result1=x[0], result2=x[1], result3=x[2], result4=x[3],
			result5=x[4], result6=x[5], result7=x[6], count2 = len(y[0]),
			result8=y[0],result9=y[1], result11=y[2], result10=y[3],
			result12=y[4], result13=y[5], result14=y[6], count3 = len(z[0]),
			result15=z[0], result16=z[1], result17=z[2], result18=z[3], result19=z[4])

@app.route('/search/chromosome')
def chromoSearch():
	return render_template('chromo.html')

@app.route('/result/chromosome', methods=['GET', 'POST'])
def chromoSearchResult():
	if request.method == 'POST' and ('chromoloc1' in request.form):
		global cMax, cMin, x, y, query
		cMin = request.form.get('chromoloc1')
		cMax = request.form.get('chromoloc2')
		variantJSON = variantJoin2()
		query = f'{cMin} - {cMax}'
		variantJSON2 = rangeMaker(cMin, cMax, variantJSON)
		x = variants3(variantJSON2)
		clinJSON = clinJoin2()
		clinJSON2 = rangeMaker(cMin, cMax, clinJSON)
		y = clinSif3(clinJSON2)
		goJSON = goJoin2()
		goJSON2 = rangeMaker(cMin, cMax, goJSON)
		z = goTerms2(goJSON2)
		#list of snps that need to be highlighted
		highlight_snps=y[0]
		#call manhattan plot function including argument to highlight specific snps
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
		#list of snps that need to be highlighted
		highlight_snps=y[0]
		#call manhattan plot function including argument to highlight specific snps
		r = robjects.r
		r.source("manfunction.R")
		r('man_function')(highlight_snps)
		return render_template('chromoResult.html', option=option, search = query, count = len(x[0]), 
			result1=x[0], result2=x[1], result3=x[2], result4=x[3],
			result5=x[4], result6=x[5], result7=x[6], count2 = len(y[0]),
			result8=y[0],result9=y[1], result11=y[2], result10=y[3],
			result12=y[4], result13=y[5], result14=y[6], count3 = len(z[0]),
			result15=z[0], result16=z[1], result17=z[2], result18=z[3], result19=z[4]) 

	#return render_template('result.html')
 
@app.route('/download/')
def download():
	return render_template('download.html')

@app.route('/download/<file>')
def download_file(file):
	f = f'database\\data\\{file}'
	return send_file(f, as_attachment=True)

@app.route('/result', methods=['GET', 'POST'])
def result():
	if request.method == 'POST' and ('SEARCH' in request.form):
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
			#list of snps that need to be highlighted
			highlight_snps=y[0]
			#call manhattan plot function including argument to highlight specific snps
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
			#list of snps that need to be highlighted
			highlight_snps=y[0]
			#call manhattan plot function including argument to highlight specific snps
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
			#list of snps that need to be highlighted
			highlight_snps=y[0]
			#call manhattan plot function including argument to highlight specific snps
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
			#list of snps that need to be highlighted
			highlight_snps=y[0]
			#call manhattan plot function including argument to highlight specific snps
			r = robjects.r
			r.source("manfunction.R")
			r('man_function')(highlight_snps)
			return render_template('result.html', option = option, search = search, count = len(x[0]), 
				result1=x[0], result2=x[1], result3=x[2], result4=x[3],
				result5=x[4], result6=x[5], result7=x[6], count2 = len(y[0]),
				result8=y[0],result9=y[1], result11=y[2], result10=y[3],
				result12=y[4], result13=y[5], result14=y[6], count3 = len(z[0]),
				result15=z[0], result16=z[1], result17=z[2], result18=z[3], result19=z[4])
@app.route('/result/LD', methods=['GET', 'POST'])
def resultLD():
	if request.method == 'POST':
		global df
		pop = request.form.get('population')
		ld = request.form.getlist('ld')
		if (len(ld) > 0):
			d = dictMaker(ld, pop)
			df = dfMaker(d)
			plot_data = plotMaker(df)
			return render_template('LD.html', plot_url=plot_data, ld=ld)
		else:
			return render_template('LD.html', plot_url=None, ld=ld)

@app.route('/downloadLD')
def download_file1():
	global df
	table_string = df.to_csv(sep='\t')
	# Create a file-like buffer and write the string to it
	buffer = io.StringIO(table_string)
	#Set the buffer's position to the beginning of the file
	buffer.seek(0)
	# Create a response object that will return the file
	response = make_response(buffer.getvalue())
	# Set the appropriate headers to trigger a file download
	response.headers.set('Content-Disposition', 'attachment', filename='ld.txt')
	response.headers.set('Content-Type', 'text/plain')
	return response

@app.route('/noResult')
def noResult():
	return render_template('no_result.html')			

@app.route('/resources')
def resources():
	return render_template('resources_page.html')

#allows the app to run when called
if __name__=='__main__':
	init_db()
	app.run(debug=True)

