#important packages- see requirements.txt for versions
from db_init import session, engine
import pandas as pd
from models import Variants, Clinical_significance, GO_terms, RAFs, Variant_gene_relationship, chr6_GBR_r, chr6_Han_r, chr6_Yoruba_r
import json
import io
import base64
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from ld_plot.ld_plot import ld_plot
import re

####### Join functions ##############################################

#These functions make a join between tables and query these
#They then serialise the objects returned from the query and enforce JSON format

def variantJoin():
	db_session = session() # opens a session between flask and SQLAlchemy database
	results = db_session.query(Variants, RAFs).join(RAFs).all() # SQLAlchemy query
	
	serialised_results = []
	for result in results: # assigns attribute values from the returned objects to dict keys
		row = {
		"variant_name": result.Variants.variant_name, 
		"p_value": result.Variants.p_value,
		"allele": result.Variants.allele,
		"chromosome": result.Variants.chromosome,
		"location_on_chromosome": result.Variants.location_on_chromosome,
		"han_raf": result.RAFs.han_raf,
		"yoruba_raf": result.RAFs.yoruba_raf,
		"gbr_raf": result.RAFs.gbr_raf
		}
		serialised_results.append(row)

	db_session.close() # session must be closed to avoid threading issues with flask
	return serialised_results # JSON file returned 


def variantJoin2():
	db_session = session()
	results = db_session.query(Variants, Variant_gene_relationship, RAFs).join(Variant_gene_relationship, RAFs).all() # variation of the above query
	
	serialised_results = []
	for result in results:
		row = {
		"variant_name": result.Variants.variant_name,
		"p_value": result.Variants.p_value,
		"allele": result.Variants.allele,
		"chromosome": result.Variants.chromosome,
		"location_on_chromosome": result.Variants.location_on_chromosome,
		"gene_name": result.Variant_gene_relationship.gene_name,
		"han_raf": result.RAFs.han_raf,
		"yoruba_raf": result.RAFs.yoruba_raf,
		"gbr_raf": result.RAFs.gbr_raf
		}
		serialised_results.append(row)

	db_session.close()
	return serialised_results


def clinJoin():
	db_session = session()
	query = session.query(Clinical_significance, Variant_gene_relationship.gene_name).join(Variant_gene_relationship, Variant_gene_relationship.variant_name == Clinical_significance.variant_name)
	results = query.all() # .all returns all data from the query in place of a filter

	serialised_results = []
	for i in results:
		clinical_significance, gene_name = i
		row = {
		"variant_name": clinical_significance.variant_name,
		"variant_consequence": clinical_significance.variant_consequence,
		"clinical_significance": clinical_significance.clinical_significance,
		"polyPhen_prediction": clinical_significance.polyPhen_prediction,
		"polyPhen_score": clinical_significance.polyPhen_score,
		"sift_prediction": clinical_significance.sift_prediction,
		"sift_score": clinical_significance.sift_score,
		"gene_name": gene_name,
		}
		serialised_results.append(row)

	db_session.close()
	return serialised_results


def clinJoin2():
	db_session = session()
	results = db_session.query(Variants, Clinical_significance).join(Clinical_significance).all()
	
	serialised_results = []
	for result in results:
		row = {
		"chromosome": result.Variants.chromosome,
		"location_on_chromosome": result.Variants.location_on_chromosome,
		"variant_name": result.Clinical_significance.variant_name,
		"variant_consequence": result.Clinical_significance.variant_consequence,
		"clinical_significance": result.Clinical_significance.clinical_significance,
		"polyPhen_prediction": result.Clinical_significance.polyPhen_prediction,
		"polyPhen_score": result.Clinical_significance.polyPhen_score,
		"sift_prediction": result.Clinical_significance.sift_prediction,
		"sift_score": result.Clinical_significance.sift_score,
		# add more fields as needed
		}
		serialised_results.append(row)

	db_session.close()
	return serialised_results


def goJoin(searchTerm='cellular_component'):
	db_session = session()
	results = db_session.query(GO_terms, Variant_gene_relationship).join(Variant_gene_relationship).filter(GO_terms.go_domain == searchTerm).all()
	
	serialised_results = []
	for result in results:
	    row = {
	    "gene_name": result.GO_terms.gene_name,
	    "go_domain": result.GO_terms.go_domain,
	    "go_term_name": result.GO_terms.go_term_name,
	    "go_term_definition": result.GO_terms.go_term_definition,
	    "go_term_accession": result.GO_terms.go_term_accession,
	    "variant_name": result.Variant_gene_relationship.variant_name,
	    }
	    serialised_results.append(row)

	db_session.close()

  # query returned objects that had the same values for gene_name and all go_ values
  # but differed only in variant_name
  # made it appear on the website tables like there were repeats as variant_name is omitted
	# the below removes repeats
	uniqueList = [] 
	for d in serialised_results:
	  if not any( # checks if a dict with matching gene_name and go_term_accession was already added
	    nd["gene_name"] == d["gene_name"] and nd["go_term_accession"] == d["go_term_accession"]
	    for nd in uniqueList
	    ):
	      uniqueList.append(d) # only adds if there is no matching dict

	return uniqueList


def goJoin2(searchTerm='cellular_component'):
	db_session = session()
	results = db_session.query(Variants, Variant_gene_relationship, GO_terms).join(Variant_gene_relationship, Variant_gene_relationship.variant_name == Variants.variant_name).filter(GO_terms.go_domain == searchTerm).join(GO_terms, GO_terms.gene_name == Variant_gene_relationship.gene_name).all()
	
	serialised_results = []
	for result in results:
		row = {
		"chromosome": result.Variants.chromosome,
		"location_on_chromosome": result.Variants.location_on_chromosome,
		"gene_name": result.GO_terms.gene_name,
		"go_domain": result.GO_terms.go_domain,
		"go_term_name": result.GO_terms.go_term_name,
		"go_term_definition": result.GO_terms.go_term_definition,
		"go_term_accession": result.GO_terms.go_term_accession,
		"variant_name": result.Variant_gene_relationship.variant_name,
		}
		serialised_results.append(row)

	db_session.close()

	uniqueList = []
	for d in serialised_results:
		if not any(
			nd["gene_name"] == d["gene_name"] and nd["go_term_accession"] == d["go_term_accession"]
			for nd in uniqueList
			):
				uniqueList.append(d)

	return uniqueList


# geneJoin allows multiple genes in the variant information table to be represented per variant 
def geneJoin():
	db_session = session()
	results = db_session.query(Variants, Variant_gene_relationship).join(Variant_gene_relationship).all()

	serialised_results = []
	for result in results: # creates a dictionary of all variant and gene relationship in the DB
		row = {
		"variant_name": result.Variants.variant_name,
		"gene_name": result.Variant_gene_relationship.gene_name
		}
		serialised_results.append(row)

	serialised_dict = {} # a new dictionary that has each variant returned above as a key, the value is all associated genes in a list
	for d in serialised_results:
		variant = d['variant_name'] # new variables assigned for the genes and variants returned in the above SQLAlchemy query
		gene = d['gene_name']

		if variant in serialised_dict: # if variant is present already in serialised_dict, gene is appended to the list of genes
			serialised_dict[variant].append(gene)

		else:
			serialised_dict[variant] = [gene] # if variant not present then a list of genes is created as a value for the variant key

	db_session.close()

	return serialised_dict


####### Result functions ##############################################

# These functions take the JSON created in the functions above and package them into lists

def variants(search, rafJSON, geneJSON): # creates data for variant info if the search is a SNP
		l1 = []
		l2 = []
		l3 = []
		l4 = []
		l5 = []
		l6 = []
		l7 = []

		for i in rafJSON:
			if (search in i['variant_name']) is True: # checks data in each JSON dict to see if there is a match with the search
				l1.append(f"{i['variant_name']} - {i['allele']}") # appends data to lists if there is a match between variant_names
				l2.append(i['p_value'])
				l3.append(f"{i['chromosome']}:{i['location_on_chromosome']}")
				l5.append(i['gbr_raf'])
				l6.append(i['han_raf'])	
				l7.append(i['yoruba_raf'])	

		for i in geneJSON:
			if (search == i): # checks if search matches any of the variant_name keys in geneJSON produced by geneJoin
				x = ', '.join(geneJSON[i]) # if there is a match, the list is joined and passed into l4 to be included in the website table
				l4.append(x)

		return [l1,l2,l3,l4,l5,l6,l7]

def variants2(search, variantJSON): # creates data for variant info if the search is a gene
		l1 = []
		l2 = []
		l3 = []
		l4 = []
		l5 = []
		l6 = []
		l7 = []

		for i in variantJSON:
			if (search in i['gene_name']) is True:
				l1.append(f"{i['variant_name']} - {i['allele']}")
				l2.append(i['p_value'])
				l3.append(f"{i['chromosome']}:{i['location_on_chromosome']}")
				l4.append(i['gene_name'])
				l5.append(i['gbr_raf'])
				l6.append(i['han_raf'])	
				l7.append(i['yoruba_raf'])	

		# searches with gene name only returns one gene name per variant so doesn't require the use of geneJoin
		return [l1,l2,l3,l4,l5,l6,l7]

def variants3(variantJSON): # creates data for variant info if the search is chromosome coordinates
		l1 = []
		l2 = []
		l3 = []
		l4 = []
		l5 = []
		l6 = []
		l7 = []

		# chromosome searches produced repeated dictionaries where gene_name is unique but all other values repeated
		# this code checks for this and collates repeated dictionaries into one, with a list for the unique gene names

		variantJSON2 = [] # new JSON file
		for d in variantJSON: # original JSON with repeats

			found = False # variable checking if below loop finds a dictionary in the new JSON matching one from original JSON as it loops through original

			for nd in variantJSON2:

			  if nd["p_value"] == d["p_value"] and nd["variant_name"] == d["variant_name"]: # checks if dict from variantJSON has already been added to variantJSON2
	
			  	if isinstance(nd['gene_name'], list):#checks if there is already a list at 'gene_name'
			  		
			  		nd['gene_name'].append(d['gene_name'])#appends values to this list if there is

			  	else:
			  		nd['gene_name'] = [nd['gene_name'], d['gene_name']] #creates a list if not

			  	found = True 
			  	break

			if not found:
				variantJSON2.append(d) # this adds the dict from the old list to the new list if it is not already present

		for i in variantJSON2: # uses the dict with no repeats
			l1.append(f"{i['variant_name']} - {i['allele']}")
			l2.append(i['p_value'])
			l3.append(f"{i['chromosome']}:{i['location_on_chromosome']}")
			l5.append(i['gbr_raf'])
			l6.append(i['han_raf'])	
			l7.append(i['yoruba_raf'])	

			if isinstance(i['gene_name'], list): # not all records have multiple genes and therefore won't necessarily be in a list
				x = ', '.join(i['gene_name']) # only joins if they are
				l4.append(x)
			else:
				l4.append(i['gene_name']) # otherwise just appends

		return [l1,l2,l3,l4,l5,l6,l7]


def clinSif(search): # creates data for clinical significance table if the search is SNP
		l8 = []
		l9 = []
		l10 = []
		l11 = []
		l12 = []
		l13 = []
		l14 = []

		for i in Clinical_significance.query.all(): # does not need a join so the SQLAlchemy query is called in this function
			if (search in i.variant_name) is True:
				l8.append(i.variant_name)
				l9.append(i.variant_consequence)
				l10.append(i.clinical_significance)
				l11.append(i.polyPhen_prediction)
				l12.append(i.polyPhen_score)
				l13.append(i.sift_prediction)
				l14.append(i.sift_score)

		return [l8,l9,l10,l11,l12,l13,l14]

def clinSif2(search, clinJSON): # creates data for the clinical significance table if the search is a gene
		l8 = []
		l9 = []
		l10 = []
		l11 = []
		l12 = []
		l13 = []
		l14 = []

		for i in clinJSON:
			if (search in i['gene_name']) is True:
				l8.append(i['variant_name'])
				l9.append(i['variant_consequence'])
				l10.append(i['clinical_significance'])
				l11.append(i['polyPhen_prediction'])
				l12.append(i['polyPhen_score'])
				l13.append(i['sift_prediction'])
				l14.append(i['sift_score'])

		return [l8,l9,l10,l11,l12,l13,l14]

def clinSif3(clinJSON): # creates data for the clinical significance table if the search is chromosome coordinates
		l8 = []
		l9 = []
		l10 = []
		l11 = []
		l12 = []
		l13 = []
		l14 = []

		for i in clinJSON:
			l8.append(i['variant_name'])
			l9.append(i['variant_consequence'])
			l10.append(i['clinical_significance'])
			l11.append(i['polyPhen_prediction'])
			l12.append(i['polyPhen_score'])
			l13.append(i['sift_prediction'])
			l14.append(i['sift_score'])

		return [l8,l9,l10,l11,l12,l13,l14]

def goTerms(search, goJSON, searchTerm): # creates data for the gene ontology table if the search is either gene or SNP
		l15 = []
		l16 = []
		l17 = []
		l18 = []
		l19 = []

		for i in goJSON:
			if (search in i[searchTerm]) is True: # search term differentiates between searches for SNP and gene
				l15.append(i['gene_name'])
				l16.append(i['go_domain'])
				l17.append(i['go_term_name'])
				l18.append(i['go_term_definition'])
				l19.append(i['go_term_accession'])

		return [l15,l16,l17, l18, l19]

def goTerms2(goJSON): # creates data for gene ontology table if the search is chromosome coordinates
		l15 = []
		l16 = []
		l17 = []
		l18 = []
		l19 = []		

		for i in goJSON:
			l15.append(i['gene_name'])
			l16.append(i['go_domain'])
			l17.append(i['go_term_name'])
			l18.append(i['go_term_definition'])
			l19.append(i['go_term_accession'])

		return [l15,l16,l17,l18,l19]

####### Range Maker function ##########################################

# This function takes the minimum and maximum values for chromosome search
# It then turns uses it to refine JSON data returned by Join functions so it 
# is within this range

def rangeMaker(cMin, cMax, JSON): # cMin and cMax are the search variables from /search/chromosome
  cMin = cMin.split(":") # splits chromosome and location values either side of ':'
  cMax = cMax.split(":")

  r1 = list(range(int(cMin[0]), (int(cMax[0])+1))) # takes chromosome values and makes them into a range
  r2 = [[r1[0]], r1[1:-1], [r1[-1]]] # splits this range into three lists which will have different filters applied

  # new data structures for later on in the code
  newJSON2 = [[], [], []]
  newJSON3 = []

  #first layer of filtering- chromosome filter
  newJSON1 = [x for x in JSON if x['chromosome'] in r1] # adds objects to newJSON1 if the chromosome number is in the search range
  
  #second layer of filtering- nested lists
  for obj in newJSON1:
    if obj['chromosome'] == r1[0]: # check if chromosome in obj matches the first in the range 
      newJSON2[0].append(obj) # add to first list of newJSON2

    elif obj['chromosome'] == r1[-1]: # check if chromosome in obj matches the last in the range 
      newJSON2[2].append(obj) # add to last list of newJSON2

    else:
      newJSON2[1].append(obj) # add all middle ones to the middle list in newJSON2

  #third layer of filtering- location filter
  if (len(newJSON2[0])>0) and (len(newJSON2[2])>0): # performs below code when chromosome search spans 2 or more chromosomes
    for i in range(len(newJSON2[0])-1, -1, -1): # removes everything in newJSON2 first list that is lower than min location value
      if newJSON2[0][i]['location_on_chromosome'] < int(cMin[1]):
        del newJSON2[0][i] 

    for i in range(len(newJSON2[2])-1, -1, -1): # removes everything in newJSON2 last list that is higher than max location value
      if newJSON2[2][i]['location_on_chromosome'] > int(cMax[1]):
        del newJSON2[2][i]

  elif (len(newJSON2[0])>0) and (len(newJSON2[2])==0): # performs below code when chromosome search spans one chromosome
    for i in range(len(newJSON2[0])-1, -1, -1): # only newJSON2[0] is populated with data in these instances
      if not int(cMin[1]) <= newJSON2[0][i]['location_on_chromosome'] <= int(cMax[1]): # removes data where location is not in the min-max range
        del newJSON2[0][i]

  for l in newJSON2: # joins all data from three lists into one final list newJSON3
    newJSON3.extend(l)

  return newJSON3

####### LD graph functions #############################################

#The functions below are required to produce the linkage disequilibrium plot

def ldSearch(ld, searchTerm): # returns a dictionary for all data present 
	with engine.connect() as conn: # creates a SQLAlchemy engine
		result = conn.execute(searchTerm.select()) # connects to the database and searches for all LD data based on searchTerm
		
		# below code serialises the results similar to in the Join functions
		rows = [dict(row) for row in result]
		serialised_rows = json.dumps(rows)
		deserialised_rows = json.loads(serialised_rows)

		conn.close() # close connection- important!

	newResults = []
	for i in deserialised_rows: # filters for ld values that have rs_values matching checkboxes selected
		if i['rs_value'] in ld:
			newResults.append(i)

	# below code formats the data into nested dicts
	# outer dict (dict1) has keys for each rs value from the checkboxes selected for ld 
	# one inner dict (dict2) exists as a value per rs value key in dict1 and it shows the 
	# LD values calculated for that rs value key and the other rs values in ld
	dict1 = {}
	for obj in newResults: # iterate through ld results, one obj per rs_value row in the SQL matrix
		rs_value = obj['rs_value'] # save the rs_value for this obj to make set as a dict1 key
		dict2 = {} # create a dict2 for this obj
		for key, value in obj.items(): # separate obj to access rs_values
			if key in ld: # only return the keys if they're selected by checkboxes
				dict2[key] = value # add the keys (rs values) and values (LD score) to dict2
		dict1[rs_value] = dict2 # assign dict1 a key and value

	return dict1

def dictMaker(ld, pop): # performs the above ldSearch depending on which population is selected
	if pop == 'British':
		ldJSON = ldSearch(ld, chr6_GBR_r) # chr6_GBR_r is the SQL table and searchTerm above
		return ldJSON

	if pop == 'Han Chinese':
		ldJSON = ldSearch(ld, chr6_Han_r)
		return ldJSON

	if pop == 'Yoruba':
		ldJSON = ldSearch(ld, chr6_Yoruba_r)
		return ldJSON

def dfMaker(ld_dict): # turns the dictionary produced by ldSearch into a df
	df = pd.DataFrame.from_dict(ld_dict)
	return df

def plotMaker(df): # creates a heatmap plot based using ld_plot- https://github.com/NikKonst/ld_plot
	n = df.columns.values # x axis labels
	fig = ld_plot(ld=df, labels=n) # plot the figure
	plt.xticks(fontsize=7) # set font size of x axis labels

	# encodes graph in a format that can be added to HTML template 
	buffer = io.BytesIO() # creates a buffer object
	fig.savefig(buffer, format='png') # save the plot to buffer in PNG format
	buffer.seek(0) # reset position of buffer to beginning of the file
	plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8') # encode the plot in base64
	return plot_data

####### data-type-check functions ######################################


#creates a list of genes that will be used for the below function
geneList = []
for i in GO_terms.query.all(): # genes are based on all genes in GO_terms in SQL DB
	if i.gene_name in geneList:
		pass
	else:
		geneList.append(i.gene_name)

def geneCheck(search): # checks if gene searched in search bar is present in DB
	if geneList.count(search)>0:
		return True
	else: 
		return False

def rsCheck(search): # regex that checks if the re_value SNP search begins with rs
	rgx = re.compile(r"^rs\d*")
	if rgx.search(search):
		return True
	else:
		return False

# creates a list of all rs values in ld matrices to catch errors when plotting ld
rsList=[]

with engine.connect() as conn:
	# #query database and serialise data
  result = conn.execute(chr6_GBR_r.select())
  rows = [dict(row) for row in result]
  serialised_rows = json.dumps(rows)
  deserialised_rows = json.loads(serialised_rows)

  conn.close() #close connection- important!

for key, value in deserialised_rows[1].items(): # appends all keys (rs_values)
  rsList.append(key)


# counts number of rs values in ld that are present in rsList
def ldCheck(ld):  
	count = 0 # uses this count 
	for i in ld:
		if i in rsList:
			count+=1
		else:
			pass
	return count # count then affects what happens when ld plot submit button is pressed on results page