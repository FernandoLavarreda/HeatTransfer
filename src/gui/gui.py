#GUI for Transient Heat transfer Interactions
#Fernando Lavarreda

from typing import Tuple

from commands import Command
import tkinter as tk
import tkinter.ttk as ttk
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.pyplot import tight_layout
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Graphics():
    
    def __init__(self, parent, size:Tuple[int, int], row, column, columnspan, rowspan, dpi:int, title=""):
        self.fig = Figure(figsize=size, dpi=dpi)
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=column, row=row, rowspan=rowspan, columnspan=columnspan, sticky=tk.SE+tk.NW)
        self.axis = self.fig.add_subplot(111)
        self.axis.set_title(title)
        self.fig.tight_layout()
    
    def render(self):
        self.canvas.draw()
        self.canvas.flush_events()
    
    
    def clear(self, ):
        self.axis.cla()
        self.render()
    
    


class HeatImp(tk.Tk):
    
    inputs = ["Biot", "Starting temperature", "Temperature of Surroundings", "Dimension", "Conductivity Constant", "Convection Constant", \
              "Specific Heat", "Density", "Diffusivity", "time", "lambdas", "dx", "coordinates"]
    
    def __init__(self):
        super().__init__()
        self.title("Heat Transient Anlysis")
        self.main_menu = tk.Menu(self)
        self.main_menu.add_command(label="Quit", command=self.quit)
        self.config(menu=self.main_menu)
        
        #Graphical user aid/inputs
        variables = ttk.LabelFrame(self, text="Inputs")
        values = []
        crow = 0
        for input_ in self.inputs:
            ttk.Label(variables, text=input_).grid(row=crow*2, sticky=tk.NE+tk.SW)
            val = ttk.Entry(variables)
            values.append(val)
            val.grid(row=crow*2+1)
            crow+=1
        #--------------------------
        #Work with power user functionalities
        self.commands = Command(master=self)
        
        
        
        #--------------------------
        
        
        #Add widgets to window
        variables.grid(row=0, column=4, rowspan=len(self.inputs)*2, sticky=tk.NE+tk.SW)
        self.commands.grid(row=6, column=0, columnspan=5, rowspan=2, sticky=tk.NE+tk.SW)
        self.graphics = Graphics(self, size=(8, 6), row=0, column=0, columnspan=4, rowspan=5, dpi=100, title="Ole")
    
    
    def do(self, *args):
        pass
    
    
    def do2(self, *args):
        pass
    
    
    def quit(self, *args):
        self.destroy()
    
    




if __name__ == "__main__":
    app = HeatImp()
    app.mainloop()
