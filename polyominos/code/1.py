import numpy as np
from collections import OrderedDict
import random as rm
import operator

def matrix_to_vector(input1, output1):
    with open(input1, 'r') as file:
        lines = file.readlines()

    output_lines = []  # To hold the output strings

    i = 0  # Line counter
    while i < len(lines):
        line = lines[i].strip()
        if line.isdigit():  # If the line is an integer, indicating the start of a new unit
            number = line
            vector = ""
            # Process the next 4 lines as the 4x4 matrix
            for j in range(1, 5):
                matrix_line = lines[i + j].rstrip()  # Trim right side to handle lines shorter than 4 characters
                for char in matrix_line:
                    vector += '1' if char == 'X' else '0'
                # In case the line is shorter than 4 characters, fill the rest with '0's
                vector += '0' * (4 - len(matrix_line))
            # Append the formatted string (number and vector) to the output list
            output_lines.append(f"{number} {vector}")
            i += 4  # Skip the next 4 lines as they've been processed
        i += 1  # Move to the next line

    # Write the processed data to the output file
    with open(output1, 'w') as output_file:
        for line in output_lines:
            output_file.write(line + "\n")



input1 = 'Polyomino/s_28_phenos'  
output1 = "data/unique_binary_str.txt"



matrix_to_vector(input1, output1)



input2 = open('Polyomino/s_28_list.txt',"r")
output2 = open("data/unique_str_prob.txt","w")
arr2 = input2.read()
arr_t2 = arr2.split("\n")
arr_t2.pop()


arrlist = np.array(arr_t2)
unique, counts = np.unique(arrlist, return_counts=True)
w = dict(zip(unique, counts))

sorted_w = dict(sorted(w.items(), key=lambda x: int(x[0])))

total_outputs = 0
for kv in sorted_w.items():
    total_outputs = total_outputs+kv[1]
print("Total sum is ",total_outputs)

for kv in sorted_w.items():
    output2.write(str(kv[1]/total_outputs))
    output2.write("\n")





