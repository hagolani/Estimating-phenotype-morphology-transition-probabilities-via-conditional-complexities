import numpy as np
import sys

file = open("matrix_D.txt",'w')
file0 = open("in_out_str.txt",'w')
file1 = open("in_str.txt",'w')
file2 = open("out_str.txt",'w')

arguments = sys.argv
# First argument is the script name, following arguments are user-provided
if len(arguments) > 1:
    n = int(arguments[1])
    #print("User provided input:", user_input)
print(n)

#n = 18   # length of string

mat_D = np.random.randint(-1,2, size=(n, n))
#print(mat_D)

content = str(mat_D)
file.write(content)

def generate_binary(n, l):
    if n == 0:
        return l
    else:
        if len(l) == 0:
            return generate_binary(n-1, ["0", "1"])
        else:
            return generate_binary(n-1, [i + "0" for i in l] + [i + "1" for i in l])

str_g = generate_binary(n,[])
#print(str_g)

list_g = []
def generate_list(str_g):
    for i in range(0,len(str_g)):
        w1 = str_g[i]
        w2 = [i for a,i in enumerate(w1) ]
        list_g.append(w2)
    
    return list_g

list_g = generate_list(str_g)

#print(list_g)

arr_g = []
def generate_array(list_g):
    for i in range(0,len(list_g)):
        w1 = list_g[i]
        w2 = [int(x) for x in w1 ]
        arr_g.append(w2)
    return arr_g

arr_g = generate_array(list_g)

#print(arr_g)
#print(np.add(array_g[1],array_g[6]))

prod_Dg = []

def mat_vec_multiply(mat_D,arr_g):
    for vector in arr_g:
    # Multiply the vector with matrix A
        result = np.dot(mat_D,vector)
    # Append the result to the list
        prod_Dg.append(result)
    return prod_Dg

prod_Dg = mat_vec_multiply(mat_D,arr_g)
#print(prod_Dg)
#print(len(prod_Dg))

array_P = []

def generate_output(prod_Dg):
    for i in range(0,len(prod_Dg)):
        w = prod_Dg[i]
        for j in range(0,len(w)):
            if w[j] > 0:
                array_P.append("1")
            else:
                array_P.append("0")
    return array_P

array_P = generate_output(prod_Dg)

#print(array_P)
#print(len(array_P))

list_to_str = []

def generate_str(array_P):
    start = 0
    end = n
    for i in range(0,int(len(array_P)/n)):
        a1 = array_P[start:end]
#        print(a1)
        list_to_str.append("".join(a1))
        start = start + n
        end = end + n
    return list_to_str

list_to_str = generate_str(array_P)
print(list_to_str)
#print(len(list_to_str))

# for writing files 

list_g_to_str = []
def generate_str_for_g(list_g):
    for i in range(0,len(list_g)):
        b1 = list_g[i]
#        print(b1)
        list_g_to_str.append("".join(b1))
    return list_g_to_str

list_g_to_str = generate_str_for_g(list_g)
print(list_g_to_str)

for i in range(0,len(list_to_str)):
    file1.write(list_g_to_str[i])
    file1.write("\n")
    file2.write(list_to_str[i])
    file2.write("\n")
for i in range(0,len(list_to_str)):
    file0.write(list_g_to_str[i])
    file0.write("\t")
    file0.write(list_to_str[i])
    file0.write("\n")

print("Bingooooooooooo!")
file.close()
file0.close()
file1.close()
file2.close()
