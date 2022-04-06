from time import sleep
from turtle import width
import threading
import tkinter as tk
from tkinter import *
from tkinter import font as tkfont
import tkinter.ttk as ttk
from processor import *
from bus import *
from memory import *
import re

mem_map = {0:"000",1:"001",2:"010",3:"011",4:"100",5:"101",6:"110",7:"111"}
#F5F5F2
class SampleApp(tk.Tk):

    def __init__(self,processors,memory,bus, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=22, weight="bold", slant="italic")
        self.title("MOESI CACHE SIMULATOR")
        self.geometry("1550x1000")

        #tkt = tkthread.TkThread(self)
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self,processors=processors,memory=memory,bus=bus)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")
        self.mainloop()

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller,processors,memory,bus):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the start page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=30)

        button1 = tk.Button(self, text="Simulator",
                            command=lambda: controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="Information",
                            command=lambda: controller.show_frame("PageTwo"))
        button3 = tk.Button(self, text="Exit",
                            command=self.exitFunction)
        button1.pack(pady=20)
        button2.pack()
        button3.pack()

    def exitFunction(self):
        tk.Tk.quit(self)

class PageOne(tk.Frame):

    def __init__(self, parent, controller,processors,memory,bus):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.processors = processors
        self.memory = memory
        self.bus = bus
        ### Cache 1
        self.CACHE1_L1_1 = ""
        self.CACHE1_L1_2 = ""
        self.CACHE1_L1_3 = ""
        self.CACHE1_L1_4 = ""
        ### Cache 2
        self.CACHE2_L1_1 = ""
        self.CACHE2_L1_2 = ""
        self.CACHE2_L1_3 = ""
        self.CACHE2_L1_4 = ""
        ### Cache 3
        self.CACHE3_L1_1 = ""
        self.CACHE3_L1_2 = ""
        self.CACHE3_L1_3 = ""
        self.CACHE3_L1_4 = ""
        ### Cache 4
        self.CACHE4_L1_1 = ""
        self.CACHE4_L1_2 = ""
        self.CACHE4_L1_3 = ""
        self.CACHE4_L1_4 = ""
        ### Controllers
        self.CONTROLLER_1 = ""
        self.CONTROLLER_2 = ""
        self.CONTROLLER_3 = ""
        self.CONTROLLER_4 = ""
        self.MEMORY = []
        self.CURRENT =[]
        self.LAST =   []
        label = tk.Label(self, text="", font=controller.title_font)
        label.place(x=670,y=20)
        
        # Constructing the elements.
        # Entire Rectangle of the CPU
        CPU1 = tk.Canvas(self,height=450,width=350,bg="#1482FA")
        CPU2 = tk.Canvas(self,height=450,width=350,bg="#1482FA")
        CPU3 = tk.Canvas(self,height=450,width=350,bg="#1482FA")
        CPU4 = tk.Canvas(self,height=450,width=350,bg="#1482FA")
        
        # Controller Message
        self.CONTROLLER_1 = tk.Text(self, height = 4, width = 35)
        self.CONTROLLER_2 = tk.Text(self, height = 4, width = 35)
        self.CONTROLLER_3 = tk.Text(self, height = 4, width = 35)
        self.CONTROLLER_4 = tk.Text(self, height = 4, width = 35)
        
        CPU1.place(x=30,y=65)
        CPU2.place(x=410,y=65)
        CPU3.place(x=790,y=65)
        CPU4.place(x=1170,y=65)
        self.CONTROLLER_1.place(x=65,y=360)
        self.CONTROLLER_2.place(x=445,y=360)
        self.CONTROLLER_3.place(x=825,y=360)
        self.CONTROLLER_4.place(x=1205,y=360)

        # CPU ID Label
        CPU1.create_text(175,20, fill="White", text="CPU 1",font=tkfont.Font(family='Times', size=16, weight="bold"))
        CPU2.create_text(175,20, fill="White", text="CPU 2",font=tkfont.Font(family='Times', size=16, weight="bold"))
        CPU3.create_text(175,20, fill="White", text="CPU 3",font=tkfont.Font(family='Times', size=16, weight="bold"))
        CPU4.create_text(175,20, fill="White", text="CPU 4",font=tkfont.Font(family='Times', size=16, weight="bold"))

        # Controller Label
        CPU1.create_text(175,270, fill="White", text="CONTROLLER",font=tkfont.Font(family='Times', size=16, weight="bold"))
        CPU2.create_text(175,270, fill="White", text="CONTROLLER",font=tkfont.Font(family='Times', size=16, weight="bold"))
        CPU3.create_text(175,270, fill="White", text="CONTROLLER",font=tkfont.Font(family='Times', size=16, weight="bold"))
        CPU4.create_text(175,270, fill="White", text="CONTROLLER",font=tkfont.Font(family='Times', size=16, weight="bold"))
        
        # Current and Last instruction
        CPU1.create_text(85,390, fill="White", text="Current Ins",font=tkfont.Font(family='Times', size=16, weight="bold"))
        CPU1.create_text(265,390, fill="White", text="Last Ins",font=tkfont.Font(family='Times', size=16, weight="bold"))
        CPU2.create_text(85,390, fill="White", text="Current Ins",font=tkfont.Font(family='Times', size=16, weight="bold"))
        CPU2.create_text(265,390, fill="White", text="Last Ins",font=tkfont.Font(family='Times', size=16, weight="bold"))
        CPU3.create_text(85,390, fill="White", text="Current Ins",font=tkfont.Font(family='Times', size=16, weight="bold"))
        CPU3.create_text(265,390, fill="White", text="Last Ins",font=tkfont.Font(family='Times', size=16, weight="bold"))
        CPU4.create_text(85,390, fill="White", text="Current Ins",font=tkfont.Font(family='Times', size=16, weight="bold"))
        CPU4.create_text(265,390, fill="White", text="Last Ins",font=tkfont.Font(family='Times', size=16, weight="bold"))
        c_x = 55
        l_x = 235 
        for i in range(4):
            self.CURRENT.append(tk.Text(self, height = 1, width =17, font=tkfont.Font(family='Helvetica', size=10, weight="bold"),bg="#022366",fg="white"))
            self.LAST.append(tk.Text(self, height = 1, width = 17, font=tkfont.Font(family='Helvetica', size=10, weight="bold"),bg="#022366",fg="white"))
            self.CURRENT[i].place(x=c_x,y=470)
            self.LAST[i].place(x=l_x,y=470)
            c_x = c_x + 380
            l_x = l_x + 380

    ###### # Cache for CPU1
        ### B0
        CPU1.create_text(45,90,fill = "white",text="B0",font=tkfont.Font(family='Helvetica', size=14, weight="bold"))
        self.CACHE1_L1_1 = tk.Text(self, height = 4, width = 10, font=tkfont.Font(family='Helvetica', size=14, weight="bold"),bg="#bde3ff")
        for key in self.processors[0].CACHE['B0']:
            self.CACHE1_L1_1.insert(END, self.processors[0].CACHE['B0'][key]+"\n")
        self.CACHE1_L1_1.place(x=92,y=110)
        ### B1
        CPU1.create_text(300,90,fill = "white",text="B1",font=tkfont.Font(family='Helvetica', size=14, weight="bold"))
        self.CACHE1_L1_2 = tk.Text(self, height = 4, width = 10, font=tkfont.Font(family='Helvetica', size=14, weight="bold"),bg="#bde3ff")
        for key in self.processors[0].CACHE['B1']:
            self.CACHE1_L1_2.insert(END, self.processors[0].CACHE['B1'][key]+"\n")
        self.CACHE1_L1_2.place(x=209,y=110)
        ### B2
        CPU1.create_text(45,180,fill = "white",text="B2",font=tkfont.Font(family='Helvetica', size=14, weight="bold"))
        self.CACHE1_L1_3 = tk.Text(self, height = 4, width = 10, font=tkfont.Font(family='Helvetica', size=14, weight="bold"),bg="#bde3ff")
        for key in self.processors[0].CACHE['B2']:
            self.CACHE1_L1_3.insert(END, self.processors[0].CACHE['B2'][key]+"\n")
        self.CACHE1_L1_3.place(x=92,y=205)
        ### B3
        CPU1.create_text(300,180,fill = "white",text="B3",font=tkfont.Font(family='Helvetica', size=14, weight="bold"))
        self.CACHE1_L1_4 = tk.Text(self, height = 4, width = 10, font=tkfont.Font(family='Helvetica', size=14, weight="bold"),bg="#bde3ff")
        for key in self.processors[0].CACHE['B3']:
            self.CACHE1_L1_4.insert(END, self.processors[0].CACHE['B3'][key]+"\n")
        self.CACHE1_L1_4.place(x=209,y=205)
    ###### # Cache for CPU2
        ### B0
        CPU2.create_text(45,90,fill = "white",text="B0",font=tkfont.Font(family='Helvetica', size=14, weight="bold"))
        self.CACHE2_L1_1 = tk.Text(self, height = 4, width = 10, font=tkfont.Font(family='Helvetica', size=14, weight="bold"),bg="#bde3ff")
        for key in self.processors[1].CACHE['B0']:
            self.CACHE2_L1_1.insert(END, self.processors[1].CACHE['B0'][key]+"\n")
        self.CACHE2_L1_1.place(x=472,y=110)
        ### B1
        CPU2.create_text(300,90,fill = "white",text="B1",font=tkfont.Font(family='Helvetica', size=14, weight="bold"))
        self.CACHE2_L1_2 = tk.Text(self, height = 4, width = 10, font=tkfont.Font(family='Helvetica', size=14, weight="bold"),bg="#bde3ff")
        for key in self.processors[1].CACHE['B1']:
            self.CACHE2_L1_2.insert(END, self.processors[1].CACHE['B1'][key]+"\n")
        self.CACHE2_L1_2.place(x=589,y=110)
        ### B2
        CPU2.create_text(45,180,fill = "white",text="B2",font=tkfont.Font(family='Helvetica', size=14, weight="bold"))
        self.CACHE2_L1_3 = tk.Text(self, height = 4, width = 10, font=tkfont.Font(family='Helvetica', size=14, weight="bold"),bg="#bde3ff")
        for key in self.processors[1].CACHE['B2']:
            self.CACHE2_L1_3.insert(END, self.processors[1].CACHE['B2'][key]+"\n")
        self.CACHE2_L1_3.place(x=472,y=205)
        ### B3
        CPU2.create_text(300,180,fill = "white",text="B3",font=tkfont.Font(family='Helvetica', size=14, weight="bold"))
        self.CACHE2_L1_4 = tk.Text(self, height = 4, width = 10, font=tkfont.Font(family='Helvetica', size=14, weight="bold"),bg="#bde3ff")
        for key in self.processors[1].CACHE['B3']:
            self.CACHE2_L1_4.insert(END, self.processors[1].CACHE['B3'][key]+"\n")
        self.CACHE2_L1_4.place(x=589,y=205)
    ###### # Cache for CPU3
        ### B0
        CPU3.create_text(45,90,fill = "white",text="B0",font=tkfont.Font(family='Helvetica', size=14, weight="bold"))
        self.CACHE3_L1_1 = tk.Text(self, height = 4, width = 10, font=tkfont.Font(family='Helvetica', size=14, weight="bold"),bg="#bde3ff")
        for key in self.processors[2].CACHE['B0']:
            self.CACHE3_L1_1.insert(END, self.processors[2].CACHE['B0'][key]+"\n")
        self.CACHE3_L1_1.place(x=852,y=110)
        ### B1
        CPU3.create_text(300,90,fill = "white",text="B1",font=tkfont.Font(family='Helvetica', size=14, weight="bold"))
        self.CACHE3_L1_2 = tk.Text(self, height = 4, width = 10, font=tkfont.Font(family='Helvetica', size=14, weight="bold"),bg="#bde3ff")
        for key in self.processors[2].CACHE['B1']:
            self.CACHE3_L1_2.insert(END, self.processors[2].CACHE['B1'][key]+"\n")
        self.CACHE3_L1_2.place(x=969,y=110)
        ### B2
        CPU3.create_text(45,180,fill = "white",text="B2",font=tkfont.Font(family='Helvetica', size=14, weight="bold"))
        self.CACHE3_L1_3 = tk.Text(self, height = 4, width = 10, font=tkfont.Font(family='Helvetica', size=14, weight="bold"),bg="#bde3ff")
        for key in self.processors[2].CACHE['B2']:
            self.CACHE3_L1_3.insert(END, self.processors[2].CACHE['B2'][key]+"\n")
        self.CACHE3_L1_3.place(x=852,y=205)
        ### B3
        CPU3.create_text(300,180,fill = "white",text="B3",font=tkfont.Font(family='Helvetica', size=14, weight="bold"))
        self.CACHE3_L1_4 = tk.Text(self, height = 4, width = 10, font=tkfont.Font(family='Helvetica', size=14, weight="bold"),bg="#bde3ff")
        for key in self.processors[2].CACHE['B3']:
            self.CACHE3_L1_4.insert(END, self.processors[2].CACHE['B3'][key]+"\n")
        self.CACHE3_L1_4.place(x=969,y=205)
    ###### # Cache for CPU4
        ### B0
        CPU4.create_text(45,90,fill = "white",text="B0",font=tkfont.Font(family='Helvetica', size=14, weight="bold"))
        self.CACHE4_L1_1 = tk.Text(self, height = 4, width = 10, font=tkfont.Font(family='Helvetica', size=14, weight="bold"),bg="#bde3ff")
        for key in self.processors[3].CACHE['B0']:
            self.CACHE4_L1_1.insert(END, self.processors[3].CACHE['B0'][key]+"\n")
        self.CACHE4_L1_1.place(x=1232,y=110)
        ### B1
        CPU4.create_text(300,90,fill = "white",text="B1",font=tkfont.Font(family='Helvetica', size=14, weight="bold"))
        self.CACHE4_L1_2 = tk.Text(self, height = 4, width = 10, font=tkfont.Font(family='Helvetica', size=14, weight="bold"),bg="#bde3ff")
        for key in self.processors[3].CACHE['B1']:
            self.CACHE4_L1_2.insert(END, self.processors[3].CACHE['B1'][key]+"\n")
        self.CACHE4_L1_2.place(x=1349,y=110)
        ### B2
        CPU4.create_text(45,180,fill = "white",text="B2",font=tkfont.Font(family='Helvetica', size=14, weight="bold"))
        self.CACHE4_L1_3 = tk.Text(self, height = 4, width = 10, font=tkfont.Font(family='Helvetica', size=14, weight="bold"),bg="#bde3ff")
        for key in self.processors[3].CACHE['B2']:
            self.CACHE4_L1_3.insert(END, self.processors[3].CACHE['B2'][key]+"\n")
        self.CACHE4_L1_3.place(x=1232,y=205)
        ### B3
        CPU4.create_text(300,180,fill = "white",text="B3",font=tkfont.Font(family='Helvetica', size=14, weight="bold"))
        self.CACHE4_L1_4 = tk.Text(self, height = 4, width = 10, font=tkfont.Font(family='Helvetica', size=14, weight="bold"),bg="#bde3ff")
        for key in self.processors[3].CACHE['B3']:
            self.CACHE4_L1_4.insert(END, self.processors[3].CACHE['B3'][key]+"\n")
        self.CACHE4_L1_4.place(x=1349,y=205)

        # Memory
        MEMORY = tk.Canvas(self,height=470,width=450,bg="#ED4A0D")
        MEMORY.place(x=570,y=520)
        MEMORY.create_text(225,30,fill="White", text="MEMORY", font=tkfont.Font(family='Helvetica', size=14, weight="bold") )
        # Creating Mem blocks
        Y=580
        global mem_map 
        for i in range(8):
            self.MEMORY.append(tk.Text(self, height = 2, width = 8, font=tkfont.Font(family='Helvetica', size=14, weight="bold"),bg="#FFDB69"))
            self.MEMORY[i].insert(END,self.memory.BLOCKS[mem_map[i]])
            self.MEMORY[i].place(x=755,y=Y)
            Y=Y+50
        Y=85
        for cell in self.memory.BLOCKS:
            MEMORY.create_text(150,Y,fill="white", text=cell, font=tkfont.Font(family='Helvetica', size=14, weight="bold") )
            Y=Y+50

        ### Finally adding the Bus Log
        self.LOG = tk.Text(self, height = 20, width = 35,font=tkfont.Font(family='Helvetica', size=14, weight="bold"),bg="black", fg="white")
        self.LOG.grid(sticky="nsew")
        self.LOG.place(x=35,y=580)
        scrollb = ttk.Scrollbar(self, command=self.LOG.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        self.LOG['yscrollcommand'] = scrollb.set
        log = tk.Label(self,text="Instruction Log",font=tkfont.Font(family='Helvetica', size=14, weight="bold"))
        log.place(x=130,y=550)
        ### Instruction entry
        self.entry = Entry(self)
        self.entry.place(x=160,y=33)


        stepButton = tk.Button(self, text="Add",
                           command=self.addInstruction)
        stepButton.place(x=340,y=30)
        stepButton = tk.Button(self, text="Step",
                           command=self.step)
        stepButton.place(x=410,y=30)
        #t1 = threading.Thread(target=self.processors[0].processorRoutine, args=[])
        #t1.start()
        
        self.updateData()
        returnButton = tk.Button(self, text="Go to the start page",
                           command=self.returnToStart)
        returnButton.place(x=1350,y=30)
        # MUST CREATE A START, PAUSE AND STOP BUTTON
        startButton = tk.Button(self, text="Start", command=self.startThreads)
        startButton.place(x=30,y=30)
        stopButton = tk.Button(self, text="Pause", command=self.stopThreads)
        stopButton.place(x=90,y=30)
        # MUST ADD AN EXIT BUTTON
        exitButton = tk.Button(self, text="Exit",
                            command=self.exitFunction)
        exitButton.place(x=1490,y=950)
        export = tk.Button(self, text="Export",
                            command=self.exportLog)
        export.place(x=1400,y=950)


    def exportLog(self):
        self.bus.exportLog()

    def returnToStart(self):
        # Stop the threads
        for CPU in self.processors:
            CPU.ACTIVE= False
        # Clean the objects
        # Return to Start Page
        self.controller.show_frame("StartPage")
    
    def addInstruction(self):
        pattern ='^(([1-4]) (calc|(read (0|1){3})|(write (0|1){3} 0x([a-f]|[0-9]){4})))$'
        instruction = self.entry.get()
        isInstruction = re.search(pattern, instruction)
        if (isInstruction):
            ins_slices = instruction.split(" ")
            proc_num = int(ins_slices[0])-1
            inst = ins_slices[1:len(ins_slices)]
            # CPU{num}.addToQueue(instruction, address, data0)
            print("Valid Instruction")
            if self.processors[proc_num].ACTIVE:
                self.bus.LOG.append("System is currently running. Must pause before inserting a instruction")
                print("System is currently running. Must pause before inserting a instruction")
            else:
                self.processors[proc_num].add_inst_to_queue(inst)
                self.bus.LOG.append("CPU " +instruction+". Instruction added")
                print("CPU " +instruction+". Instruction added")
        else:
            self.bus.LOG.append("Invalid instruction for CPU" +instruction+"\nInstruction not added")
            print("Invalid Instruction")
        

    def stopThreads(self):
        # Stop the threads
        for CPU in self.processors:
            CPU.ACTIVE= False

    def startThreads(self):
        if (not self.processors[0].ACTIVE): # If the threads are nor started yet 
            for CPU in self.processors:
                CPU.ACTIVE= True
                t1 = threading.Thread(target=CPU.processorRoutine, args=[])
                t1.start()
            #t2 = threading.Thread(target=self.processors[1].processorRoutine, args=[])
            #t2.start()
    
    def step(self):
        for proc in self.processors:
            t = threading.Thread(target=proc.processorStep, args=[])
            t.start()
            sleep(0.0000001)

    def exitFunction(self):
        tk.Tk.quit(self)

    def updateData(self):
        global mem_map
########## First we work on cache ###############
    ########## Processor 1#############
        self.CACHE1_L1_1.delete(1.0,END)
        self.CACHE1_L1_2.delete(1.0,END)
        self.CACHE1_L1_3.delete(1.0,END)
        self.CACHE1_L1_4.delete(1.0,END)
        
        for key in self.processors[0].CACHE['B0']:
            self.CACHE1_L1_1.insert(END, self.processors[0].CACHE['B0'][key]+"\n")
       
        for key in self.processors[0].CACHE['B1']:
            self.CACHE1_L1_2.insert(END, self.processors[0].CACHE['B1'][key]+"\n")
        
        for key in self.processors[0].CACHE['B2']:
            self.CACHE1_L1_3.insert(END, self.processors[0].CACHE['B2'][key]+"\n")
        
        for key in self.processors[0].CACHE['B3']:
            self.CACHE1_L1_4.insert(END, self.processors[0].CACHE['B3'][key]+"\n")
    ########## Processor 2#############
        self.CACHE2_L1_1.delete(1.0,END)
        self.CACHE2_L1_2.delete(1.0,END)
        self.CACHE2_L1_3.delete(1.0,END)
        self.CACHE2_L1_4.delete(1.0,END)
        
        for key in self.processors[1].CACHE['B0']:
            self.CACHE2_L1_1.insert(END, self.processors[1].CACHE['B0'][key]+"\n")
       
        for key in self.processors[1].CACHE['B1']:
            self.CACHE2_L1_2.insert(END, self.processors[1].CACHE['B1'][key]+"\n")
        
        for key in self.processors[1].CACHE['B2']:
            self.CACHE2_L1_3.insert(END, self.processors[1].CACHE['B2'][key]+"\n")
        
        for key in self.processors[1].CACHE['B3']:
            self.CACHE2_L1_4.insert(END, self.processors[1].CACHE['B3'][key]+"\n")
    ########## Processor 3#############
        self.CACHE3_L1_1.delete(1.0,END)
        self.CACHE3_L1_2.delete(1.0,END)
        self.CACHE3_L1_3.delete(1.0,END)
        self.CACHE3_L1_4.delete(1.0,END)
        
        for key in self.processors[2].CACHE['B0']:
            self.CACHE3_L1_1.insert(END, self.processors[2].CACHE['B0'][key]+"\n")
       
        for key in self.processors[2].CACHE['B1']:
            self.CACHE3_L1_2.insert(END, self.processors[2].CACHE['B1'][key]+"\n")
        
        for key in self.processors[2].CACHE['B2']:
            self.CACHE3_L1_3.insert(END, self.processors[2].CACHE['B2'][key]+"\n")
        
        for key in self.processors[2].CACHE['B3']:
            self.CACHE3_L1_4.insert(END, self.processors[2].CACHE['B3'][key]+"\n")
    ########## Processor 4#############
        self.CACHE4_L1_1.delete(1.0,END)
        self.CACHE4_L1_2.delete(1.0,END)
        self.CACHE4_L1_3.delete(1.0,END)
        self.CACHE4_L1_4.delete(1.0,END)
        
        for key in self.processors[3].CACHE['B0']:
            self.CACHE4_L1_1.insert(END, self.processors[3].CACHE['B0'][key]+"\n")
       
        for key in self.processors[3].CACHE['B1']:
            self.CACHE4_L1_2.insert(END, self.processors[3].CACHE['B1'][key]+"\n")
        
        for key in self.processors[3].CACHE['B3']:
            self.CACHE4_L1_3.insert(END, self.processors[3].CACHE['B2'][key]+"\n")
        
        for key in self.processors[3].CACHE['B3']:
            self.CACHE4_L1_4.insert(END, self.processors[3].CACHE['B3'][key]+"\n")
        ## Controller messages
        self.CONTROLLER_1.delete(1.0,END)# Controller for CPU1
        self.CONTROLLER_1.insert(1.0,self.processors[0].STATUS)
        self.CONTROLLER_2.delete(1.0,END)# Controller for CPU2
        self.CONTROLLER_2.insert(1.0,self.processors[1].STATUS)
        self.CONTROLLER_3.delete(1.0,END)# Controller for CPU3
        self.CONTROLLER_3.insert(1.0,self.processors[2].STATUS)
        self.CONTROLLER_4.delete(1.0,END)# Controller for CPU4
        self.CONTROLLER_4.insert(1.0,self.processors[3].STATUS)
    ######### Updating memory ################
        for i in range(8):
            self.MEMORY[i].delete(1.0,END)
            self.MEMORY[i].insert(END,self.memory.BLOCKS[mem_map[i]])
        ###### Updating last/current instructions #####
        for i in range(4):
            self.CURRENT[i].delete(1.0,END)
            self.LAST[i].delete(1.0,END)
            self.CURRENT[i].insert(1.0, self.processors[i].CURRENT_INSTRUCTION)
            self.LAST[i].insert(1.0, self.processors[i].LAST_INSTRUCTION)
    ######## Updating the Log ###########
        self.LOG.delete(1.0,END)
        for entry in self.bus.LOG:
            self.LOG.insert(END,entry+"\n")
        self.after(100,self.updateData)
    
    def memString(self):
        string = ""
        for cell in self.memory.BLOCKS:
            string = string+cell+"\n\n\n"
        print(string)
        return string
class PageTwo(tk.Frame):

    def __init__(self, parent, controller,processors,memory,bus):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Hello There...", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        
        
        button = tk.Button(self, text="Go to the start page",
                           command=self.returnToStart)
        button.pack()
    def returnToStart(self):
        # Stop the threads
        # Clean the objects
        # Return to Start Page
        self.controller.show_frame("StartPage")

if __name__ == "__main__":
    CPUS = []
    MEMORY = Memory()
    BUS = Bus(MEMORY)
    for i in range(1,5):
        CPUS.append(Processor(i,BUS))
    BUS.PROCESSORS=CPUS
    app = SampleApp(CPUS,MEMORY,BUS)