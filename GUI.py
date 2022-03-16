from turtle import width
import threading
import tkinter as tk
from tkinter import *
from tkinter import font as tkfont
from processor import *
from bus import *
from memory import *


#F5F5F2
class SampleApp(tk.Tk):

    def __init__(self,processors,memory, *args, **kwargs):
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
            frame = F(parent=container, controller=self,processors=processors,memory=memory)
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

    def __init__(self, parent, controller,processors,memory):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the start page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=30)

        button1 = tk.Button(self, text="Step by Step",
                            command=lambda: controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="Continuous",
                            command=lambda: controller.show_frame("PageTwo"))
        button3 = tk.Button(self, text="Exit",
                            command=self.exitFunction)
        button1.pack(pady=20)
        button2.pack()
        button3.pack()

    def exitFunction(self):
        tk.Tk.quit(self)

class PageOne(tk.Frame):

    def __init__(self, parent, controller,processors,memory):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.processors = processors
        self.CACHE1_L1_1 = ""
        self.CACHE1_L1_2 = ""
        self.CACHE1_L1_3 = ""
        self.CACHE1_L1_4 = ""
        self.memory = memory
        label = tk.Label(self, text="Step by Step execution", font=controller.title_font)
        label.place(x=670,y=20)
        
        # Constructing the elements.
        # Entire Rectangle of the CPU
        CPU1 = tk.Canvas(self,height=450,width=350,bg="#1482FA")
        CPU2 = tk.Canvas(self,height=450,width=350,bg="#1482FA")
        CPU3 = tk.Canvas(self,height=450,width=350,bg="#1482FA")
        CPU4 = tk.Canvas(self,height=450,width=350,bg="#1482FA")
        
        # Controller Message
        CONTROLLER1 = tk.Text(self, height = 7, width = 35)
        CONTROLLER2 = tk.Text(self, height = 7, width = 35)
        CONTROLLER3 = tk.Text(self, height = 7, width = 35)
        CONTROLLER4 = tk.Text(self, height = 7, width = 35)
        
        CPU1.place(x=30,y=65)
        CPU2.place(x=410,y=65)
        CPU3.place(x=790,y=65)
        CPU4.place(x=1170,y=65)
        CONTROLLER1.place(x=65,y=360)
        CONTROLLER2.place(x=445,y=360)
        CONTROLLER3.place(x=825,y=360)
        CONTROLLER4.place(x=1205,y=360)

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
        CPU2.create_rectangle(40,50,175,150,fill="#bde3ff")
        CPU2.create_rectangle(175,50,310,150,fill="#bde3ff")
        CPU2.create_rectangle(40,150,175,250,fill="#bde3ff")
        CPU2.create_rectangle(175,150,310,250,fill="#bde3ff")
    ###### # Cache for CPU3
        CPU3.create_rectangle(40,50,175,150,fill="#bde3ff")
        CPU3.create_rectangle(175,50,310,150,fill="#bde3ff")
        CPU3.create_rectangle(40,150,175,250,fill="#bde3ff")
        CPU3.create_rectangle(175,150,310,250,fill="#bde3ff")
    ###### # Cache for CPU4
        CPU4.create_rectangle(40,50,175,150,fill="#bde3ff")
        CPU4.create_rectangle(175,50,310,150,fill="#bde3ff")
        CPU4.create_rectangle(40,150,175,250,fill="#bde3ff")
        CPU4.create_rectangle(175,150,310,250,fill="#bde3ff")

        # Memory
        MEMORY = tk.Canvas(self,height=470,width=450,bg="white")
        MEMORY.place(x=570,y=520)
        MEMORY.create_text(225,260,fill="Black", text=self.memString(), font=tkfont.Font(family='Helvetica', size=14, weight="bold") )
        entry = Entry(self)
        entry.place(x=160,y=33)


        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.place()
        #t1 = threading.Thread(target=self.processors[0].processorRoutine, args=[])
        #t1.start()
        
        self.updateData()
        returnButton = tk.Button(self, text="Go to the start page",
                           command=self.returnToStart)
        returnButton.place(x=1350,y=30)
        # MUST CREATE A START, PAUSE AND STOP BUTTON
        startButton = tk.Button(self, text="Start", command=self.startThreads)
        startButton.place(x=30,y=30)
        stopButton = tk.Button(self, text="STOP", command=self.stopThreads)
        stopButton.place(x=90,y=30)
        # MUST ADD AN EXIT BUTTON
        exitButton = tk.Button(self, text="Exit",
                            command=self.exitFunction)
        exitButton.place(x=1490,y=950)

    def returnToStart(self):
        # Stop the threads
        for CPU in self.processors:
            CPU.ACTIVE= False
        # Clean the objects
        # Return to Start Page
        self.controller.show_frame("StartPage")
    
    def stopThreads(self):
        # Stop the threads
        for CPU in self.processors:
            CPU.ACTIVE= False

    def startThreads(self):
        if (not self.processors[0].ACTIVE): # If the threads are nor started yet 
            for CPU in self.processors:
                CPU.ACTIVE= True
            t1 = threading.Thread(target=self.processors[0].processorRoutine, args=[])
            t1.start()
        
    def exitFunction(self):
        tk.Tk.quit(self)

    def updateData(self):
        self.CACHE1_L1_1.delete(1.0,END)
        self.CACHE1_L1_2.delete(1.0,END)
        self.CACHE1_L1_3.delete(1.0,END)
        self.CACHE1_L1_4.delete(1.0,END)
        #CACHE1_L1_1 = tk.Text(self, height = 4, width = 10, font=tkfont.Font(family='Helvetica', size=14, weight="bold"),bg="#bde3ff")
        for key in self.processors[0].CACHE['B0']:
            self.CACHE1_L1_1.insert(END, self.processors[0].CACHE['B0'][key]+"\n")
        #self.CACHE1_L1_1.place(x=92,y=140)

        #CACHE1_L1_2 = tk.Text(self, height = 4, width = 10, font=tkfont.Font(family='Helvetica', size=14, weight="bold"),bg="#bde3ff")
        for key in self.processors[0].CACHE['B1']:
            self.CACHE1_L1_2.insert(END, self.processors[0].CACHE['B1'][key]+"\n")
        #self.CACHE1_L1_2.place(x=209,y=140)

        #CACHE1_L1_3 = tk.Text(self, height = 4, width = 10, font=tkfont.Font(family='Helvetica', size=14, weight="bold"),bg="#bde3ff")
        for key in self.processors[0].CACHE['B2']:
            self.CACHE1_L1_3.insert(END, self.processors[0].CACHE['B2'][key]+"\n")
        #self.CACHE1_L1_3.place(x=92,y=235)

        #CACHE1_L1_4 = tk.Text(self, height = 4, width = 10, font=tkfont.Font(family='Helvetica', size=14, weight="bold"),bg="#bde3ff")
        for key in self.processors[0].CACHE['B3']:
            self.CACHE1_L1_4.insert(END, self.processors[0].CACHE['B3'][key]+"\n")
        #self.CACHE1_L1_4.place(x=209,y=235)
        self.after(100,self.updateData)
    
    def memString(self):
        string = ""
        for cell in self.memory.BLOCKS:
            string = string+self.memory.BLOCKS[cell]+"\n\n\n"
        print(string)
        return string
class PageTwo(tk.Frame):

    def __init__(self, parent, controller,processors,memory):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="continuous execution", font=controller.title_font)
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
    CPUS.append(Processor(1,BUS))
    app = SampleApp(CPUS,MEMORY)