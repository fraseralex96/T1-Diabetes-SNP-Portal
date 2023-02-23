#function to produce interactive manhattan plot

man_function <- function(snplist) {
  
  #load required libraries
  library(manhattanly)
  library('stringr')
  library(htmlwidgets)

  #load data into dataframe
  man_data <- read.csv("./database/Data/Type 1 GWAS.csv", fileEncoding="UTF-8-BOM")


  #split the genomic location data from one column (6:1234) to two columns (6 & 1234) and save this as new dataframe 
  split_location <- data.frame(do.call('rbind', strsplit(as.character(man_data$Location),':',fixed=TRUE)))

  #combine the dataframes
  updated_man_data <-cbind(man_data,split_location) 
  #change the names of certain columns to names that "manhattanly" will recognise
  colnames(updated_man_data)[colnames(updated_man_data) == "X1"] ="CHR"
  colnames(updated_man_data)[colnames(updated_man_data) == "X2"] ="BP"
  colnames(updated_man_data)[colnames(updated_man_data) == "P.value"] ="P"
  #change the X chromosomes into 23 so it can be recognised by "manhattanly"
  updated_man_data$CHR[updated_man_data$CHR == 'X'] <- '23'
  
  #create new dataframe that excludes data where chromosome location is not available
  data_new <- updated_man_data[!is.na(as.numeric(updated_man_data$CHR)), ]
  #ensure certain columns are numeric so it can be recognised by "manhattanly"
  data_new$CHR <- as.numeric(as.character(data_new$CHR))
  data_new$BP <- as.numeric(as.character(data_new$BP))
  #p-value was written like(2x10-13) which is recognised as a character, replace x10 with e so p-value is written like(2e-13) which is recognised as numeric
  data_new$P <- str_replace(data_new$P,' x 10','e')
  data_new$P <- as.numeric(as.character(data_new$P))


  
  #create new column which only has the SNPs and not the risk alleles and add this to the dataframe
  SNP <- sub("\\-.*", "", data_new$Variant.and.risk.allele)
  data_new$SNP = SNP
  #change name of column
  colnames(data_new)[colnames(data_new) == "Mapped.gene"] ="Mapped gene(s)"
  
  #create manhattan plot
  manhattan_plot = manhattanly(data_new, snp = "SNP", gene = "Mapped gene(s)", highlight = snplist, labelChr=c(1:22, "X"), suggestiveline = FALSE, genomewideline = FALSE)
  
  
  
  #save interactive manhattan plot as html
  saveWidget(manhattan_plot, "./static/newman.html", selfcontained=FALSE)
  
}





#function to install "manhattanly" package in R if it hasn't already been installed

using<-function(...) {
    libs<-unlist(list(...))
    req<-unlist(lapply(libs,require,character.only=TRUE))
    need<-libs[req==FALSE]
    if(length(need)>0){ 
        install.packages(need)
        lapply(need,require,character.only=TRUE)
    }
}