import numpy as np

# Open the necessary files
file = open('HP_output_data/output_HPn25.txt', "r")
file1 = open("HP_output_data/HPn25_unique_str_count_prob.txt", "w")
file2 = open("HP_output_data/HPn25_unique_str.txt", "w")
file3 = open("HP_output_data/HPn25_unique_str_prob.txt", "w")

# Read and split the file data by lines
arr = file.read()
arr_t = arr.split("\n")

# Remove any empty lines if present
arr_t = [line for line in arr_t if line]

# Initialize columns
col_1 = []
col_2 = []
col_3 = []

# Loop through each line, splitting by spaces
for line in arr_t:
    temp = line.split()  # Split the line by spaces
    col_1.append(temp[0])
    col_2.append(temp[1])
    col_3.append(temp[2])

print("Reading and splitting done")
print("sample ", col_1[0], col_2[0], col_3[0])

# Calculate the unique occurrences of strings in col_2
arrlist = np.array(col_2)
unique, counts = np.unique(arrlist, return_counts=True)
w = dict(zip(unique, counts))

# Total number of possible outputs based on the length of the strings in col_2
total_outputs = 2 ** len(col_2[0])

# Write the results to the files
for kv in w.items():
    file1.write(f"{kv[0]}\t{kv[1]}\t{kv[1]/total_outputs}\n")
    file2.write(f"{kv[0]}\n")
    file3.write(f"{kv[1]/total_outputs}\n")

# Close all files
file.close()
file1.close()
file2.close()
file3.close()

