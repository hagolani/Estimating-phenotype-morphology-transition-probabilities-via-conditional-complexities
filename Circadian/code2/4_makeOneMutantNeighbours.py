import numpy as np
from math import sqrt
import random as rm
import matplotlib.pyplot as plt
import sys

#0110000000000000011
#0110000000000000000
#0111111111100000001
#0111111111000000011
#0111111111100000011
#0111111100001001110
#0111100000001111111
#0100000000000000000
#0100000000000000001
#0100000000000001111
#0100000000011111111
#0110000000000000001
#0110000000011111111
#0111000000000000000
#0111000000011111100
#0111110010111111111
#0111111000000000011
#0111111100000001111
thephenotype = sys.argv[1] #"0111111100000001111"
print("input2 ",thephenotype)
# Initializing files and arrays
fileout = open("dataNeigh" + thephenotype + "_new.txt", "w")
# headers
fileout.write("ParentPhenotype line ParentGenotype MutantPhenotype MutantGenotype\n")

filein = "final_Binar_Para.txt"

# converting each number into binary digits.
def sol_str(q):
    bin_str = []
    for j in range(1, len(q)):
        if q[j] <= q[j - 1]:
            bin_str.append(0)
        else:
            bin_str.append(1)
    return bin_str

def modify_sequence(sequence):
    modified_sequences = []
    for i, num in enumerate(sequence):
        modified_sequence = sequence.copy()
        for replacement in range(8):
            if replacement != num:
                modified_sequence[i] = replacement
                modified_sequences.append(modified_sequence.copy())
    return modified_sequences

def read_specific_line(file_path, line_number):
    with open(file_path, 'r') as file:
        for current_line_number, line in enumerate(file, start=1):
            if current_line_number == line_number:
                return line.strip()
    return None  # In case the line number is out of range

def extract_numbers(file_path, line_number):
    # Open the file
    with open(file_path, 'r') as file:
        # Read all lines into a list
        lines = file.readlines()

        # Check if the line number is within bounds
        if 0 <= line_number < len(lines):
            # Get the line of interest
            line = lines[line_number]

            # Find the substring between '[' and ']' and split it by ','
            numbers_str = line[line.find('[') + 1: line.find(']')].split(',')

            # Convert each number from string to integer
            numbers = [int(num.strip()) for num in numbers_str]

            return numbers
        else:
            print("Line number out of range.")
            return None

def rhs(u, p, t):
    try:
        f0 = p[0] * u[2] - p[2] * u[0] * u[5]
        f1 = p[1] * u[3] - p[3] * u[1] * u[5]
        f2 = p[2] * u[0] * u[5] - p[0] * u[2]
        f3 = p[3] * u[1] * u[5] - p[1] * u[3]
        f4 = p[6] * u[2] + p[5] * u[0] - p[9] * u[4]
        f5 = p[13] * u[4] + p[0] * u[2] + p[1] * u[3] - u[5] * (p[2] * u[0] + p[3] * u[1] + p[4] * u[7] + p[11])
        f6 = p[8] * u[3] + p[7] * u[1] - p[10] * u[6]
        f7 = p[14] * u[6] - p[4] * u[5] * u[7] + p[11] * u[8] - p[12] * u[7]
        f8 = p[4] * u[5] * u[7] - p[11] * u[8]

        # Add simple overflow check
        if np.any(np.abs([f0, f1, f2, f3, f4, f5, f6, f7, f8]) > 1e308):
            print("Overflow detected in rhs function")
            return np.zeros(9)  # Return zero array to handle overflow

        return np.array([f0, f1, f2, f3, f4, f5, f6, f7, f8])
    except OverflowError:
        print("OverflowError encountered in rhs function.")
        return np.zeros(9)  # Return zero array to handle overflow

def rk4(f, u0, p, t0, tf, n):
    t = np.linspace(t0, tf, n + 1)
    u = np.array((n + 1) * [u0])
    h = t[1] - t[0]
    for i in range(n):
        k1 = h * f(u[i], p, t[i])
        k2 = h * f(u[i] + 0.5 * k1, p, t[i] + 0.5 * h)
        k3 = h * f(u[i] + 0.5 * k2, p, t[i] + 0.5 * h)
        k4 = h * f(u[i] + k3, p, t[i] + h)
        u[i + 1] = u[i] + (k1 + 2 * (k2 + k3) + k4) / 6
    return u, t

matching_lines = []
line_number = -1
# Open the file
with open(filein, 'r') as file:
    # Iterate through each line
    for line in file:
        line_number += 1
        # Split the line by whitespace to get the first column
        columns = line.strip().split()
        first_column = columns[0]  # Assuming the first column contains the binary numbers
        # Check if the first column matches the sequence
        if first_column == thephenotype:
            matching_lines.append(line_number)
            if len(matching_lines) > 50:
                break


print(matching_lines)
iteras = 500000
seeitera = 25000

for w in matching_lines:
    # -----------------------------------
    prob = np.linspace(0.25, 2.0, 8)
    # read para values from file
    temp = extract_numbers(filein, w)

    modified_sequences = modify_sequence(temp)
    print(temp)
    print("now mutas")
    for modified_sequence in modified_sequences:
        u = np.array([1., 1., 0., 0., 0., 0., 0., 0., 0.])  # initial values
        p = np.array([50.0, 100.0, 1.0, 1.0, 2.0, 50, 500, 0.01, 50, 10, 0.5, 1, 0.2, 50, 5])  # parameters, how the u elements interact or are affected
        tosafe = []
        print(modified_sequence)
        for k in range(0, 15):
            p[k] = p[k] * prob[int(modified_sequence[k])]

        u, t = rk4(rhs, u, p, 0., 10.0, iteras)  # integrating using runge-kutta 4th order
        for j in range(1, iteras):
            if j % seeitera == 0:
                print(u[j][8])
                tosafe.append(u[j][8])
        # change format to write it nicely in file
        phenotype2 = sol_str(tosafe)
        phenotype2 = ''.join(map(str, phenotype2))

        temp = ''.join(map(str, temp))
        modified_sequence = ''.join(map(str, modified_sequence))

        print(phenotype2)
        fileout.write(f"{thephenotype} {w} {temp} {phenotype2} {modified_sequence}\n")

    print("Done with iteration number ", w)

fileout.close()

