from app import app
from models import Variants, Clinical_significance, GO_terms, RAFs, Variant_gene_relationship, chr6_GBR_r, chr6_Han_r, chr6_Yoruba_r
from db_init import init_db, session, engine
from flask import Flask, jsonify, render_template, request, send_file
from functions import goJoin, rangeMaker, variantJoin, geneJoin, variants, goTerms, clinSif, clinSif3, geneCheck, variantJoin2, variants2, clinJoin, clinJoin2, variants3, dfMaker, plotMaker, ldSearch
import json
import rpy2
import rpy2.robjects as robjects
from rpy2.rinterface_lib.embedded import RRuntimeError
from sqlalchemy import create_engine
import json



@app.route('/')
def index():
  db_session = session()
  results = db_session.query(GO_terms, Variant_gene_relationship).join(Variant_gene_relationship).filter(GO_terms.gene_name == 'HLA-DQB1').all()
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

#allows the app to run when called
if __name__=='__main__':
	init_db()
	app.run(debug=True)

