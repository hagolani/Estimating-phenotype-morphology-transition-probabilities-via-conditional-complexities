# From Chico adapted for Python 3.X
# Code previously from Ben Frot
# Originally from XXX paper
import numpy as np

def KC_LZ(string):
    n=len(string)
    s = '0'+string
    c=1
    l=1
    i=0
    k=1
    k_max=1
    stop=0

    while stop==0:
        if s[i+k] != s[l+k]:
            if k>k_max:
                k_max=k

            i=i+1
            
            if i==l:
                c=c+1
                l=l+k_max

                if l+1>n:
                    stop=1

                else:
                    i=0
                    k=1
                    k_max=1
            else:
                k=1

        else:
            k=k+1

            if l+k>n:
                c=c+1
                stop=1



    # a la Lempel and Ziv (IEEE trans inf theory it-22, 75 (1976), 
    # h(n)=c(n)/b(n) where c(n) is the kolmogorov complexity
    # and h(n) is a normalised measure of complexity.
    complexity=c;

    #b=n*1.0/np.log2(n)
    #complexity=c/b;

    return complexity


def calc_KC(s):
    L = len(s)
    if s == '0'*L or s == '1'*L:
        return np.log2(L)
    else:
        return np.log2(L)*(KC_LZ(s)+KC_LZ(s[::-1]))/2.0
