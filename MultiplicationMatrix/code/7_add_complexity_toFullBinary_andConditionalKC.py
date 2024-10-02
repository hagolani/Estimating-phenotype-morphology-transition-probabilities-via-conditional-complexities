import numpy as np
import sys

def KC_LZ(string):
    n = len(string)
    s = '0' + string
    c = 1
    l = 1
    i = 0
    k = 1
    k_max = 1
    stop = 0

    while stop == 0:
        if s[i + k] != s[l + k]:
            if k > k_max:
                k_max = k

            i = i + 1

            if i == l:
                c = c + 1
                l = l + k_max

                if l + 1 > n:
                    stop = 1
                else:
                    i = 0
                    k = 1
                    k_max = 1
            else:
                k = 1
        else:
            k = k + 1

            if l + k > n:
                c = c + 1
                stop = 1

    return c

def calc_KC(s):
    L = len(s)
    if s == '0' * L or s == '1' * L:
        return np.log2(L)
    else:
        return np.log2(L) * (KC_LZ(s) + KC_LZ(s[::-1])) / 2.0

def process_file(input_file, output_file,argument):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        #header = infile.readline().strip()
        outfile.write("genotype phenotype count KC Conditional_Complexity\n")

        for line in infile:
            parts = line.strip().split()
            if len(parts) < 1:
                continue  # Skip lines that don't have enough columns
            col1 = parts[1]  ; col4 = argument          
            KC_col1 = calc_KC(col1)           
            
            k1 = round(KC_col1, 5)
            str_arrlist_con = [col1 + col4]# for _ in range(len(col4))]  # using col4 multiple times to form concatenated strings
            Z = [round(calc_KC(s), 5) for s in str_arrlist_con]
            Z1 = np.array(Z) - k1
            #print("z1", Z1)
            conditional_complexity = np.mean(Z1)

            
            outfile.write(line.strip() + f" {KC_col1:.5f} {conditional_complexity:.5f}\n")


argument = sys.argv[1]
input_file = 'in_out_count.txt'
#output_file = "in_out_count_KC.txt"
output_file = "in_out_count_"+argument+"_KC_new2.txt"
process_file(input_file, output_file,argument)

