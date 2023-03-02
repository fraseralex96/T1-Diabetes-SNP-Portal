#load modules
import csv, sqlite3
import pandas as pd

#create a connection to a SQLite database
con = sqlite3.connect('DB.db')
cur = con.cursor() 

#SQL to add data to the Variants table
cur.execute("CREATE TABLE Variants(Variant_ID INT PRIMARY KEY, Variant_name VARCHAR(30), Allele VARCHAR(30), P_value REAL, Chromosome INT, Location_on_chromosome INT);")

with open('./Data/main.csv') as file:
    for row in file:
        cur.execute("INSERT INTO Variants VALUES(?,?,?,?,?,?)", row.split(','))
        con.commit()


#SQL to create and add data to clinical significance table
cur.execute("CREATE TABLE Clinical_significance(Variant_ID INT PRIMARY KEY, Variant_name VARCHAR(30), Variant_consequence TEXT, Clinical_significance TEXT, polyPhen_prediction TEXT, polyPhen_score INT, sift_prediction TEXT, sift_score INT, FOREIGN KEY (Variant_name) REFERENCES Variants(Variant_name));")

with open('./Data/cs.csv') as file:
    for row in file:
        cur.execute("INSERT INTO Clinical_significance VALUES(?,?,?,?,?,?,?,?)", row.split(','))
        con.commit()


#SQL to create and add data to RAFs table 

cur.execute("CREATE TABLE RAFs(Variant_ID INT PRIMARY KEY, Variant_name VARCHAR(30), Han_raf FLOAT, Yoruba_raf FLOAT, GBR_raf FLOAT, FOREIGN KEY (Variant_name) REFERENCES Variants(Variant_name));")

with open('./Data/raf.csv') as file:
    for row in file:
        cur.execute("INSERT INTO RAFs VALUES(?,?,?,?,?)", row.split(','))
        con.commit()


#SQL to create and add data to Variant_gene_relationship table 

cur.execute("CREATE TABLE Variant_gene_relationship(Variant_name VARCHAR(30) NOT NULL, Gene_name VARCHAR(30) NOT NULL, PRIMARY KEY (Variant_name, Gene_name), FOREIGN KEY (Variant_name) REFERENCES Variants(Variant_name));")


with open('./Data/variant_gene_pairings.csv') as file:
    for row in file:
        # Trim the gene name before inserting it into the table
        gene_name = row.split(',')[1].strip()  # strip() removes leading/trailing whitespace
        # Check if the record already exists
        cur.execute("SELECT * FROM Variant_gene_relationship WHERE Variant_name=? AND Gene_name=?", (row.split(',')[0], gene_name))
        existing_record = cur.fetchone()

        # Insert the record only if it doesn't already exist
        if not existing_record:
            cur.execute("INSERT INTO Variant_gene_relationship VALUES(?,?)", (row.split(',')[0], gene_name))
            con.commit()
#SQL to create and add data to GO_terms table 

cur.execute("CREATE TABLE GO_terms(Gene_ID INT PRIMARY KEY, Gene_name VARCHAR(30), GO_domain TEXT, GO_term_name TEXT, GO_term_definition TEXT, GO_term_accession TEXT,FOREIGN KEY (Gene_name) REFERENCES Variant_gene_relationship(Gene_name));")

with open('./Data/gt.tsv') as file:
    for row in file:
        cur.execute("INSERT INTO GO_terms VALUES(?,?,?,?,?,?)", row.split('\t'))
        con.commit()

#create a matrix for LD values for GBR chr6

df = pd.read_csv('./Data/chr6_GBR_r.csv')
#make the column names into a list for automating the process of SQL table creation
cols = df.columns.tolist()
cols.pop(0)

cur.execute("CREATE TABLE chr6_GBR_r(rs_value VARCHAR(30) PRIMARY KEY);")
#add a column for each of the column names in df, importantly this is automated
for col in cols:
    cur.execute(f"ALTER TABLE chr6_GBR_r ADD COLUMN {col} FLOAT")
    con.commit()

with open('./Data/chr6_GBR_r.csv') as file:
    for row in file:
        cur.execute("INSERT INTO chr6_GBR_r VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", row.split(','))
        con.commit()

#create a matrix for LD values for Han chr6

df = pd.read_csv('./Data/chr6_Han_r.csv')
#make the column names into a list for automating the process of SQL table creation
cols = df.columns.tolist()
cols.pop(0)

cur.execute("CREATE TABLE chr6_Han_r(rs_value VARCHAR(30) PRIMARY KEY);")
#add a column for each of the column names in df, importantly this is automated
for col in cols:
    cur.execute(f"ALTER TABLE chr6_Han_r ADD COLUMN {col} FLOAT")
    con.commit()

with open('./Data/chr6_Han_r.csv') as file:
    for row in file:
        cur.execute("INSERT INTO chr6_Han_r VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", row.split(','))
        con.commit()

#create a matrix for LD values for Yoruba chr6

df = pd.read_csv('./Data/chr6_Yoruba_r.csv')
#make the column names into a list for automating the process of SQL table creation
cols = df.columns.tolist()
cols.pop(0)

cur.execute("CREATE TABLE chr6_Yoruba_r(rs_value VARCHAR(30) PRIMARY KEY);")
#add a column for each of the column names in df, importantly this is automated
for col in cols:
    cur.execute(f"ALTER TABLE chr6_Yoruba_r ADD COLUMN {col} FLOAT")
    con.commit()

with open('./Data/chr6_Yoruba_r.csv') as file:
    for row in file:
        cur.execute("INSERT INTO chr6_Yoruba_r VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", row.split(','))
        con.commit()

con.close()