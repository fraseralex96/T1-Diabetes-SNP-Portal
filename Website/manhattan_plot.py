#import modules
import pandas as pd
import re 
import numpy as np
import seaborn as sns

#import data
df = pd.read_csv(r'C:/Users/frase/OneDrive/Documents/MSc Bioinformatics/Group Project/Data/Type 1 GWAS.csv')

#'re-make' the p-values so they are in a python friendly format
newPList = []
for i in df['P-value']:
    rgx = re.compile(r"([0-9])\s.*(-.*)")
    num = rgx.search(i)
    a = num.group(1)
    b = num.group(2)
    newP = float(f'{a}E{b}')
    newPList.append(newP)
df['P-value']=newPList
df['-log10P'] = -np.log10(df['P-value'])

#separate chromosome from location in the current location format of chromosome:location
newChr = []
newLoc = []
for i in df['Location']:
    rgx = re.compile(r"(.*):(.*)")
    num = rgx.search(i)
    a = num.group(1)
    b = num.group(2)
    newChr.append(int(a))
    newLoc.append(int(b))
df['Chr']=newChr
df['Location on chromosome']=newLoc

#sort by chromosome and location on chromosome 
df = df.sort_values(by=['Chr', 'Location on chromosome'], ignore_index=True)

#create a new category called SNP number which is the index
#this will be used for the x-axis
df['SNP Number'] = df.index

#create the manhattan plot
grid = sns.relplot(
    data=df,
    x = 'SNP Number',
    y = '-log10P',
    aspect = 3,
    hue = 'Chr',
    palette = 'Set1',
    legend= None
)
grid.ax.set_xlabel('Chromosome')
grid.ax.set_xticks(df.groupby('Chr')['SNP Number'].median())
grid.ax.set_xticklabels(df['Chr'].unique())
grid.fig.suptitle('GWAS plot showing association between SNPs on autosomes and T1D')

grid.savefig('C:/Users/frase/OneDrive/Documents/MSc Bioinformatics/Group Project/Data/manhattan_plot.png')