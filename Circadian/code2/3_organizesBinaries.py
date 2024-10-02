#It identifies unique binary stings and their 
#   respective counts and then writes this information to multiple output files

import numpy as np

file1 = open("final_Binary.txt", "r")
file2 = open("final_Binary_and_Count.txt","w")
file3 = open("final_Unique_Binary.txt","w")
file4 = open("final_Unique_Count.txt","w")
arr = file1.read()
arrlist = arr.split("\n")
#print(arrlist)
#result = np.where(arrlist=="")[0]
#arrlist = np.delete(arrlist,result)

arrlist.pop()

#print(arrlist)

arrlist = np.array(arrlist) 
unique, counts = np.unique(arrlist, return_counts=True)

w= dict(zip(unique, counts))
#print(len(w))
#print(w)
#prob_arr = []
#str_arr = []
for kv in w.items():
#    print( kv[0],'\t',kv[1])
    file2.write(str(kv[0]))
    file3.write(str(kv[0]))
#    str_arr.append(kv[0])
    file2.write('\t')
    file2.write(str(kv[1]))
    file4.write(str(kv[1]))
#    prob_arr.append(kv[1])
    file2.write("\n")
    file3.write("\n")
    file4.write("\n")
file1.close()
file2.close()
file3.close()
file4.close()
#print(prob_arr)
#print("-----------")
#print(str_arr)
print("Done.")

