from db_init import session, engine
import pandas as pd
from models import Variants, Clinical_significance, GO_terms, RAFs, Variant_gene_relationship, chr6_GBR_r, chr6_Han_r, chr6_Yoruba_r
import json
import io
import base64
import seaborn as sns
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from ld_plot.ld_plot import ld_plot
import re


def variantJoin():
	db_session = session()
	results = db_session.query(Variants, RAFs).join(RAFs).all()
	serialized_results = []
	for result in results:
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
		serialized_results.append(row)
	db_session.close()
	return serialized_results

def variantJoin2():
	db_session = session()
	results = db_session.query(Variants, Variant_gene_relationship, RAFs).join(Variant_gene_relationship, RAFs).all()
	serialized_results = []
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
		serialized_results.append(row)
	db_session.close()
	return serialized_results

def clinJoin():
	db_session = session()
	query = session.query(Clinical_significance, Variant_gene_relationship.gene_name).join(Variant_gene_relationship, Variant_gene_relationship.variant_name == Clinical_significance.variant_name)
	results = query.all()
	serialized_results = []
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
		# add more fields as needed
		}
		serialized_results.append(row)
	db_session.close()
	return serialized_results

def clinJoin2():
	db_session = session()
	results = db_session.query(Variants, Clinical_significance).join(Clinical_significance).all()
	serialized_results = []
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
		serialized_results.append(row)
	db_session.close()
	return serialized_results

def goJoin(searchTerm='cellular_component'):
	db_session = session()
	results = db_session.query(GO_terms, Variant_gene_relationship).join(Variant_gene_relationship).filter(GO_terms.go_domain == searchTerm).all()
	serialized_results = []
	for result in results:
	    row = {
	    "gene_name": result.GO_terms.gene_name,
	    "go_domain": result.GO_terms.go_domain,
	    "go_term_name": result.GO_terms.go_term_name,
	    "go_term_definition": result.GO_terms.go_term_definition,
	    "go_term_accession": result.GO_terms.go_term_accession,
	    "variant_name": result.Variant_gene_relationship.variant_name,
	    }
	    serialized_results.append(row)
	db_session.close()
	uniqueList = []
	for d in serialized_results:
	  if not any(
	    nd["gene_name"] == d["gene_name"] and nd["go_term_accession"] == d["go_term_accession"]
	    for nd in uniqueList
	    ):
	      uniqueList.append(d)
	return uniqueList

def goJoin2(searchTerm='cellular_component'):
	db_session = session()
	results = db_session.query(Variants, Variant_gene_relationship, GO_terms).join(Variant_gene_relationship, Variant_gene_relationship.variant_name == Variants.variant_name).filter(GO_terms.go_domain == searchTerm).join(GO_terms, GO_terms.gene_name == Variant_gene_relationship.gene_name).all()
	serialized_results = []
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
		serialized_results.append(row)
	db_session.close()
	uniqueList = []
	for d in serialized_results:
		if not any(
			nd["gene_name"] == d["gene_name"] and nd["go_term_accession"] == d["go_term_accession"]
			for nd in uniqueList
			):
				uniqueList.append(d)
	return uniqueList

def geneJoin():
	db_session = session()
	results = db_session.query(Variants, Variant_gene_relationship).join(Variant_gene_relationship).all()
	serialized_results = []
	for result in results:
		row = {
		"variant_name": result.Variants.variant_name,
		"gene_name": result.Variant_gene_relationship.gene_name
		}
		serialized_results.append(row)
	serialized_dict = {}
	for d in serialized_results:
		variant = d['variant_name']
		gene = d['gene_name']
		if variant in serialized_dict:
			serialized_dict[variant].append(gene)
		else:
			serialized_dict[variant] = [gene]
	db_session.close()
	return serialized_dict

def variants(search, rafJSON, geneJSON):
		l1 = []
		l2 = []
		l3 = []
		l4 = []
		l5 = []
		l6 = []
		l7 = []
		for i in rafJSON:
			if (search in i['variant_name']) is True:
				l1.append(f"{i['variant_name']} - {i['allele']}")
				l2.append(i['p_value'])
				l3.append(f"{i['chromosome']}:{i['location_on_chromosome']}")
				l5.append(i['gbr_raf'])
				l6.append(i['han_raf'])	
				l7.append(i['yoruba_raf'])	
		for i in geneJSON:
			if (search == i):
				x = ', '.join(geneJSON[i])
				l4.append(x)
		return [l1,l2,l3,l4,l5,l6,l7]

def variants2(search, variantJSON):
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
		return [l1,l2,l3,l4,l5,l6,l7]

def variants3(variantJSON):
		l1 = []
		l2 = []
		l3 = []
		l4 = []
		l5 = []
		l6 = []
		l7 = []
		for i in variantJSON:
			l1.append(f"{i['variant_name']} - {i['allele']}")
			l2.append(i['p_value'])
			l3.append(f"{i['chromosome']}:{i['location_on_chromosome']}")
			l4.append(i['gene_name'])
			l5.append(i['gbr_raf'])
			l6.append(i['han_raf'])	
			l7.append(i['yoruba_raf'])	
		return [l1,l2,l3,l4,l5,l6,l7]

def clinSif(search):
		l8 = []
		l9 = []
		l10 = []
		l11 = []
		l12 = []
		l13 = []
		l14 = []
		for i in Clinical_significance.query.all():
			if (search in i.variant_name) is True:
				l8.append(i.variant_name)
				l9.append(i.variant_consequence)
				l10.append(i.clinical_significance)
				l11.append(i.polyPhen_prediction)
				l12.append(i.polyPhen_score)
				l13.append(i.sift_prediction)
				l14.append(i.sift_score)
		return [l8,l9,l10,l11,l12,l13,l14]

def clinSif2(search, clinJSON):
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

def clinSif3(clinJSON):
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

def goTerms(search, goJSON, searchTerm):
		l15 = []
		l16 = []
		l17 = []
		l18 = []
		l19 = []
		for i in goJSON:
			if (search in i[searchTerm]) is True:
				l15.append(i['gene_name'])
				l16.append(i['go_domain'])
				l17.append(i['go_term_name'])
				l18.append(i['go_term_definition'])
				l19.append(i['go_term_accession'])
		return [l15,l16,l17, l18, l19]

def goTerms2(goJSON):
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

def rangeMaker(cMin, cMax, JSON):
  cMin = cMin.split(".")
  cMax = cMax.split(".")
  r1 = list(range(int(cMin[0]), (int(cMax[0])+1)))
  r2 = [[r1[0]], r1[1:-1], [r1[-1]]]
  newJSON1 = [x for x in JSON if x['chromosome'] in r1]
  newJSON2 = [[], [], []]
  newJSON3 = []
  for obj in newJSON1:
    if obj['chromosome'] == r1[0]:
      newJSON2[0].append(obj)
    elif obj['chromosome'] == r1[-1]:
      newJSON2[2].append(obj)
    else:
      newJSON2[1].append(obj)
  if (len(newJSON2[0])>0) and (len(newJSON2[2])>0):
    for i in range(len(newJSON2[0])-1, -1, -1):
      if newJSON2[0][i]['location_on_chromosome'] < int(cMin[1]):
        del newJSON2[0][i]
    for i in range(len(newJSON2[2])-1, -1, -1): 
      if newJSON2[2][i]['location_on_chromosome'] > int(cMax[1]):
        del newJSON2[2][i]
  elif (len(newJSON2[0])>0) and (len(newJSON2[2])==0):  
    for i in range(len(newJSON2[0])-1, -1, -1):
      if not int(cMin[1]) <= newJSON2[0][i]['location_on_chromosome'] <= int(cMax[1]):
        del newJSON2[0][i]
  for l in newJSON2:
    newJSON3.extend(l)
  return newJSON3

def ldSearch(ld, searchTerm):
	with engine.connect() as conn:
		result = conn.execute(searchTerm.select())
		rows = [dict(row) for row in result]
		serialised_rows = json.dumps(rows)
		deserialised_rows = json.loads(serialised_rows)
		conn.close()
	newResults = []
	for i in deserialised_rows:
		if i['rs_value'] in ld:
			newResults.append(i)
	newResults2 = []
	dict1 = {}
	for obj in newResults:
		dict2 = {}
		rs_value = obj['rs_value']
		for key, value in obj.items():
			if key in ld:
				dict2[key] = value
		dict1[rs_value] = dict2
	return dict1

def dictMaker(ld, pop):
	if pop == 'British':
		ldJSON = ldSearch(ld, chr6_GBR_r)
		return ldJSON
	if pop == 'Han Chinese':
		ldJSON = ldSearch(ld, chr6_Han_r)
		return ldJSON
	if pop == 'Yoruba':
		ldJSON = ldSearch(ld, chr6_Yoruba_r)
		return ldJSON

def dfMaker(ld_dict):
	df = pd.DataFrame.from_dict(ld_dict)
	return df

def plotMaker(df):
	n = df.columns.values
	fig = ld_plot(ld=df, labels=n)
	plt.xticks(fontsize=7)

	# Save plot to buffer
	buffer = io.BytesIO()
	fig.savefig(buffer, format='png')
	buffer.seek(0)
	plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
	return plot_data

#creates a list of genes that will be used for the below function
geneList = []
for i in GO_terms.query.all():
	if i.gene_name in geneList:
		pass
	else:
		geneList.append(i.gene_name)

def geneCheck(search):
	if geneList.count(search)>0:
		return True
	else: 
		return False

def rsCheck(search):
	rgx = re.compile(r"^rs\d*")
	if rgx.search(search):
		return True
	else:
		return False

rsList=[]
with engine.connect() as conn:
  result = conn.execute(chr6_GBR_r.select())
  rows = [dict(row) for row in result]
  serialised_rows = json.dumps(rows)
  deserialised_rows = json.loads(serialised_rows)
  conn.close()
for key, value in deserialised_rows[1].items():
  rsList.append(key)

def ldCheck(ld):
	count = 0
	for i in ld:
		if i in rsList:
			count+=1
		else:
			pass
	if count > 0:
		return True
	elif count == 0:
		return False