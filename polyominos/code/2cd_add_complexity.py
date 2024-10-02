# For Umar
import numpy as np
#import LZ78Complexity
import KC # used for Lempel-Ziv complexity estimation
import matplotlib.pyplot as plt
import math as mt

for target_num in range(1, 22):  # Loop from 1 to 22
 theone=target_num ; print(theone)
 target_num = str(target_num)
 file1 = open("data/unique_binary_str.txt","r")
 file2 = open(f"data/prob_reverse_output_{target_num}.txt","r")

 outfile = open(f"dataNeigh{target_num}_new_KC.txt","w")
 #headers
 outfile.write("ParentPhenotyope MutantPhenotype proportion KC_col1 KC_col4 Conditional_Complexity\n")
 
 str_arr = file1.readlines()
 prob_arr = file2.readlines()
  
 str_arr = [line.strip().split()[-1] for line in str_arr]
 prob_arr = [line.strip().split()[-1] for line in prob_arr] 
 theoneBinary=str_arr[theone]

 iji=-1
 k1 = KC.calc_KC(theoneBinary)
 for s in str_arr:
    iji=iji+1
    print(iji)
    p = prob_arr[iji]
    k2 = KC.calc_KC(s)
    combined_str = theoneBinary + s
    k = KC.calc_KC(combined_str)
    
    outfile.write(f" {theoneBinary} {s} {p} {k1:.2f} {k2:.2f} {k:.2f}\n")
 
 
 
 
 
 #Z1 = Z-k1

 
 file1.close()
 file2.close()
 outfile.close()
 

 
 
