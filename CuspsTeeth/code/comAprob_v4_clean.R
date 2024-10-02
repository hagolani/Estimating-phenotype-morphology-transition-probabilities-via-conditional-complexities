library(dplyr)
library(MASS)
library(gtools) 
library(matrixStats)
#if (!require("nloptr")) install.packages("nloptr", dependencies=TRUE)
#install.packages("lpSolve", dependencies = TRUE)

rm(list = ls())
cex_axis=2.2 ; cex_lab=2.2 ; cex_main=2.2 ; cex_leyend=1.25
cex2=2.5

dir=dirname(rstudioapi::getActiveDocumentContext()$path)
setwd(dir)

dfmax=read.table("frequencies_C",header = F)
#colnames(dfmax)=c("Z","prob")
NPheno=length(unique(dfmax$V1)) # mmax , uniqM
rm(dfmax)

allindis=c("frequencies_per_C0_01","frequencies_per_C0_03","frequencies_per_C0_05",
           "frequencies_per_C0_07","frequencies_per_C0_09","frequencies_per_C0_11")
cc=1
alldata=data.frame()
for (indi in allindis) {
   df.tmp=read.table(indi)
   df.tmp$complexity=cc ; cc=cc+2
   alldata=rbind(alldata,df.tmp)
}

df=alldata

#colnames(df) = c("ComplexityMutant","Freq","Complexity")
colnames(df) = c("MutComplexity","Freq","PaCom")

df$ConditionalComplexity = pmin(abs(df$PaCom - df$MutComplexity),df$MutComplexity)

#df$ConditionalComplexity=pmin(abs(df$Complexity-df$ComplexityMutant),df$ComplexityMutant)
#df=df[df$Freq>0.00001,]                        

allindis=unique(df$PaCom)
save.stas=data.frame()
for (indi in allindis) {

    df1=df[which(df$PaCom==indi),]
    df1=df1[order(df1$ConditionalComplexity),]
    df1$Freq=log10(df1$Freq)
    
    df1 <- aggregate(Freq ~ ConditionalComplexity, data = df1, FUN = mean)
    
    #df1=df1[df1$ConditionalComplexity<17,]
    df1=df1[df1$Freq>-10,]
    
    NPheno=length(unique(df1$ConditionalComplexity))
    
    minC= min(df1$ConditionalComplexity) ; maxC= max(df1$ConditionalComplexity)
    upper_bound=df1
    upper_bound$Z2=log2(NPheno)*((df1$ConditionalComplexity-minC)/(maxC-minC))
    
    maxis <- df1 %>%
      group_by(ConditionalComplexity) %>%
      summarise(Max_prob = max(Freq))
    maxis20=maxis[which(maxis$Max_prob>-7),]
    
    #testing ******************************************

    # Extract x and y
    x <- maxis20$ConditionalComplexity
    y <- maxis20$Max_prob
    
    # Function to compute the residual sum for a given line
    compute_residuals <- function(x, y, a, b) {
      residuals <- y - (a + b * x)
      return(sum(residuals[residuals > 0]^2))  # Sum of squared residuals above the line
    }
    
    # Initialize best result
    best_residual_sum <- Inf
    best_pair <- NULL
    best_params <- NULL
    
    # Iterate over all pairs of points
    combinations <- combn(nrow(maxis20), 2)
    for (i in 1:ncol(combinations)) {
      idx <- combinations[, i]
      x1 <- x[idx[1]]
      y1 <- y[idx[1]]
      x2 <- x[idx[2]]
      y2 <- y[idx[2]]
      
      # Calculate slope (b) and intercept (a) of the line
      b <- (y2 - y1) / (x2 - x1)
      a <- y1 - b * x1
      
      # Check if the line is above all points
      if (all(y <= a + b * x)) {
        # Compute residuals
        residual_sum <- compute_residuals(x, y, a, b)
        
        # Update best result if this combination is better
        if (residual_sum < best_residual_sum) {
          best_residual_sum <- residual_sum
          best_pair <- idx
          best_params <- c(a = a, b = b)
        }
      }
    }
    
    # Extract the best pair of points
    best_x <- x[best_pair]
    best_y <- y[best_pair]
  
    #testing ******************************************  
    
    a=-1 ; b=0
    #upper_bound=df1
    upper_bound$Max_prob2= log10(2**(a*upper_bound$Z2+b))
    
    maxis21=data.frame(maxis20[which(maxis20$Max_prob==max(maxis20$Max_prob)),])
    maxis22=data.frame(maxis20[which(maxis20$Max_prob==min(maxis20$Max_prob)),])
    maxis23=rbind(maxis21,maxis22)
    
    model <- lm(Max_prob ~ ConditionalComplexity, data = maxis20)
    model1 <- lm(Max_prob2 ~ ConditionalComplexity, data = upper_bound)
    color1=rgb(0, 0, 0, 0.75)
    
    pearson.r2 = (cor(as.numeric(maxis20$ConditionalComplexity),maxis20$Max_prob))**2
    
    ######################    test bootstrap
    x1=maxis20$ConditionalComplexity ; y1=maxis20$Max_prob
    x2=upper_bound$ConditionalComplexity ; y2=upper_bound$Max_prob2
    
    dfmx=data.frame(x=x1,y=y1)
    dfbound=data.frame(x=x2,y=y2)
    
    fit1 <- glm(y ~ x, data=dfmx)
    ndf1 <- data.frame(x=seq(min(dfmx$x), max(dfmx$x), length.out=1e3))
    pred1 <- predict(fit1, newdata=ndf1, type='link')
    
    fit2 <- glm(y ~ x, data=dfbound)
    ndf2 <- data.frame(x=seq(min(dfbound$x), max(dfbound$x), length.out=1e3))
    pred2 <- predict(fit2, newdata=ndf2, type='link')
    
    n_boot=999
    set.seed(42)
    bf <- replicate(
      999L, {
        bdf <- dfmx[sample.int(nrow(dfmx), replace=TRUE), ]
        glm(y ~ x, data=bdf)
      },
      simplify=FALSE
    )
    
  
    bf2 <- replicate(
      999L, {
        bdf <- dfbound[sample.int(nrow(dfbound), replace=TRUE), ]
        glm(y ~ x, data=bdf)
      },
      simplify=FALSE
    )
    
    bpred <- sapply(bf, predict, newdata=ndf1, type='link')
    ci <- \(x, sd) x + as.matrix(sd*(-qt(.025, Inf))) %*% cbind(-1, 1)
    bpredci <- ci(matrixStats::rowMeans2(bpred), matrixStats::rowSds(bpred))
    
    
    
    
    
    boot_fits <- matrix(NA, nrow = n_boot, ncol = length(x))
    slope_diff <- numeric(n_boot)
    # Extract slopes and calculate the difference
    for (i in 1:n_boot) {
      boot_fits[i, ] <- predict(bf[[i]], newdata = data.frame(x = x))
      slope_diff[i] <- bf[[i]]$coefficients[2] - bf2[[i]]$coefficients[2]
    }
    
    # Calculate confidence interval
    slope_diff=na.omit(slope_diff)
    ci <- quantile(slope_diff, probs = c(0.025, 0.975))
    
    ci_lower <- apply(boot_fits, 2, quantile, probs = 0.025)
    ci_upper <- apply(boot_fits, 2, quantile, probs = 0.975)
    
    
    # Print results
    cat("Bootstrap 95% confidence interval for slope difference:", ci, "\n")
    
    # Test if 0 is within the confidence interval
    if (ci[1] > 0 || ci[2] < 0) {
      print("The slopes are significantly different.")
      a="boot: sig different"
      asv="sigdifferent"
    } else {
      print("The slopes are not significantly different.")
      a="boot: NOT sig different"
      asv="notsigdifferent"
    }
    
    
    
    
    
    #################
    
    
    
    
    pdf(paste(indi,"_cShade_CI.pdf",sep=""))
    par(mar = c(5, 6, 4, 2) + 0.1)  # Adjusting margin
    par(cex.axis = cex_axis, cex.lab = cex_lab , cex_main=cex_lab)
    
    # Initial scatter plot
    plot(x = df1$ConditionalComplexity, y = df1$Freq,
         xaxt = 'n', yaxt = 'n', xlab = "", ylab = "",
         cex = cex2, pch = 16, col = "blue", ylim = c(min(df1$Freq), 0))
    
    axis(1,cex=cex2,line=0)
    axis(2,cex=cex2,line=0)
    mtext(expression(paste(~tilde(K), "(y|x)")), side = 1, line = 4,cex=cex2)  # Increase the 'line' value to move the label further down
    mtext(expression(paste("mean(log"[10], " P(x" %->% "y))")), side = 2, line = 3.5,cex=cex2)  # Increase the 'line' value to move the label further down
    
    
    # Add points for dfmx
    points(dfmx, col = "black", pch = 16, cex = 1.5)
    
    # Add the main fitted line
    lines(ndf1$x, fit1$family$linkinv(pred1), col = "black", lwd = 3)
    
    # Create a shaded area between the two prediction interval lines
    polygon(c(ndf1$x, rev(ndf1$x)),
            c(fit1$family$linkinv(bpredci[, 1]), rev(fit1$family$linkinv(bpredci[, 2]))),
            col = rgb(0, 0, 0, alpha = 0.1), border = NA) # Adjust the alpha level for shading
    
    # Add the regression line
    abline(model1, col = "red", lwd = 3)
    
    legend("topright",legend = c("Fitted model","Fitted 95% CI","Bound model"),
           lwd = c(2.5, 2.5,2.5),lty=c(1,1,1),cex=cex_leyend,        # Point symbols like the plot
           col = c("black","gray", "red")) # Colors for the symbols
      
      
      #add stats
      #prediction one, negative correlation
      #cor(df1$Freq,df1$ConditionalComplexity)
      corr=cor.test(df1$Freq,df1$ConditionalComplexity,method="spearman")
      #prediction two, linear
      summary_model=summary(model)
      f_statistic <- summary_model$fstatistic[1]
      model_p_value <- pf(f_statistic, summary_model$fstatistic[2], summary_model$fstatistic[3], lower.tail = FALSE)
      #prediction three, slope
        #model  maxis20
        #model1 upper_bound
     
      group1 <- rep("Fitted", nrow(maxis20))
      group2 <- rep("Bound", nrow(upper_bound))
      
      x <- c(maxis20$ConditionalComplexity, upper_bound$ConditionalComplexity)
      y <- c(maxis20$Max_prob, upper_bound$Max_prob2)
      group <- factor(c(group1, group2))
      model3 <- lm(y ~ x * group)
      summary_model3 <- summary(model3)
      anova_model <- anova(model3)
      print(anova_model)
    
      interaction_p_value <- summary_model3$coefficients[4, 4] # p-value of the interaction term
      
      tmp=data.frame(spearman=corr$estimate,pvalcorr=corr$p.value,
                     pvallinear=model_p_value,pvalanova=interaction_p_value,
                     bootstrap=asv,pearson=pearson.r2)
      save.stas=rbind(save.stas,tmp)
      
      
      
    dev.off()
    
    
    
    pdf(paste(indi,"_cShade_CI_stats.pdf",sep=""))
    par(mar = c(5, 6, 4, 2) + 0.1)  # Adjusting margin
    par(cex.axis = cex_axis, cex.lab = cex_lab , cex_main=cex_lab)
    
    # Initial scatter plot
    plot(x = df1$ConditionalComplexity, y = df1$Freq,
         xaxt = 'n', yaxt = 'n', xlab = "", ylab = "",
         cex = cex2, pch = 16, col = "blue", ylim = c(min(df1$Freq), 0))
    
    axis(1,cex=cex2,line=0)
    axis(2,cex=cex2,line=0)
    mtext(expression(paste(~tilde(K), "(y|x)")), side = 1, line = 4,cex=cex2)  # Increase the 'line' value to move the label further down
    mtext(expression(paste("mean(log"[10], " P(x" %->% "y))")), side = 2, line = 3.5,cex=cex2)  # Increase the 'line' value to move the label further down
    
    
    # Add points for dfmx
    points(dfmx, col = "black", pch = 16, cex = 1.5)
    
    # Add the main fitted line
    lines(ndf1$x, fit1$family$linkinv(pred1), col = "black", lwd = 3)
    
    # Create a shaded area between the two prediction interval lines
    polygon(c(ndf1$x, rev(ndf1$x)),
            c(fit1$family$linkinv(bpredci[, 1]), rev(fit1$family$linkinv(bpredci[, 2]))),
            col = rgb(0, 0, 0, alpha = 0.1), border = NA) # Adjust the alpha level for shading
    
    # Add the regression line
    abline(model1, col = "red", lwd = 3)
    
    legend("topright",legend = c("Fitted model","Fitted 95% CI","Bound model"),
           lwd = c(2.5, 2.5,2.5),lty=c(1,1,1),cex=cex_leyend,        # Point symbols like the plot
           col = c("black","gray", "red")) # Colors for the symbols
    
    
    plot_limits <- par("usr")
    x_left <- plot_limits[1]  # Leftmost x-coordinate
    y_bottom <- plot_limits[3] # Bottommost y-coordinate
    # Adjusting the text positions relative to the bottom left corner
    text(x_left, y_bottom + 0.25, paste("Level 1: corr", round(corr$estimate, 4), "pval", round(corr$p.value, 4)), adj = c(0, 0))
    #text(x_left, y_bottom + 0.50, paste("Level 2: lm pval", round(model_p_value, 4)), adj = c(0, 0))
    text(x_left, y_bottom + 0.50,bquote("Level 2: " ~ R^2 ~ .(round(pearson.r2, 4))),adj = c(0, 0))
    # text(x_left, y_bottom + 0.75, paste("Prediction 3: anova pval", round(interaction_p_value, 4)), adj = c(0, 0))
    text(x_left, y_bottom + 0.75, paste("Level 3: bootstrap", a), adj = c(0, 0))
    
    
    dev.off()
    
    
    
    
    
    
}


write.table(save.stas,"stats.dat")




save.stas=read.table("stats.dat")
par(mfrow=c(1,1))



pdf("stats_circadian_corr.pdf")
par(mar = c(5, 6, 4, 2) + 0.1)  # Adjusting margin
par(cex.axis = cex_axis, cex.lab = cex_lab, cex.main=cex_main)
boxplot(save.stas$spearman,
        ylim=c(-1,1),
        main="Level (I) \n Spearman correlations",
        xlab="",ylab="correlations")
abline(0,0)
dev.off()

pdf("stats_circadian_lm.pdf")
par(mar = c(5, 6, 4, 2) + 0.1)  # Adjusting margin
par(cex.axis = cex_axis, cex.lab = cex_lab, cex.main=cex_main)
boxplot(save.stas$pvallinear,
        ylim=c(min(save.stas$pvallinear),0.051),
        main="Level (II) \n Significant linear regressions",
        xlab="",ylab="p-values")
abline(0.05,0)
dev.off()

#remove predicted if no linear correlation
#save.stas$bootstrap2="sigdifferent"
for (iji in 1:nrow(save.stas)) {
  if(save.stas$pvallinear[iji]>0.05){
    save.stas$bootstrap[iji]="sigdifferent"
  }
}


not_npredicted=nrow(save.stas[which(save.stas$bootstrap=="sigdifferent"),])
npredicted=nrow(save.stas[which(save.stas$bootstrap=="notsigdifferent"),])
total=sum(not_npredicted,npredicted)

pdf("stats_circadian_slope.pdf")
par(mar = c(5, 6, 4, 2) + 0.1)  # Adjusting margin
par(cex.axis = cex_axis, cex.lab = cex_lab, cex.main=cex_main)
barplot(c(not_npredicted/total,npredicted/total),
        main="Level (III) \n Predicted slopes",
        ylab="proportion of phenotypes",
        names.arg = c("Not predicted","Predicted"))

dev.off()

pdf("stats_cusp_pear_r2.pdf")
par(mar = c(5, 6, 4, 2) + 0.1)  # Adjusting margin
par(cex.axis = cex_axis, cex.lab = cex_lab, cex.main=cex_main)
boxplot(save.stas$pearson,
        ylim=c(0,1),
        main="Level (II) \n Pearson correlations",
        xlab="",ylab=expression(R^2))
#abline(0,0)
dev.off()