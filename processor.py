import time
from bus import Bus
from random import randint

class Processor:
    def __init__(self, id, bus):
        self.ID = id
        self.CACHE = { 
                    "B0":
                        {"State":"I","Data":"0x0000", "Address":"0000"},
                    "B1":
                        {"State":"I","Data":"0x0000", "Address":"0000"}, 
                    "B2":
                        {"State":"I","Data":"0x0000", "Address":"0000"}, 
                    "B3":
                        {"State":"I","Data":"0x0000", "Address":"0000"}
                        }
        self.STATUS = "Waiting..."
        self.CURRENT_INSTRUCTION = ""
        self.BUS = bus
        self.ACTIVE = True

    # Main function to update the state of the blocks
    def updateCache(self, inst, address, data):
        for block in self.CACHE:
            # Here we check the current state and set the state to the corresponding
            # state according to MOESI
            if self.CACHE[block]["Address"] == address:
                # I state transitions
                if self.CACHE[block]["State"] == "I":
                    if (inst == "read"):
                        # If the state is INVALID and the instruction is a READ
                        # we transition to EXCLUSIVE
                        print("Transitioning from I to E at block",block)
                        self.CACHE[block]["State"]="E"
                        break
                    elif (inst == "write"):
                        # If the state is INVALID and the instruction is WRITE
                        # we transition to MODIFIED
                        print("Transitioning fron I to M")
                        self.CACHE[block]["State"]="M"
                        break
                # O State transitions
                elif (self.CACHE[block]["State"] == "O"):
                    if (inst == "read"):
                        # If the state is OWNED and the instruction is a READ
                        # no transition is needed
                        print("Read hit. No transition needed",block)
                        break
                    elif (inst == "write"):
                        # If the state is OWNED and the instruction is a write
                        # We transition to MODIFIED. Data is updated. 
                        # an INVALIDATION request is placed in the bus
                        self.BUS.invalidateRequest(address)
                        self.CACHE[block]["Address"]=address
                        self.CACHE[block]["Data"]=data
                        self.CACHE[block]["State"]="M"
                        break
                # M state transitions
                elif (self.CACHE[block]["State"] == "M"):
                    if (inst == "read"):
                        # This transitions to OWNED if the processor is different.
                        break
                    elif (inst == "write"):
                        # If the state is MODIFIED and the instruction is a WRITE
                        # No transition is needed. Data is updated.
                        self.CACHE[block]["Address"]=address
                        self.CACHE[block]["Data"]=data
                        break
                # S state transitions
                elif (self.CACHE[block]["State"] == "S"):
                    if (inst == "read"):
                        # If the state is SHARED and the instruction is READ
                        # No transition is needed
                        break
                    elif (inst == "write"):
                        # If the state is SHARED and the instruction is a WRITE
                        # DATA is to be updated. State transitions to MODIFIED
                        # and an INVALIDATION request is placed in the bus
                        self.BUS.invalidateRequest(address)
                        self.CACHE[block]["Address"]=address
                        self.CACHE[block]["Data"]=data
                        self.CACHE[block]["State"]="M"
                        break
                # The exclusive state does not move when reading or writting
                # from withing itself.
                elif (self.CACHE[block]["State"] == "E"):
                    if (inst == "read"):
                        print("Read hit. No transition needed")
                        break
                    elif (inst =='write'):
                        print("Write hit. Transitioning to Modified state")
                        self.CACHE[block]["State"]="M"
                        self.CACHE[block]["Address"]=address
                        self.CACHE[block]["Data"]=data
                        break
    
    # When there is a Cache miss we will need to insert the new address in it
    # along with the information we gathered and the state depending on who 
    # gave back the info nd the instructions type. 
    def insertInCache(self,address,data,state):
        EXISTS = False
        for block in self.CACHE:
            if (self.CACHE[block]["State"]=="I"):
                self.CACHE[block]["State"]=state
                self.CACHE[block]["Address"]=address
                self.CACHE[block]["Data"]=data
                EXISTS = True
                break
        if (not EXISTS):
            # We apply a replace policy
            pass
    
    # This functions checks if the address is in cache
    # If the address is in cache, it returns the block
    # If the address is not in cache it returns None
    def checkCache(self,address):
        returnBlock = None
        for block in self.CACHE:
            if (self.CACHE[block]["Address"] == address and self.CACHE[block]["State"] != "I"):
                returnBlock = block
        return returnBlock
    
    """ Example of usage for checkCache(addr)
    block = CPUS[0].checkCache("010")
        if (block):
            print("YAS")
        print(block)
    """

    
    # This functions is in charge of creating a random instruction 
    # the results available are read, write, calc
    def createRandomInstruction(self):
        INSTRUCTIONS =["read",'write','calc']
        value = randint(1, 3)

        if (value==1): # read
            ADDRESS = self.getRandomAddress()
            print("Processor", self.ID,":read",ADDRESS)
            time.sleep(3)
            #self.updateCache("read",ADDRESS,None) 
            return "read", ADDRESS

        elif (value==2): # write
            ADDRESS = self.getRandomAddress()
            DATA = self.getRandomData()
            print("Processor", self.ID,":write", ADDRESS, DATA)
            time.sleep(3)
            #self.write(ADDRESS,DATA)
            #self.updateCache("write",ADDRESS,DATA) 
            return "write", ADDRESS, DATA

        else:               # calc
            print("Processor", self.ID,":Calc")
            time.sleep(2)
            return ["Calc"]

    # Generates a random address
    # The address goes from 0 to 7
    # 8 blocks of memory 
    def getRandomAddress(self):
        ADDRESSES = ["000","001","010","011","100","101","110","111"]
        value = randint(0, 7)
        return ADDRESSES[value]
    
    # Generates a random value
    # ranging from 0 to FFFF
    def getRandomData(self):
        value = randint(1,65535)
        return str(hex(value))
    ## 
    def processorRoutine(self):
        while(self.ACTIVE):
            instruction =[] # instruction[0] -> instruction |
                            # instruction[1] -> address     |
                            # instruction[2] -> data        | 
            instruction = self.createRandomInstruction()
            #print(instruction)
            if (instruction[0]=='read'):
                # We check cache
                BLOCK = self.checkCache(instruction[1]) # instruction[1] -> address     |
                # If we hit we read memory
                if(BLOCK):
                    print("Read hit. Showing info")
                    print(self.CACHE[BLOCK])
                # If we miss we place a request in the bus
                else:
                    print("Read Miss. Placing request in the bus")
                    # Once the memory responds we update cache with the info
                    response = self.BUS.readRequest(instruction[1],self.ID)
                    self.insertInCache(instruction[1],response[0],response[1]) # 0000, 0x0001,"S"
                    print("Updated Cache of processor",self.ID,":",self.CACHE)

                pass
            elif (instruction[0]=='write'):
                # We check cache
                BLOCK = self.checkCache(instruction[1]) # B1|B2|B0
                # If we hit we update memory
                if(BLOCK):
                    print("Write hit. Updating cache")
                    self.updateCache(instruction[0],instruction[1],instruction[2]) #  write 0000 0x0001
                    print(self.CACHE)
                    print("Updated Cache of processor",self.ID,":",self.CACHE)
                # If we miss we place a write request in the bus
                # An invalidation request must also be done
                else:
                    print("Write miss. Placing requests in the bus")
                    self.BUS.invalidateRequest(instruction[1]) # Invalidating the address
                    self.BUS.writeRequest(instruction[1],instruction[2],self.ID) # Writting to memory the address and data
                    self.insertInCache(instruction[1],instruction[2],"M") # Storing in memory the info
                    print("Updated Cache of processor",self.ID,":",self.CACHE)
                
            else:
                self.STATUS = "Calc... \n No further action required"
                pass

#################################### Debugging Functions #######################################################
    # This function sets a write request to the bus
    # 
    def write(self, address,data):
        print("\nProcessor ID: ", self.ID, "is trying to write data in address....", address)

        BLOCK = self.checkCache(address)
        
        if(BLOCK):
            print("Write hit. Updating cache")
            self.updateCache("write",address,data)
            print(self.CACHE)
        else:
            print("Write miss. Placing requests in the bus.")
            self.BUS.invalidateRequest(address)
            self.BUS.writeRequest(address,data,self.ID)
            self.insertInCache(address,data,"M")

    # This function sets a read request to the bus
    # 
    def read(self,address):
        BLOCK = self.checkCache(address)
        # If we hit we read memory
        if(BLOCK):
            print("Found: ",self.CACHE[BLOCK])
        # If we miss we place a request in the bus
        else:
            print("Read Miss. Placing request in the bus")
            # Once the memory responds we update cache with the info
            response = self.BUS.readRequest(address,self.ID)
            self.insertInCache(address,response[0],response[1])
        pass
# --------- Driver ------------------
#proc = Processor(1,{})

#print(proc["B0"]["address"])