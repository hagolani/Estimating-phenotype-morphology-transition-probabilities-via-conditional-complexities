import numpy as np
from collections import defaultdict

file1 = open("in_str.txt", "r")
file2 = open("out_str.txt", "r")

instr = file1.read()
outstr = file2.read()

in_str = instr.split("\n")
out_str = outstr.split("\n")

#print(in_str)
#print(out_str)

in_str.pop()
out_str.pop()

#print(in_str)
#print(out_str)

# Create a dictionary to store the mappings from B to A
mapping = defaultdict(list)
for a, b in zip(in_str, out_str):
    mapping[b].append(a)

# Find the unique elements of B
unique_b = set(out_str)

# Write the results to a file
with open('in_out_count.txt', 'w') as f:
    for b in unique_b:
        a_list = mapping[b]
        count = len(a_list)
        unique_a = set(a_list)
        for a in unique_a:
            f.write(f'{a}\t{b}\t{count}\n')

file1.close()
file2.close()

print("Bingooooooooo")

