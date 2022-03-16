
def poissonDistribution():
    lambdaValue = 4
    # e^-lambda
    p = 1.0
    k = 0
    pass

def normalDistribution():
    u = 0
    v = 0
    pass

### Cache associativity mapping
ADDRESSES = {"000":0,"001":1,"010":2,"011":3,"100":4,"101":5,"110":6,"111":7}
SET0 = ["B0","B1"]
SET1 = ["B2","B3"]
address = '000'
SET = ADDRESSES[address]%2
print("Set:", SET)
match SET:
    case 0:
        for block in SET0:
            print(block)
    case 1:
        for block in SET1:
            print(block)