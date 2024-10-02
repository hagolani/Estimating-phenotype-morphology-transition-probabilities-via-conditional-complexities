rm(list = ls())
library(dplyr)


dir=dirname(rstudioapi::getActiveDocumentContext()$path)
setwd(dir)

#1 mutant bmbs
bmbFound=read.table("results_multmatrix.dat",header = T)
allindis=unique(bmbFound$Parent)

#whole exploration
allfound=read.table("in_out_count_KC.txt",header = T)
allfound <- allfound[!duplicated(allfound[, 2]), ]

alldata = data.frame()
for (indi in allindis) {
  
  bmbFound.tmp = bmbFound[which(bmbFound$Parent==indi),]
  #parent complexity
  pacom = bmbFound.tmp$PaComplexity[1]
  
  #found
  df1n <- allfound %>%
    filter(phenotype %in% bmbFound$Mutant)
  df1n$phenotype= as.numeric(df1n$phenotype)
  bmbFound$Mutant= as.numeric(bmbFound$Mutant)
  
  selected_bmbFound <- bmbFound %>% dplyr::select(Mutant, ConditionalComplexity)
  
  
  df1n <- df1n %>%
    left_join(bmbFound, by = c("phenotype" = "Mutant"))
  df1n$phenotype[2] - df1n$phenotype[1]
  
  
  #not found
  df2n <- allfound %>%
    filter(!(phenotype %in% bmbFound$Mutant))
  
  foundckc=median(df1n$ConditionalComplexity)
  notfoundckc=median(df2n$Conditional_Complexity)
  
  data.tmp=data.frame(phenotype=indi,
                      complexity=pacom,
                      foundckc,notfoundckc)
  alldata=rbind(alldata,data.tmp)
  
}


