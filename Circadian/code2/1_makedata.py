#simulates the concentration changes of some interacting variables (u) according to some parameters (p)
import numpy as np
from math import sqrt
import random as rm
import matplotlib.pyplot as plt

# Initializing files and arrays
file1 = open("parameters.txt", "w")
file2 = open("solution.txt", "w")

def rhs(u, p, t):
    f0= p[0]*u[2]      - p[2]*u[0]*u[5]
    f1= p[1]*u[3]      - p[3]*u[1]*u[5]
    f2= p[2]*u[0]*u[5] - p[0]*u[2] 
    f3= p[3]*u[1]*u[5] - p[1]*u[3]
    f4= p[6]*u[2]      + p[5]*u[0]     - p[9]*u[4]
    f5= p[13]*u[4]     + p[0]*u[2]     + p[1]*u[3]- u[5]*(p[2]*u[0]+p[3]*u[1]+p[4]*u[7]+p[11])
    f6= p[8]*u[3]      + p[7]*u[1]     - p[10]*u[6]
    f7= p[14]*u[6]     - p[4]*u[5]*u[7]+ p[11]*u[8]-p[12]*u[7]
    f8= p[4]*u[5]*u[7] - p[11]*u[8]
    return np.array([f0, f1, f2, f3, f4, f5, f6, f7, f8])

def rk4(f, u0, p, t0, tf , n):
    t = np.linspace(t0, tf, n+1)
    u = np.array((n+1)*[u0])
    h = t[1]-t[0]
    for i in range(n):
        k1 = h * f(u[i], p, t[i])    
        k2 = h * f(u[i] + 0.5 * k1, p, t[i] + 0.5*h)
        k3 = h * f(u[i] + 0.5 * k2, p, t[i] + 0.5*h)
        k4 = h * f(u[i] + k3, p, t[i] + h)
        u[i+1] = u[i] + (k1 + 2*(k2 + k3 ) + k4) / 6
    return u, t


for ff in range(1,2000000): 
 file_name = "parameters" + str(ff) + ".txt"   
 file1 = open(file_name, "w")
 file_name = "solution" + str(ff) + ".txt"     
 file2 = open(file_name, "w")   
 for w in range(0,100):     # lines Added by Umar
    u = np.array([1., 1., 0. , 0., 0., 0., 0., 0., 0.])  #variables , concentrations of something for example
    p = np.array([50.0, 100.0, 1.0, 1.0, 2.0, 50, 500, 0.01, 50, 10, 0.5, 1, 0.2, 50, 5]) #parameters, how the u elements interact or are afected
    # lines Added by Umar
#-----------------------------------    
    prob = np.linspace(0.25, 2.0, 8)
#    print(prob)

    temp = []
    for k in range(0,15):
        index = rm.randint(0,7)     # it must be (0,7) but working for (0,3)
        temp.append(index)
#    print(temp)
    file1.write(str(temp)+'\n')
    
    for k in range (0,15):
        p[k] = p[k]*prob[int(temp[k])]    #randomly modifiying p
#    print(p)
    file1.write(str(p)+'\n')
#-----------------------------------    
    u, t = rk4(rhs, u, p, 0., 10.0, 500000)   #integrating using runge-kutta 4th order
#    e1, e2, e3, e4, e5, e6, e7, e8, e9 = u.T
#    print(len(u))
    for j in range(1,500000):
        if j % 25000 == 0:
            file2.write(str(u[j][8])+'\n')
            print(j,'----------',u[j][8])
    print(u[500000][8])
    print("Done with iteration number ", w)
    #plt.figure(1)
    #ax = plt.gca()
    #ax.grid(True)
    #np.linspace(0,10,200000)
    #plt.plot(t,u)
    #plt.xlabel(" time")
    #plt.ylabel("Concentration")
    #plt.legend(["Da","Dr","Da'","Dr'","Ma","A","Mr","R","C"])
    #plt.show()
file1.close()
file2.close()
