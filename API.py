import requests
import sys
import json

###GWAS###

url = "https://www.ebi.ac.uk/gwas/rest/api/efoTraits/MONDO_0005147/associations"
response = requests.get(url)
data = json.loads(response.text)
first_object = data['_embedded']['associations'][0]
print(first_object['riskFrequency'])

rsValues = [data['_embedded']['associations'][i]['loci'][0]['strongestRiskAlleles'][0]['riskAlleleName'] for i in range(len(data['_embedded']['associations']))]
pValues = [data['_embedded']['associations'][i]['pvalue'] for i in range(len(data['_embedded']['associations']))]

###ENSEMBLE###
server = "http://grch37.rest.ensembl.org"
ext = "/ld/human/pairwise/rs73043122/rs34941730?population_name=1000GENOMES:phase_3:GBR;content-type=application/json"
 
r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
 
data = r.json()
print(data)
