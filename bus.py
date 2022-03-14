from memory import Memory
class Bus:
    def __init__(self, memory):
        self.MEMORY = memory
        self.PROCESSORS= []
        self.LOG=[]
        pass

    # This function must set a request to invalidate data in cache for a given address
    # For example [invalidate 000]
    def invalidateRequest(self,address):
        for proc in self.PROCESSORS:
            for block in proc.CACHE:
                if (proc.CACHE[block]["Address"]==address):
                    proc.CACHE[block]["State"]="I"

        
    def findDataInCache(self,address):
        for proc in self.PROCESSORS:
            for block in proc.CACHE:
                # If we find the value in a Modified cache
                if (proc.CACHE[block]["Address"]==address and proc.CACHE[block]["State"]=="M"):
                    # The MODIFIED cache is set to OWNER
                    proc.CACHE[block]["State"]="O"
                    print("Updated Cache of processor",proc.ID,":",proc.CACHE)
                    # And we return the DATA
                    return proc.CACHE[block]["Data"]
                # If we find the value in an Exlusive cache    
                elif (proc.CACHE[block]["Address"]==address and (proc.CACHE[block]["State"]=="E" or proc.CACHE[block]["State"]=="S")):
                    # The exclusive cache is set to Shared
                    proc.CACHE[block]["State"]="S"
                    print("Updated Cache of processor",proc.ID,":",proc.CACHE)
                    return proc.CACHE[block]["Data"]
        return None


    # This function has to alert other processors that there is a read request for a given 
    # address if there is a cache in another processor with valid data for that address the 
    # request is answered and cache status is updated accordingly. Data will be retrieved
    # from memory otherwise.
    def readRequest(self,address,processor):
        # Find data in memory()
        # If data is in cache somewhere then we take the value an set the State to SHARED
        DATA = self.findDataInCache(address)
        self.LOG.append({"Processor":processor, "instruction":"read", "address":address})
        if (DATA):
            return DATA,"S"
        else:
            # If DATA is not in cache then we have to access memory
            # To simulate the wall effect we have to wait X amount of time
            DATA = self.MEMORY.readFromAddress(address)
            return DATA, "E"
            

    def writeRequest(self,address,data,processor):
        # This function will be in charge of writting the new data to memory
        # Should check if the data is in another CPU with a valid State.
        self.MEMORY.writeToAddress(address,data)
        self.MEMORY.printMemory()
        self.LOG.append({"Processor":processor, "instruction":"write", "address":address, "data":data})
        
    def printLog(self):
        print("\n Printing Log:")
        for entry in self.LOG:
            print(entry)