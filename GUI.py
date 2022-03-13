import tkthread; tkthread.tkinstall()
from concurrent.futures import process
import threading
import tkinter as tk
from tkinter import *
from tkinter import font as tkfont
from processor import *
from bus import *
from memory import *


#F5F5F2
class SampleApp(tk.Tk):

    def __init__(self,processors, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=22, weight="bold", slant="italic")
        self.title("MOESI CACHE SIMULATOR")
        self.geometry("1550x950")

        tkt = tkthread.TkThread(self)
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
            frame = F(parent=container, controller=self,processors=processors)
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

    def __init__(self, parent, controller,processors):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the start page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=30)

        button1 = tk.Button(self, text="Step by Step",
                            command=lambda: controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="continuous",
                            command=lambda: controller.show_frame("PageTwo"))
        button1.pack(pady=20)
        button2.pack()
        


class PageOne(tk.Frame):

    def __init__(self, parent, controller,processors):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Step by Step execution", font=controller.title_font)
        label.place(x=650,y=20)
        
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
        
        CPU1.place(x=30,y=100)
        CPU2.place(x=410,y=100)
        CPU3.place(x=790,y=100)
        CPU4.place(x=1170,y=100)
        CONTROLLER1.place(x=65,y=400)
        CONTROLLER2.place(x=445,y=400)
        CONTROLLER3.place(x=825,y=400)
        CONTROLLER4.place(x=1205,y=400)

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

        # Cache for CPU1
        CACHE1_L1_1 = tk.Text(self, height = 4, width = 10, font=tkfont.Font(family='Helvetica', size=14, weight="bold"),bg="#bde3ff")
        for key in processors[0].CACHE['B0']:
            CACHE1_L1_1.insert(END, processors[0].CACHE['B0'][key]+"\n")
        CACHE1_L1_1.place(x=92,y=140)

        CACHE1_L1_2 = tk.Text(self, height = 4, width = 10, font=tkfont.Font(family='Helvetica', size=14, weight="bold"),bg="#bde3ff")
        for key in processors[0].CACHE['B1']:
            CACHE1_L1_2.insert(END, processors[0].CACHE['B1'][key]+"\n")
        CACHE1_L1_2.place(x=209,y=140)

        CACHE1_L1_3 = tk.Text(self, height = 4, width = 10, font=tkfont.Font(family='Helvetica', size=14, weight="bold"),bg="#bde3ff")
        for key in processors[0].CACHE['B2']:
            CACHE1_L1_3.insert(END, processors[0].CACHE['B2'][key]+"\n")
        CACHE1_L1_3.place(x=92,y=235)

        CACHE1_L1_4 = tk.Text(self, height = 4, width = 10, font=tkfont.Font(family='Helvetica', size=14, weight="bold"),bg="#bde3ff")
        for key in processors[0].CACHE['B3']:
            CACHE1_L1_4.insert(END, processors[0].CACHE['B3'][key]+"\n")
        CACHE1_L1_4.place(x=209,y=235)
        # Cache for CPU2
        CPU2.create_rectangle(40,50,175,150,fill="#bde3ff")
        CPU2.create_rectangle(175,50,310,150,fill="#bde3ff")
        CPU2.create_rectangle(40,150,175,250,fill="#bde3ff")
        CPU2.create_rectangle(175,150,310,250,fill="#bde3ff")
        # Cache for CPU3
        CPU3.create_rectangle(40,50,175,150,fill="#bde3ff")
        CPU3.create_rectangle(175,50,310,150,fill="#bde3ff")
        CPU3.create_rectangle(40,150,175,250,fill="#bde3ff")
        CPU3.create_rectangle(175,150,310,250,fill="#bde3ff")
        # Cache for CPU4
        CPU4.create_rectangle(40,50,175,150,fill="#bde3ff")
        CPU4.create_rectangle(175,50,310,150,fill="#bde3ff")
        CPU4.create_rectangle(40,150,175,250,fill="#bde3ff")
        CPU4.create_rectangle(175,150,310,250,fill="#bde3ff")

        res = tk.Label(self)
        res.place()
        entry = Entry(self)
        entry.place()
        test = tk.Button(self, text="Show text",
                           command=lambda: self.updateData(entry,res))
        test.place()

        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.place()
        t1 = threading.Thread(target=processors[0].processorRoutine, args=[])
        t1.start()
        self.updateData(processors,CACHE1_L1_1,CACHE1_L1_2,CACHE1_L1_3,CACHE1_L1_4)
    def updateData(self,processors,c1,c2,c3,c4):
        c1.delete(1.0,END)
        c2.delete(1.0,END)
        c3.delete(1.0,END)
        c4.delete(1.0,END)
        #CACHE1_L1_1 = tk.Text(self, height = 4, width = 10, font=tkfont.Font(family='Helvetica', size=14, weight="bold"),bg="#bde3ff")
        for key in processors[0].CACHE['B0']:
            c1.insert(END, processors[0].CACHE['B0'][key]+"\n")
        c1.place(x=92,y=140)

        #CACHE1_L1_2 = tk.Text(self, height = 4, width = 10, font=tkfont.Font(family='Helvetica', size=14, weight="bold"),bg="#bde3ff")
        for key in processors[0].CACHE['B1']:
            c2.insert(END, processors[0].CACHE['B1'][key]+"\n")
        c2.place(x=209,y=140)

        #CACHE1_L1_3 = tk.Text(self, height = 4, width = 10, font=tkfont.Font(family='Helvetica', size=14, weight="bold"),bg="#bde3ff")
        for key in processors[0].CACHE['B2']:
            c3.insert(END, processors[0].CACHE['B2'][key]+"\n")
        c3.place(x=92,y=235)

        #CACHE1_L1_4 = tk.Text(self, height = 4, width = 10, font=tkfont.Font(family='Helvetica', size=14, weight="bold"),bg="#bde3ff")
        for key in processors[0].CACHE['B3']:
            c4.insert(END, processors[0].CACHE['B3'][key]+"\n")
        c4.place(x=209,y=235)
        self.update_idletasks()
        
class PageTwo(tk.Frame):

    def __init__(self, parent, controller,processors):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="continuous execution", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


if __name__ == "__main__":
    CPUS = []
    MEMORY = Memory()
    BUS = Bus(MEMORY)
    CPUS.append(Processor(1,BUS))
    app = SampleApp(CPUS)
    #app.geometry("1550x950")
    #app.title("MOESI CACHE SIMULATOR")
    #app.mainloop()