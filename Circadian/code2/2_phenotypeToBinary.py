#This script is used for converting sequences of numerical values 
#into binary strings based on the comparison of each number with 
#its predecessor, writing the output to a file: final_Binary_str374.txt
import numpy as np
#file opening for writing the binary strings
file1 = open("final_Binary.txt", "w")
file2 = open("final_Binar_Para.txt", "w")
# Reading the file.
filename='solution.txt'
fn = open(filename,"r")
arr = fn.read()
arrlist = arr.split("\n")

# Reading the file.
filename2='parameters.txt'


#print(arrlist)

arrlist.pop()
# converting each number into binary digits.
def sol_str(q,genotype):
    bin_str = []
    xp = 0
    bin_str.append(0)
    file1.write(str(0))
    file2.write(str(0))
    for j in range(1,len(q)):        
        if q[j] <= q[j-1]:
            bin_str.append(0)
            file1.write(str(0))
            file2.write(str(0))
        else:
            bin_str.append(1)
            file1.write(str(1))
            file2.write(str(1))
    file1.write("\n")
    file2.write(' ')
    file2.write(genotype)
    file2.write("\n")
    return bin_str
    
def read_specific_line(file_path, line_number):
    with open(file_path, 'r') as file:
        for current_line_number, line in enumerate(file, start=1):
            if current_line_number == line_number:
                return line.strip()
    return None  # In case the line number is out of range    
    
    

counter2 = 1
for i in range(0,len(arrlist)):
    if i%19 == 0:
        counter = 0
        q = np.zeros(19)
        q[counter] = arrlist[i]
    if (i%19 != 0):
        q[counter] = arrlist[i]
    counter = counter + 1

    if (i !=0 and (i+1)%19 == 0):
        genotype = read_specific_line(filename2, counter2)
        m = sol_str(q,genotype)
        counter2= counter2 + 3
print('Done.')
file1.close()


























