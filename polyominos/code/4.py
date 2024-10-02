import numpy as np
from collections import OrderedDict
import random as rm
import time
for target_num in range(1, 2):  # Loop from 1 to 22
 target_num = str(target_num)
 
 file_inp1 = open(f'data/reverse_output_{target_num}.txt', "r") 
 file_out1 = open(f'data/prob_reverse_output_{target_num}.txt',"w")

 arr1 = file_inp1.read()
 arr_t1 = arr1.split("\n")
 arr_t1.pop()

 #print(arr_t1)
 print(len(arr_t1))
 print("File Reading Done.")


 arrlist = np.array(arr_t1)
 unique, counts = np.unique(arrlist, return_counts=True)
 w = dict(zip(unique, counts))
 
 existing_w = set(w.keys())

 # Create a set of all keys that should be present (0 to 22)
 expected_w = set(map(str, range(23)))

 # Find the missing keys
 missing_w = expected_w - existing_w

 # Add the missing keys with a value of 0 to the original dictionary
 for key in missing_w:
    w[key] = 0

 print(w)

 sorted_w = dict(sorted(w.items(), key=lambda x: int(x[0])))
 print(sorted_w)

 total_outputs = 0
 for kv in sorted_w.items():
    total_outputs = total_outputs+kv[1]
 print("Total sum is ",total_outputs)

 for kv in sorted_w.items():
    file_out1.write(str(kv[1]/total_outputs))
    file_out1.write("\n")

 file_out1.close()

print("done")
