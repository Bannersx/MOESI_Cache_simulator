class Memory:
    def __init__(self):
        self.BLOCKS = {
            "000":"0x0000",
            "001":"0x0000",
            "010":"0x0000",
            "011":"0x0000",
            "100":"0x0000",
            "101":"0x0000",
            "110":"0x0000",
            "111":"0x0000",
        }
    def writeToAddress(self, address, data):
        self.BLOCKS[address] = data

    def readFromAddress(self,address):
        return self.BLOCKS[address]

    def printMemory(self):
        print("\n Current State of Memory:")
        print(self.BLOCKS)
# Driver example
""" test = Memory()
print("Before: ", test.readFromAddress("000"))
print("Writting data: 0x1234 to address: 000")
test.writeToAddress("000","0x1234")
print("After: ", test.readFromAddress("000")) """