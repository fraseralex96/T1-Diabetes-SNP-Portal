import pandas as pd
import re

#######MAIN GWAS FILE########

#import the data
DF = pd.read_csv(r'C:/Users/frase/OneDrive/Documents/MSc Bioinformatics/Group Project/Website/database/Data/Type 1 GWAS.csv')

#filter only for chromosome 6 
#df = df[df.Location.str.startswith('6')]

#remove unwanted columns
mainDF = DF[['Variant and risk allele', 'P-value', 'RAF', 'Location']]

#format the p-value into something that is usable by python
newPList = []
for i in mainDF['P-value']:
    rgx = re.compile(r"([0-9])\s.*(-.*)")
    num = rgx.search(i)
    a = num.group(1)
    b = num.group(2)
    newP = float(f'{a}E{b}')
    newPList.append(newP)
mainDF['P-value']=newPList

#split location into chromosome and location
newChr = []
newLoc = []
for i in mainDF['Location']:
    rgx = re.compile(r"(.*):(.*)")
    num = rgx.search(i)
    a = num.group(1)
    b = num.group(2)
    newChr.append(int(a))
    newLoc.append(int(b))
mainDF['Chromosome']=newChr
mainDF['Location on chromosome']=newLoc

newRS = []
allele = []
for i in mainDF['Variant and risk allele']:
    rgx = re.compile(r"(rs[0-9]*)(.*)")
    num = rgx.search(i)
    a = num.group(1)
    b = num.group(2)
    newRS.append(a)
    allele.append(b)
mainDF['Variant']=newRS
mainDF['Allele']=allele

mainDF = mainDF[['Variant', 'Allele', 'P-value', 'Chromosome', 'Location on chromosome']]

mainDF["Allele"] = mainDF["Allele"].str.replace('<b>','')
mainDF["Allele"] = mainDF["Allele"].str.replace('</b>','')
mainDF["Allele"] = mainDF["Allele"].str.replace('-','')


mainDF = mainDF.sort_values(by=['Chromosome', 'Location on chromosome'], ignore_index=True)

#replace blanks with N/A
mainDF = mainDF.fillna('N/A')

mainDF

#export new table
mainDF.to_csv(r'C:/Users/frase/OneDrive/Documents/MSc Bioinformatics/Group Project/Website/database/Data/main.csv')

########CLINICAL SIGNIFICANCE FILE########


#import clinical significance data
csDF = pd.read_csv(r'C:/Users/frase/OneDrive/Documents/MSc Bioinformatics/Group Project/Website/database/Data/Clinical significance.csv')

#select only useful columns
csDF = csDF[['Variant name', 'Variant consequence', 
'Clinical significance', 'PolyPhen prediction', 
'PolyPhen score', 'SIFT prediction', 'SIFT score']]

#replace blanks with N/A
csDF = csDF.fillna('N/A')

#replace commas in the data to avoid confusion when it is read as a csv later
csDF["Clinical significance"]=csDF["Clinical significance"].str.replace(',','/')

#save to a new file
csDF.to_csv(r'C:/Users/frase/OneDrive/Documents/MSc Bioinformatics/Group Project/Website/database/Data/cs.csv', index=True)

#######GO TERMS FILE########
#import GO data
gtDF = pd.read_table(r'C:/Users/frase/OneDrive/Documents/MSc Bioinformatics/Group Project/Website/database/Data/GO terms.tsv')

#replace blanks with N/A
gtDF = gtDF.fillna('N/A')

#save to a new file
gtDF.to_csv(r'C:/Users/frase/OneDrive/Documents/MSc Bioinformatics/Group Project/Website/database/Data/gt.tsv', sep="\t")

########RAF FILE#########
#import data
rafDF = pd.read_csv(r'C:/Users/frase/OneDrive/Documents/MSc Bioinformatics/Group Project/Website/database/Data/RAF-complete.csv')

#drop unnecessary columns
rafDF = rafDF.drop(['Location'], axis=1)

#rename necessary columns
rafDF.columns = ['Variant ID and risk allele', 'Han Chinese RAF', 'Yoruba RAF', 'GBR RAF']

#remove HTML tag from rsValue
rafDF["Variant ID and risk allele"] = rafDF["Variant ID and risk allele"].str.replace('<b>','')
rafDF["Variant ID and risk allele"] = rafDF["Variant ID and risk allele"].str.replace('</b>','')

#replace blanks with N/A
rafDF = rafDF.fillna('N/A')

#create a new file
rafDF.to_csv(r'C:/Users/frase/OneDrive/Documents/MSc Bioinformatics/Group Project/Website/database/Data/raf.csv')
#######GENE TO VARIANT FILE########

#create a table for all mutations and their associated genes

#select required columns into a temporary dataframe
tempdf = DF[['Variant and risk allele', 'Mapped gene']]

#remove HTML tag from rsValue
newRS = []
for i in tempdf['Variant and risk allele']:
    rgx = re.compile(r"(rs[0-9]*).*")
    num = rgx.search(i)
    a = num.group(1)
    newRS.append(a)
tempdf['Variant and risk allele']=newRS


#create the final database by making 'Variant and risk allele' as the temp index and split the gene values 
linkDF = pd.DataFrame(tempdf['Mapped gene'].str.split(',').tolist(), index=tempdf['Variant and risk allele']).stack()

#reset the index to numerical
linkDF = linkDF.reset_index([0, 'Variant and risk allele'])

#assign the required names to the columns
linkDF.columns = ['Variant and risk allele', 'Mapped gene']

#replace blanks with N/A
linkDF = linkDF.fillna('N/A')

#save to a new file
linkDF.to_csv(r'C:/Users/frase/OneDrive/Documents/MSc Bioinformatics/Group Project/Website/database/Data/variant_gene_pairings.csv', index = False)