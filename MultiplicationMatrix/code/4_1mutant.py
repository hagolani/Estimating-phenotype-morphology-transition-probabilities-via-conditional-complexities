import numpy as np

# Open the file for reading
with open("in_out_count.txt", "r") as file:
    arr_t = file.readlines()

# Extract data into separate lists
col_1 = []  #genotype
col_2 = []  #phenotype
col_3 = []  #count of phenotype
for line in arr_t:
    temp = line.split()
    col_1.append(temp[0]) #geno
    col_2.append(temp[1]) #pheno
    col_3.append(temp[2]) #count

print("Reading and splitting done")


all_unique_cols = list(set(zip(col_1,col_2)))
# Get unique values from col_2
unique_cols = list(set(zip(col_2, col_3)))

for selected_str, count_str in unique_cols:
    count = int(count_str)
    if count > 50:
        # For this selected_str, perform the entire process
        print("Processing string:", selected_str,count_str)

        # Find target genotypes that produce selected_str
        target_strs = [col_1[i] for i, val in enumerate(col_2) if val == selected_str]

        # Mutate each genotype 0 to 1 ; 1 to 0
        new_col_1 = []
        for target_str in target_strs:
            for i in range(len(target_str)):
                temp = list(target_str)
                temp[i] = "1" if temp[i] == "0" else "0"
                new_col_1.append("".join(temp))

        
        # Find the phenotypes of the mutants
        new_col_2 = []
        for geno in new_col_1:
         #print(geno)
         # Find the corresponding col_1 value where col_2 equals geno
         matching_col_2 = next((col_2 for col_1, col_2 in all_unique_cols if col_1 == geno), None)
         print(geno, matching_col_2)
         if matching_col_2:
           new_col_2.append(matching_col_2)
         else:
           new_col_2.append("0")  # no match is found, should not happen

        #print("New outputs generated")
        #print("---------------------------------")
        #print(new_col_2)
        #print(len(new_col_2))
        #print("---------------------------------")

        # Write results to files
        with open(f"possible_new_unique_str_count_prob_{selected_str}.txt", "w") as file1: #, \
             #open(f"possible_new_unique_str_{selected_str}.txt", "w") as file2, \
             #open(f"possible_new_unique_str_prob_{selected_str}.txt", "w") as file3:

            arrlist = np.array(new_col_2)
            unique, counts = np.unique(arrlist, return_counts=True)
            total_outputs = sum(counts)

            for val, count in zip(unique, counts):
                file1.write(f"{selected_str} {val} {count}  {count/total_outputs}\n")
                #file2.write(f"{val}\n")
                #file3.write(f"{count/total_outputs}\n")

        print(f"Processing for {selected_str} completed and saved.")
        print("---------------------------------")

print("All processing completed.")

