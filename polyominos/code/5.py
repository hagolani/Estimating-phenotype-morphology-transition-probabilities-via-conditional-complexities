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

 str_arr = file1.readlines()
 prob_arr = file2.readlines()
 #print(str_arr) 
  
 str_arr = [line.strip().split()[-1] for line in str_arr]
 prob_arr = [line.strip().split()[-1] for line in prob_arr]
 print(prob_arr)
 #theone1=theone+1
 
 theoneBinary=str_arr[theone]
 print(theoneBinary)

 k = KC.calc_KC(theoneBinary)
 k1 = round(k,1)

 Z = []
 for s in str_arr:
    combined_str = theoneBinary + s
    #print(combined_str)
    k = KC.calc_KC(combined_str)
    Z.append(np.round(k,1))
  
 Z1 = Z-k1

 upper_bound = []
 for i in range(0,len(Z1)):
    if float(Z1[i]) > 0:
     temp = mt.log10(1/pow(2,float(Z1[i])))
     upper_bound.append(temp)

 # sum of probabilities    
 nplist = np.array(prob_arr)

 nplist1 = np.array(nplist)
 #maxxx = max(nplist)
 #minnn = min(nplist)

 final_prob = []
 for i in range(0, len(nplist1)):
    q = nplist1[i]
    if float(q) > 0:
        qlog = mt.log10(float(q))
        final_prob.append(qlog)
    else:
        print("nothing")
        final_prob.append(0)
 min_non_zero = min(filter(lambda x: x != 0, final_prob))
 final_prob = [min_non_zero if x == 0 else x for x in final_prob]

 np.savetxt(f'phenotype{target_num}.txt', np.column_stack((Z1, final_prob)), fmt='%.6f', header='Z final_prob', delimiter='\t', comments='')


 plt.figure()
 plt.plot(Z1, upper_bound)
 plt.scatter(Z1,final_prob)
 plt.title(f'conditional complexity vs Probability \n for x = {target_num}')
 plt.ylabel(r'$\log_{10} P(x \rightarrow y)$',fontsize=18)
 plt.xlabel(r'$\tilde{K}(y|x)$',fontsize=18)
 plt.rc('xtick',labelsize=15)
 plt.rc('ytick',labelsize=15)
 plt.tight_layout()
 plt.savefig(f's28_Pxy_Kxy{target_num}.jpg',dpi=2500)
 #plt.show()

 file1.close()
 file2.close()
