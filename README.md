

# Team Microsoft Edge: MSc-Bioinformatics-group-project 
## Software development project 

Type 1 Diabetes SNP Portal is a website founded by a group of 4 Master's students from Queen Mary University of London (QMUL) in 2023 under the supervision of Prof. Conrad Bessant and Dr Matteo Fumagalli. The website was developed in order to leverage upon and link all the genomic, functional, and clinical information available on Type 1 Diabetes (T1D). Genome-wide association studies (GWAS) have identified a large number of SNPs (single nucleotide polymorphisms) / genetic variants associated with T1D, however properly interpreting the mapping of the genetic basis of T1D can be difficult. The Type 1 Diabetes SNP Portal makes it easier for users to retrieve genomic information of variants along with population, functional and clinical information ultimately making it easier to interpret the mapping of the genetic basis of T1D.

### Website Link
```bash
  http://13.42.53.58
```


## Getting Started
To run on your localhost please download the directory 'final_website'. Alternately, you can clone the project and run it locally.


## Run Locally

Clone the project

```bash
  git clone https://github.com/fraseralex96/Microsoft_edge
```

Go to the project directory

```bash
  cd final_website
```

Install dependencies

```bash
  pip install flask==2.2.2
  pip install rpy2==3.5.1
  pip install pandas==1.5.3
  pip install seaborn==0.12.2
  pip install matplotlib==3.7.0
  pip install requests==2.21.0
  pip install flask_sqlalchemy==3.0.2
  pip install SQLAlchemy==1.4.46
  pip install ld_plot==0.0.2.1
  pip install numpy==1.24.2

```

Running the website

In your commandline open the 'final_website' directory and run the following command:

```bash
  python main.py
```
Copy the localhost URL and paste it into your browser (for best user experience please use Google Chrome or Safari).

This would lead you to the homepage of 'Type 1 Diabetes SNP Portal', where you can browse for SNPs and perform data analysis such as creating Manhattan or Linkage Disequilibrium plots.

## Authors

* Alexandre Fraser - [fraseralex96](https://www.github.com/fraseralex96)
* Lynnette Bhebhe - [lbhebhe](https://www.github.com/lbhebhe)
* Fatema Hajizadah - [Fatema21H](https://www.github.com/Fatema21H)
* Peter Ulijaszek Scott - [ulijawesome](https://www.github.com/ulijawesome)

## Acknowledgements
Thank you to Professor Conrad Bessant ([conradbessant](https://www.github.com/conradbessant)) and Dr Matteo Fumagalli ([mfumagalli](https://www.github.com/mfumagalli)) for your support and guidance.


