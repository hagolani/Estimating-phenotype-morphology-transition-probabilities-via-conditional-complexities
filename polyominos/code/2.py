# For Umar
import numpy as np
import KC # used for Lempel-Ziv complexity estimation
import matplotlib.pyplot as plt
import math as mt

file1 = open("data/unique_binary_str.txt","r")
file2 = open("data/unique_str_prob.txt","r")

str_arr = file1.read()
str_arrlist = str_arr.split("\n")
str_arrlist.pop()

prob_arr = file2.read()
prob_arrlist = prob_arr.split("\n")
prob_arrlist.pop()

Z = []
for s in str_arrlist:
    k = KC.calc_KC(s)
    Z.append(np.round(k,1))

#upper_bound = []

#for i in range(0,len(Z)):
#    temp = 1/pow(2,float(Z[i]))
#    upper_bound.append(temp)

# sum of probabilities    
nplist = np.array(prob_arrlist)
#print(nplist)

#maxxx = max(nplist)
#minnn = min(nplist)

#print(maxxx)
#print(minnn)

final_prob = []
for i in range(0, len(nplist)):
    q = nplist[i]
#    print("The value for ",i, "is",q)
    qlog = mt.log10(float(q))
#    print("The log value for ",i, "is",qlog)
    final_prob.append(qlog)

nplist1 = np.array(final_prob)   
    
maxxx1 = np.max(nplist1)
minnn1 = np.min(nplist1)

#print(maxxx1)
#print(minnn1)
    
#print(final_prob)
np.savetxt('probability_plot.txt', np.column_stack((Z, final_prob)), fmt='%.6f', header='Z final_prob', delimiter='\t', comments='')

plt.figure()
#plt.plot(Z, upper_bound)
plt.scatter(Z,final_prob)
plt.title('Complexity vs Probability')
plt.ylabel(r'$\log_{10} P(x)$',fontsize=18)
plt.xlabel(r'$\tilde{K}(x)$',fontsize=18)
plt.rc('xtick',labelsize=15)
plt.rc('ytick',labelsize=15)
plt.tight_layout()
plt.savefig('s28_Px_Kx.jpg')
plt.show()


file1.close()
file2.close()
