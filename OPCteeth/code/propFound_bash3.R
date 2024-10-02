library(dplyr)


rm(list = ls())
dir=dirname(rstudioapi::getActiveDocumentContext()$path)
setwd(dir)

allbmb=read.table("../1neigh/allbmbs.dat",header = T)
allfound=read.table("../global/16000_opc_list.txt",header = T)


allindis=unique(allbmb$PaCom)
alldata=data.frame()
for (indi in allindis) {
  if(indi==87.75)next
bmbFound=allbmb[which(allbmb$PaCom==indi),]
pacom=bmbFound$PaCom[1]

allfound$ConditionalComplexity = pmin(abs(pacom-allfound$OPC),allfound$OPC)

if(nrow(bmbFound)==0)next
#found
df1n <- allfound %>%
  filter(OPC %in% bmbFound$OPC)

#not found
df2n <- allfound %>%
  filter(!(OPC %in% bmbFound$OPC))

df1nn= unique(df1n$ConditionalComplexity)
df2nn= unique(df2n$ConditionalComplexity)

foundckc=median(df1nn) #median(df1n$ConditionalComplexity)
notfoundckc=median(df2nn) #median(df2n$ConditionalComplexity)

data.tmp=data.frame(phenotype=indi,
                    complexity=pacom,
                    foundckc,notfoundckc)
alldata=rbind(alldata,data.tmp)
}

pp=alldata$foundckc-alldata$notfoundckc
pp=pp/max(abs(pp))
pdf("opc_foundOrNot.pdf")
par(cex.axis = 2.2, cex.lab = 2.2)
par(mar = c(5, 7, 4, 2))  # c(bottom, left, top, right)
boxplot(pp,ylab=expression(paste(~tilde(K), "(y|x)"[found], " - ",~tilde(K), "(y|x)"[not_found])),
        ylim=c(min(pp),0.01))

#boxplot(pp,ylab="Conditional complexity median difference: found - not_found",
#        ylim=c(min(pp),0.01))
#points( jitter(rep(1,length(pp)),5), pp)
# Define color thresholds
#low_threshold <- quantile(alldata$complexity, 0.33)
#mid_threshold <- quantile(alldata$complexity, 0.66)

# Assign colors based on value
#point_colors <- ifelse(alldata$complexity < low_threshold, "blue",
#                       ifelse(alldata$complexity < mid_threshold, "green", "red"))

# Add jittered points to the boxplot with color-coding
#points(jitter(rep(1, length(pp)), amount = 0.09), pp, col = "black", pch = 16)

# Add a legend to the plot
#legend("topright", legend = c("Low", "Medium", "High"),title="Complexity", 
#       col = c("blue", "green", "red"), pch = 16)

dev.off()
length(pp)
#plot(alldata$complexity,alldata$foundckc-alldata$notfoundckc)



