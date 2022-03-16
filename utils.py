from math import exp
import numpy as np
def poissonDistribution():
    lambdaValue = 2
    # e^-lambda
    L = exp(-lambdaValue)
    p = 1.0
    k = 0
    while (p>L):
        k=k+1
        p=np.random.rand()
    result = k -1
    
    if (result >=7):
        return 7
    else: return result

def normalDistribution():
    u = 0
    v = 0
    pass

### Cache associativity mapping
#ADDRESSES = {"000":0,"001":1,"010":2,"011":3,"100":4,"101":5,"110":6,"111":7}
#SET0 = ["B0","B1"]
#SET1 = ["B2","B3"]
#address = '000'
#SET = ADDRESSES[address]%2
#print("Set:", SET)



"""
### match is only available for python 3.10<
match SET:
    case 0:
        for block in SET0:
            print(block)
    case 1:
        for block in SET1:
            print(block)
"""
## Option 1 for Poisson
"""
poiss = np.random.poisson(lam=3)
if poiss < 2:
    print("write")
elif poiss > 3:
    print("read")
else: print("calc")
nrom = np.random.normal(loc=0.5,scale=0.225)
print(nrom)
if nrom < 1/3:
    print("write")
elif nrom > 2/3:
    print("read")
else: print("calc")
print("Poiss:", poiss)
print("Data",65535*nrom)
print(poissonDistribution())
"""