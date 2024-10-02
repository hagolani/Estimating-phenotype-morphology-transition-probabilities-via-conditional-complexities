import numpy as np
import random as rm
import time

for target_num in range(1, 23):  # Loop from 1 to 22
 target_num = str(target_num)
 # Open all output files in write mode
 file_out1 = open(f'data/binary_rep_init_{target_num}.txt', "w")
 file_out2 = open(f'data/general_info_computations_{target_num}.txt', "w")
 file_out3 = open(f'data/binary_rep_{target_num}.txt', "w")
 file_out4 = open(f'data/sample_binary_rep_{target_num}.txt', "w")
 file_out5 = open(f'data/reverse_indices_{target_num}.txt', "w")
 file_out6 = open(f'data/reverse_output_{target_num}.txt', "w")

 sample_size = 10000

 # Open and read input file
 with open('Polyomino/s_28_list.txt', "r") as file_inp1:
    arr_t1 = file_inp1.read().splitlines()

 print(len(arr_t1))
 print("File Reading Done.")

 # Generate binary representations for each index and write to file_out1
 binary_repr_gen = [np.binary_repr(i, 24) + "\n" for i in range(len(arr_t1))]
 file_out1.writelines(binary_repr_gen)

 print("Done with general representation and file writing.")

 # Start time measurement
 print("Time calculation started.")
 start_time = time.time()



 print("The targeted number is", target_num)
 file_out2.write("General info\n")
 file_out2.write("The number selected is\n")
 file_out2.write(target_num + "\n")

 # Find indices for target number
 indices = [index for index, value in enumerate(arr_t1) if value == target_num]

 # Write indices information to file_out2
 file_out2.write("The length of indices for target number is\n")
 file_out2.write(str(len(indices)) + "\n")
 print("The length of indices for targeted number is ", len(indices))
 #file_out2.write("The indices for target number is\n")
 #file_out2.write(str(indices) + "\n")

 print("Indices found for targeted number")

 # Generate binary representations for indices and write to file_out3
 binary_repr = [np.binary_repr(num_temp, 24) + "\n" for num_temp in indices]
 file_out3.writelines(binary_repr)

 print("Binary representations done for the indices")

 # Sample binary representations
 new_sample = rm.sample(binary_repr, sample_size)
 file_out4.writelines(new_sample)
 print("New Random Sampling done")

 # Manipulate binary strings and create new_col_1
 #new_col_1 = []
 #for x in new_sample:
 #    x = x.strip()  # Remove newline character
 #    temp = ["".join([str(1 - int(bit)) if bit == "0" else str(1 - int(bit)) for bit in x]) + "\n"]
 #    new_col_1.extend(temp)

 new_col_1 = []
 # Assuming new_sample is a list of binary strings like ['001', '010', ...]
 for x in new_sample:
    x = x.strip()  # Remove newline character
    for i in range(len(x)):
        # Create a mutable list of characters from the binary string
        char_list = list(x)
        
        # Flip the bit at the current position
        char_list[i] = '0' if char_list[i] == '1' else '1'
        
        # Convert back to string, add a newline for file writing, and append to new_col_1
        new_col_1.append(''.join(char_list) + "\n")

 # Now new_col_1 contains all the one-bit variations of each binary string from new_sample

 print("New list generated from samples by flipping.")

 # Find reverse indices and write to file_out5
 # Convert binary_repr_gen into a dictionary for O(1) lookups
 binary_repr_gen_dict = {repr.strip(): str(i) for i, repr in enumerate(binary_repr_gen)}

 reverse_indices = []
 for item in new_col_1:
    # Look up the index in the dictionary
    index = binary_repr_gen_dict.get(item.strip(), "000")
    reverse_indices.append(index + "\n")

 file_out5.writelines(reverse_indices)
 print("Reverse indices found")

 # Find reverse output and write to file_out6
 reverse_output = [arr_t1[int(index)] + "\n" for index in reverse_indices]
 file_out6.writelines(reverse_output)
 print("Reverse output found")

 # End time measurement
 end_time = time.time()

 print("Total time in seconds is", end_time - start_time)

 # Close all opened files
 file_out1.close()
 file_out2.close()
 file_out3.close()
 file_out4.close()
 file_out5.close()
 file_out6.close()
 print("done")

