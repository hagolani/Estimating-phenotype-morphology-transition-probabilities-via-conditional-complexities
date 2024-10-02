import numpy as np
from collections import OrderedDict
import random as rm
import sys

file  = open("in_out_count.txt","r")
file1 = open("unique_str_count_prob.txt","w")
file2 = open("unique_str.txt","w")
file3 = open("unique_str_prob.txt","w")

arr = file.read()
arr_t = arr.split("\n")
arr_t.pop()

if len(arguments) > 1:
    str_size = int(arguments[1])
    #print("User provided input:", user_input)

#str_size = 18  # size of the string
col_1 = []
col_2 = []
col_3 = []

#temp = arr_t[0]
#print(len(temp))
#print(arr_t[0])
#print("Printed")

for i in range (0,len(arr_t)):
    temp= arr_t[i]
    temp1 = temp[0:str_size]
    col_1.append(temp1)
    temp2 = temp[str_size+1:2*str_size+1]
    col_2.append(temp2)
    temp3 = temp[2*str_size+2:]
    col_3.append(temp3)

len_in_out = len(col_1) 
print("Reading and splitting done")
print("sample ", col_1[0], col_2[0], col_3[0])

print("---------------------------------")
arrlist = np.array(col_2)
unique, counts = np.unique(arrlist, return_counts=True)
w = dict(zip(unique, counts))

#print(w)
count_arr = []
for kv in w.items():
    prob_ind = kv[1]
    count_arr.append(prob_ind)
#print(count_arr)    
n_count_arr = np.array(count_arr)


print("The sum is ",np.sum(n_count_arr))
print("The maximum value is ",np.max(n_count_arr))

total_outputs = 0
for kv in w.items():
    total_outputs = total_outputs+kv[1]
print("Total sum is ",total_outputs)


for kv in w.items():
    file1.write(str(kv[0]))
    file2.write(str(kv[0]))
    file1.write('\t \t')
    file1.write(str(kv[1]))
    file1.write('\t \t')
    file1.write(str(kv[1]/total_outputs))
    file3.write(str(kv[1]/total_outputs))
    file1.write("\n")
    file2.write("\n")
    file3.write("\n")
print("Bingo")


file.close()
file1.close()
file2.close()
file3.close()

#t2 = toc()

#print(t2)
