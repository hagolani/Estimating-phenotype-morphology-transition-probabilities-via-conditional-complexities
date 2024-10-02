library(dplyr)
rm(list = ls())

dir=dirname(rstudioapi::getActiveDocumentContext()$path)

setwd(dir)
cex0=2.5 ; cex1=2.2
df1=read.table("frequencies_C",header = F)
colnames(df1)=c("Z","prob")

df1 <- df1[df1$Z <= 15, ]

df1$prob=log10(df1$prob)

df2 <- aggregate(prob ~ Z, data = df1, FUN = mean)

lm1=lm(df2$prob ~ df2$Z)

pdf("probCom.pdf")
par(mar = c(5, 6, 4, 2) + 0.1)  # Adjusting margin
par(cex.axis = 1.5, cex.lab = 1.5)
plot(x=df2$Z,y=df2$prob,
     cex=2.5,pch=16,col="blue",ylim = c(min(df2$prob),0),
     xaxt = 'n', yaxt = 'n', xlab = "", ylab = "")


abline(lm1,lwd=2)
axis(1,cex=cex0,line=0)
axis(2,cex=cex0,line=0)
mtext(expression(paste(~tilde(K), "(x)")), side = 1, line = 4,cex=cex0)  # Increase the 'line' value to move the label further down
mtext(expression(paste("mean(",log[10],"P(x))")), side = 2, line = 3.5,cex=cex0)  # Increase the 'line' value to move the label further down

abline(lm1)
dev.off()
