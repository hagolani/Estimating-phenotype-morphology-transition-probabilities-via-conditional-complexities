import numpy as np
from collections import OrderedDict
import random as rm
import re
import sys
import os

file0  = open('HP_output_data/output_HPn25.txt',"r")

#URRULULDLDLDRDRDRRURULLD
#URDDRDLLULDDRRRRUURULULD
#URRRDLLDLLULURUURURDRDLL
#UURDRDLDLDLULLUURUURDDDL
#UURDRDLDLDLLULURULURRDDD
#URDRDRDLLULDLDLULURUURDD
selected_str = sys.argv[1] # 'URDRDRDLLULDLDLULURUURDD'

file1 = open("HP_output_data/HP_25_possible_new_unique_str_count_prob_test_"+selected_str+".txt","w")
file1_path = "HP_output_data/HP_25_possible_new_unique_str_count_prob_test_" + selected_str + ".txt"

file2 = open("HP_output_data/HP_25_possible_new_unique_str_test_"+selected_str+".txt","w")
file2_path="HP_output_data/HP_25_possible_new_unique_str_test_"+selected_str+".txt"

file3 = open("HP_output_data/HP_25_possible_new_unique_str_prob_test_"+selected_str+".txt","w")
file3_path="HP_output_data/HP_25_possible_new_unique_str_prob_test_"+selected_str+".txt"

# UUUUURDDRURDRDDLULLDRDLD	105
# UUUUURDDRDLDDDLLUUULUURD
# URDDRDLLULDDRRRRUURULULD
#  UURDRDLDLDLLULURULURRDDD
# UURDRDLDLDLULLUURUURDDDL
#URDRDRDLLULDLDLULURUURDD
#URRRDLLDLLULURUURURDRDLL
#URRULULDLDLDRDRDRRURULLD


str_size = len(selected_str)  # size of the string
print(str_size)
col_1 = []
col_2 = []
col_3 = []

for line in file0:
    # Split each line into columns using any number of spaces as delimiter
    columns = re.split('\s+', line.strip())
    # Assign each column to the respective list
    col_1.append(columns[0])
    col_2.append(columns[1])
    col_3.append(columns[2])

#find all the sequences (phenotypes) in output_HPn25.txt equal to the target sequence, safe the genotypes
target_strs = []
print(len(col_2))
for j in range(0,len(col_2)):
    if selected_str == col_2[j]:
        target_strs.append(col_1[j])

print("For selected string",selected_str)        
print("I am new col 1")
print(target_strs)
print("---------------------------------")

if len(target_strs) < 10:
     print("Less than 10 matches found. Exiting script.")
     file1.close()  ;   os.remove(file1_path)
     file2.close()  ;   os.remove(file2_path)
     file3.close()  ;   os.remove(file3_path)
     exit()
    
    
new_col_1 = [] #the mutants
#explore the one mutant neighborhood
for i in range(0,len(target_strs)):   #
    x = target_strs[i]
    index = 0
    for j in range(0,len(x)):
        temp = list(x)
        if x[index] == "H":
            temp[index] = "P"
            x1 = "".join(temp)
            new_col_1.append(x1)
        else:
            temp[index] = "H"
            x1 = "".join(temp)
            new_col_1.append(x1)
        index = index + 1
    #find the mutant genotype in the global result list to stablish the phenotype
    new_col_2 = []
    for k in range(0,len(new_col_1)):
        p = new_col_1[k]
        count = 0
        for l in range(0,len(col_1)):
            q = col_1[l]
            if p == q:
                count = count +1
                w = col_2[l]
                new_col_2.append(w)
        if count == 0:
            new_col_2.append("AAAAAAAAAAAAAAAAAAAA")
            print(p)

arrlist = np.array(new_col_2) 
unique, counts = np.unique(arrlist, return_counts=True)
w = dict(zip(unique, counts))
#print(w)
#print("-----------------------------")

total_outputs = 0
for kv in w.items():
    total_outputs = total_outputs+kv[1]

for kv in w.items():
    file1.write(selected_str)
    file1.write("\t")
    file1.write(str(kv[0]))
    file2.write(str(kv[0]))
    file1.write("\t")
    file1.write(str(kv[1]))
    file1.write('\t')
    file1.write(str(kv[1]/total_outputs))
    file3.write(str(kv[1]/total_outputs))
    file1.write("\n")
    file2.write("\n")
    file3.write("\n")

file0.close()
file1.close()
file2.close()
file3.close()

#t2 = toc()

#print(t2)
