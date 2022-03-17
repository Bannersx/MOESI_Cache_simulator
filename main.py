import threading
from time import sleep
from processor import *
from memory import *
from bus import *
CPU_NUM = 4
MEMORY_SIZE = 8

def main():
    # SET UP
    CPUS = []
    MEMORY = Memory()
    BUS = Bus(MEMORY)
    for i in range(CPU_NUM):
        CPUS.append(Processor(i,BUS))
    """ BUS.writeRequest("000","0x1234")
    print("Writting from CPU")
    CPUS[0].write("011","0x5678") """
    BUS.PROCESSORS=CPUS
    """ CPUS[3].CACHE = { 
                    "B0":
                        {"Data":"1234", "Address":"000","State":"M"},
                    "B1":
                        {"Data":"6666", "Address":"010","State":"E"}, 
                    "B2":
                        {"Data":"", "Address":"011","State":"S"}, 
                    "B3":
                        {"Data":"", "Address":"100","State":"S"}
                        } """
    ### Read testing example.
    
    print("\n Before (CPU0): ",CPUS[0].CACHE)
    print(" Before (CPU3): ",CPUS[3].CACHE)

    print("\n -------------- READING NOW----------------------")
    CPUS[0].read("000")
    print("\n After (CPU0): ",CPUS[0].CACHE)
    print(" After (CPU3): ",CPUS[3].CACHE)
    print("\n")
    print("\n -------------- READING NOW----------------------")
    CPUS[3].read("000")
    print("\n -------------- READING NOW----------------------")
    CPUS[0].read("011")
    print("\n Finally (CPU0): ",CPUS[0].CACHE)
    print(" Finally (CPU3): ",CPUS[3].CACHE)
    print("\n")
    CPUS[3].write("000","8888")
    print("\n After writting (CPU0): ",CPUS[0].CACHE)
    print(" After writting (CPU3): ",CPUS[3].CACHE) 

    ### Writting test example.
    """ print("\n Before (CPU0): ",CPUS[0].CACHE)
    print(" Before (CPU3): ",CPUS[3].CACHE)
    CPUS[0].write("000","7777")
    print("\n After (CPU0): ",CPUS[0].CACHE)
    print(" After (CPU3): ",CPUS[3].CACHE)
    CPUS[0].write("000","9999")
    CPUS[0].read("000")
    print("\n Finally (CPU0): ",CPUS[0].CACHE)
    MEMORY.printMemory()
    CPUS[2].write("000","2222")
    print("\n At last (CPU0): ",CPUS[0].CACHE)
    print(" At last (CPU3): ",CPUS[3].CACHE)
    MEMORY.printMemory() """
    ### Thread example
    """
    try:
        t1 = threading.Thread(target=CPUS[0].processorRoutine, args=[])
        t1.start()
        t2 = threading.Thread(target=CPUS[1].processorRoutine, args=[])
        t2.start() 
        t3 = threading.Thread(target=CPUS[2].processorRoutine, args=[])
        t3.start()
        t4 = threading.Thread(target=CPUS[3].processorRoutine, args=[])
        t4.start() 
        sleep(15)
        CPUS[0].ACTIVE = False
        CPUS[1].ACTIVE = False
        CPUS[2].ACTIVE = False
        CPUS[3].ACTIVE = False
        sleep(3)
        print("Final State of the system")
        MEMORY.printMemory()
        print("CP0",CPUS[0].CACHE)
        print("CP1",CPUS[1].CACHE)
        print("CP2",CPUS[2].CACHE)
        print("CP3",CPUS[3].CACHE)
        BUS.printLog()
    except:
        print("Error: unable to start thread")
    """

if __name__ == '__main__':
    main()