import time
from bus import Bus
from random import randint
from utils import *

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
        self.ACTIVE = False
        self.LAST_INSTRUCTION = ""
        self.PAUSED = False
        self.INST_QUEUE = []
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
                        print("Transitioning fron I to M at address",address)
                        self.STATUS = "Transitioning from I to M at block at address {}. Placing invalidation request".format(address)
                        self.BUS.invalidateRequest(address,self.ID)
                        self.CACHE[block]["State"]="M"
                        self.CACHE[block]["Data"]=data
                        break
                # O State transitions
                elif (self.CACHE[block]["State"] == "O"):
                    if (inst == "read"):
                        # If the state is OWNED and the instruction is a READ
                        # no transition is needed
                        print("Read hit. No transition needed at address",address)
                        break
                    elif (inst == "write"):
                        # If the state is OWNED and the instruction is a write
                        # We transition to MODIFIED. Data is updated. 
                        # an INVALIDATION request is placed in the bus
                        self.BUS.invalidateRequest(address,self.ID)
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
                        self.STATUS = "Write hit while in M. No further actions needed"
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
                        self.BUS.invalidateRequest(address,self.ID)
                        self.STATUS = "Write hit. Transitioning from S to Modified state at address {}. Placing invalidation request".format(address)
                        self.CACHE[block]["Address"]=address
                        self.CACHE[block]["Data"]=data
                        self.CACHE[block]["State"]="M"
                        break
                # The exclusive state does not move when reading or writting
                # from withing itself.
                elif (self.CACHE[block]["State"] == "E"):
                    if (inst == "read"):
                        print("Read hit. No transition needed for address {}".format(address))
                        break
                    elif (inst =='write'):
                        print("Write hit. Transitioning to Modified state")
                        self.STATUS = "Write hit. Transitioning from E to Modified state at address {}. No invalidation needed".format(address)
                        self.CACHE[block]["State"]="M"
                        self.CACHE[block]["Address"]=address
                        self.CACHE[block]["Data"]=data
                        break
    
    # When there is a Cache miss we will need to insert the new address in it
    # along with the information we gathered and the state depending on who 
    # gave back the info, the instruction type and considering asociativity. 
    def insertInCache(self,address,data,state):
        ## In order to consider asociativity we calculate the set
        ## by applying a module(%) operation to the address
        ADDRESSES = {"000":0,"001":1,"010":2,"011":3,"100":4,"101":5,"110":6,"111":7}
        SET0 = ["B0","B1"]
        SET1 = ["B2","B3"]
        ## Since address is a string in binary, we map it
        ## to it's decimal value with a dictionary (ADDRESSES[address])
        SET = ADDRESSES[address]%2
        print("Address:", address, "Belings to set:",SET)
        EXISTS = False
        
        if(SET == 0):
            for block in SET0:
                # For each block in the set we check if the State 
                # is invalid in order to replace it.
                if (self.CACHE[block]["State"]=="I"):
                    self.CACHE[block]["State"]=state
                    self.CACHE[block]["Address"]=address
                    self.CACHE[block]["Data"]=data
                    #self.CACHE[block]["State"]= self.BUS.check_for_Inm(address,self.ID)
                    EXISTS = True

                    break
        elif(SET == 1):
            for block in SET1:
                # For each block in the set we check if the State 
                # is invalid in order to replace it.
                if (self.CACHE[block]["State"]=="I"):
                    self.CACHE[block]["State"]=state
                    self.CACHE[block]["Address"]=address
                    self.CACHE[block]["Data"]=data
                    EXISTS = True
                    #self.CACHE[block]["State"] = self.BUS.check_for_Inm(address,self.ID)
                    break
        if (not EXISTS):
            # We apply the replacement policy. In this case we replace a random block in the SET.
            # The block is selected by generating a value with a normal distribution and rounding said value.
            # The result of the round should be either 0 or 1. This represents the blocks in each set.
            norm = np.random.normal(loc=0.5,scale=0.225)
            norm = round(norm) # this should be 1 or 0
            if (SET == 0):
                if norm == 0:
                    #block 0
                    if self.CACHE['B0']['State']==('M' or 'O'):
                        # If this is the case then we have to write back the value before replacing it
                        #self.BUS.writeRequest(address,data,processor)
                        self.BUS.writeRequest(self.CACHE['B0']['Address'],self.CACHE['B0']['Data'],self.ID)
                    self.CACHE['B0']["State"]=state
                    self.CACHE['B0']["Address"]=address
                    self.CACHE['B0']["Data"]=data
                elif norm ==1:
                    #block 1
                    if self.CACHE['B1']['State']==('M' or 'O'):
                        # If this is the case then we have to write back the value before replacing it
                        #self.BUS.writeRequest(address,data,processor)
                        self.BUS.writeRequest(self.CACHE['B1']['Address'],self.CACHE['B1']['Data'],self.ID)
                    self.CACHE['B1']["State"]=state
                    self.CACHE['B1']["Address"]=address
                    self.CACHE['B1']["Data"]=data
            elif (SET == 1):
                if norm == 0:
                    if self.CACHE['B2']['State']==('M' or 'O'):
                        # If this is the case then we have to write back the value before replacing it
                        #self.BUS.writeRequest(address,data,processor)
                        self.BUS.writeRequest(self.CACHE['B2']['Address'],self.CACHE['B2']['Data'],self.ID)
                    #block 2
                    self.CACHE['B2']["State"]=state
                    self.CACHE['B2']["Address"]=address
                    self.CACHE['B2']["Data"]=data
                elif norm ==1:
                    if self.CACHE['B3']['State']==('M' or 'O'):
                        # If this is the case then we have to write back the value before replacing it
                        #self.BUS.writeRequest(address,data,processor)
                        self.BUS.writeRequest(self.CACHE['B3']['Address'],self.CACHE['B3']['Data'],self.ID)
                    #block 3
                    self.CACHE['B3']["State"]=state
                    self.CACHE['B3']["Address"]=address
                    self.CACHE['B3']["Data"]=data

    
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
        #value = randint(1, 3)
        value = np.random.normal(loc=0.5,scale=0.225)
        if (value>2/3): # read
            ADDRESS = self.getRandomAddress()
            print("Processor", self.ID,":read",ADDRESS)
            time.sleep(3)
            #self.updateCache("read",ADDRESS,None) 
            return "read", ADDRESS

        elif (value<1/3): # write
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
        value = poissonDistribution() # Alternative
        #value = np.random.poisson(lam=3) # We use poisson to create a a random number
        return ADDRESSES[value]
    
    # Generates a random value
    # ranging from 0 to FFFF(65535)
    def getRandomData(self):
        norm = np.random.normal(loc=0.5,scale=0.225)
        if norm > 1:
            norm =1
        elif norm < 0:
            norm = 0
        #value = randint(1,65535)
        value = round(65535 * norm)
        return str(hex(value))
    ## 
    def processorRoutine(self):
        while(self.ACTIVE):
            if not self.PAUSED:
                instruction =[] # instruction[0] -> instruction |
                                # instruction[1] -> address     |
                                # instruction[2] -> data        | 

                time.sleep(4) # the processor generates a new instrucction every 4s 
                if self.INST_QUEUE:
                    instruction = self.INST_QUEUE.pop(0)
                else:
                    instruction = self.createRandomInstruction()
                #print(instruction)
                if (instruction[0]=='read'):
                    self.CURRENT_INSTRUCTION = instruction[0]+" "+instruction[1]
                    # We check cache
                    BLOCK = self.checkCache(instruction[1]) # instruction[1] -> address     |
                    # If we hit we read memory
                    if(BLOCK):
                        print("Read hit. Showing info")
                        self.STATUS = "Read hit. No further actions required"
                        print(self.CACHE[BLOCK])
                        self.LAST_INSTRUCTION = instruction[0]+" "+instruction[1]
                    # If we miss we place a request in the bus
                    else:
                        print("Read Miss. Placing request in the bus")
                        self.STATUS = "Read Miss. Placing request in the bus"
                        # Once the memory responds we update cache with the info
                        response = self.BUS.readRequest(instruction[1],self.ID)
                        print("=================================> ",response[1])
                        self.insertInCache(instruction[1],response[0],response[1]) # 0000, 0x0001,"S"
                        self.LAST_INSTRUCTION = instruction[0]+instruction[1]
                        print("Updated Cache of processor",self.ID,":",self.CACHE)

                    pass
                elif (instruction[0]=='write'):
                    self.CURRENT_INSTRUCTION = instruction[0]+" "+instruction[1]+" "+instruction[2]
                    # We check cache
                    BLOCK = self.checkCache(instruction[1]) # B1|B2|B0
                    # If we hit we update memory
                    if(BLOCK):
                        print("Write hit. Updating cache")
                        entry = "CPU "+str(self.ID)+':'+" "+instruction[0]+" "+instruction[1]+" "+instruction[2]
                        self.BUS.LOG.append(entry)
                        #self.BUS.invalidateRequest(instruction[1]) 
                        self.STATUS = "Write Hit. Updating cache"
                        self.updateCache(instruction[0],instruction[1],instruction[2]) #  write 0000 0x0001
                        self.LAST_INSTRUCTION = instruction[0]+" "+instruction[1]+" "+instruction[2]
                        print("Updated Cache of processor",self.ID,":",self.CACHE)
                    # If we miss we place a write request in the bus
                    # An invalidation request must also be done
                    else:
                        print("Write miss. Placing requests in the bus")
                        self.STATUS ="Write miss. Placing requests in the bus"
                        self.BUS.writeRequest(instruction[1],instruction[2],self.ID) # Writting to memory the address and data
                        self.insertInCache(instruction[1],instruction[2],"M") # Storing in memory the info
                        self.LAST_INSTRUCTION = instruction[0]+" "+instruction[1]+" "+instruction[2]
                        self.BUS.invalidateRequest(instruction[1],self.ID) # Invalidating the address
                        print("Updated Cache of processor",self.ID,":",self.CACHE)
                    
                else:
                    self.STATUS = "Calc... \n No further action required"
                    self.CURRENT_INSTRUCTION = "Calc"
                    time.sleep(4) #calc takes 4s to execute
                    self.LAST_INSTRUCTION = "Calc"
                    self.BUS.LOG.append("CPU"+str(self.ID)+":  Calc")
                    pass
            else:
                pass
    
    ###
    def add_inst_to_queue(self,inst):
        self.INST_QUEUE.append(inst)
        print("Instruction added:", inst)

    ###
    def processorStep(self):
            print("Self.ID")
            instruction =[] # instruction[0] -> instruction |
                            # instruction[1] -> address     |
                            # instruction[2] -> data        | 
            if self.INST_QUEUE:
                instruction = self.INST_QUEUE.pop(0)
            else:
                instruction = self.createRandomInstruction()
            #print(instruction)
            if (instruction[0]=='read'):
                self.CURRENT_INSTRUCTION = instruction[0]+" "+instruction[1]
                # We check cache
                BLOCK = self.checkCache(instruction[1]) # instruction[1] -> address     |
                # If we hit we read memory
                if(BLOCK):
                    print("Read hit. Showing info")
                    self.STATUS = "Read hit. No further actions required"
                    print(self.CACHE[BLOCK])
                    self.LAST_INSTRUCTION = instruction[0]+" "+instruction[1]
                # If we miss we place a request in the bus
                else:
                    print("Read Miss. Placing request in the bus")
                    self.STATUS = "Read Miss. Placing request in the bus"
                    # Once the memory responds we update cache with the info
                    response = self.BUS.readRequest(instruction[1],self.ID)
                    print("=================================> ",response[1])
                    self.insertInCache(instruction[1],response[0],response[1]) # 0000, 0x0001,"S"
                    self.LAST_INSTRUCTION = instruction[0]+instruction[1]
                    print("Updated Cache of processor",self.ID,":",self.CACHE)
            elif (instruction[0]=='write'):
                self.CURRENT_INSTRUCTION = instruction[0]+" "+instruction[1]+" "+instruction[2]
                # We check cache
                BLOCK = self.checkCache(instruction[1]) # B1|B2|B0
                # If we hit we update memory
                if(BLOCK):
                    print("Write hit. Updating cache")
                    entry = "CPU "+str(self.ID)+':'+" "+instruction[0]+" "+instruction[1]+" "+instruction[2]
                    self.BUS.LOG.append(entry)
                    self.BUS.invalidateRequest(instruction[1],self.ID) 
                    self.updateCache(instruction[0],instruction[1],instruction[2]) #  write 0000 0x0001
                    self.STATUS = "Write Hit. Placing invalidation request in the Bus. Updating cache"
                    self.LAST_INSTRUCTION = instruction[0]+" "+instruction[1]+" "+instruction[2]
                    print("Updated Cache of processor",self.ID,":",self.CACHE)
                # If we miss we place a write request in the bus
                # An invalidation request must also be done
                else:
                    print("Write miss. Placing requests in the bus")
                    self.STATUS ="Write miss. Placing requests in the bus"
                    self.BUS.writeRequest(instruction[1],instruction[2],self.ID) # Writting to memory the address and data
                    self.insertInCache(instruction[1],instruction[2],"M") # Storing in memory the info
                    self.LAST_INSTRUCTION = instruction[0]+" "+instruction[1]+" "+instruction[2]
                    self.BUS.invalidateRequest(instruction[1],self.ID) # Invalidating the address
                    print("Updated Cache of processor",self.ID,":",self.CACHE)
                    
            else:
                self.STATUS = "Calc... \n No further action required"
                self.CURRENT_INSTRUCTION = "Calc"
                time.sleep(4)
                self.LAST_INSTRUCTION = "Calc"
                self.BUS.LOG.append("CPU"+str(self.ID)+":  Calc")
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
            self.BUS.invalidateRequest(address,self.ID)
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