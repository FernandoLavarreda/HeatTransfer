#GUI for Transient Heat transfer Interactions
#Fernando Lavarreda

from typing import Tuple, List

from commands import Command
from inputs import read_float, read_int, read_list, read_linspace, mapping
import tkinter as tk
import tkinter.ttk as ttk
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.pyplot import tight_layout
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from functools import partial
import time
import math

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
    
    
    def clear(self):
        self.axis.cla()
        self.render()
    
    
    def set_lims(self, xlims:Tuple[float, float], ylims:Tuple[float, float]):
        self.axis.axis(xmin=xlims[0], xmax=xlims[1], ymin=ylims[0], ymax=ylims[1])
        self.render()
    
    
    def make_animation(self, sequence:Tuple[List[List[float]], List[List[float]]], *, time_out:float=0):
        self.clear()
        line = self.axis.plot(sequence[0][0], sequence[1][0])[0]
        self.render()
        for frame in range(len(sequence[0])):
            line.set_data(sequence[0][frame], sequence[1][frame])
            time.sleep(time_out)
            self.render()
    
    
    def moving(self):
        self.set_lims([-1.2*4/3, 1.2*4/3], [-1.2, 1.2])
        xs = [[0, math.cos(i/1_000*2*math.pi)] for i in range(1_000)]
        ys = [[0, math.sin(i/1_000*2*math.pi)] for i in range(1_000)]
        self.make_animation([xs, ys], time_out=0)
            
            
    
    


class HeatImp(tk.Tk):
    
    inputs = ["Biot", "Starting temperature", "Temperature of Surroundings", "Size", "Conductivity Constant", "Convection Constant", \
              "Specific Heat", "Density", "Diffusivity", "time", "lambdas", "dx", "coordinates"]
    parse_inputs = [(read_int, read_float)]*9+[(read_int, read_float, read_linspace, read_list), (read_int,), (read_int, read_float), (read_int, read_float, read_linspace, read_list)]
    can_be_none = [False, False, False, False, True, True, True, True, True, False, False, True, True]
    def __init__(self, actions:dict):
        super().__init__()
        self.title("Heat Transient Anlysis")
        self.main_menu = tk.Menu(self)
        self.main_menu.add_command(label="Quit", command=self.quit)
        #self.main_menu.add_command(label="Run", command=self.do)
        self.config(menu=self.main_menu)
        
        self.geometry(f"+{self.winfo_screenwidth()//6}+{self.winfo_screenheight()//10}") #Center
        #Graphical user aid/inputs
        variables = ttk.LabelFrame(self, text="Inputs")
        self.values = []
        crow = 0
        for input_ in self.inputs:
            ttk.Label(variables, text=input_).grid(row=crow*2, sticky=tk.NE+tk.SW)
            val = tk.StringVar()
            self.values.append(val)
            ttk.Entry(variables, textvariable=val).grid(row=crow*2+1)
            crow+=1
        #--------------------------
        #Work with power user functionalities
        self.commands = Command(master=self, actions=actions)
        
        
        
        #--------------------------
        
        
        #Add widgets to window
        variables.grid(row=0, column=4, rowspan=len(self.inputs)*2, sticky=tk.NE+tk.SW)
        self.commands.grid(row=6, column=0, columnspan=5, rowspan=2, sticky=tk.NE+tk.SW)
        self.graphics = Graphics(self, size=(8, 6), row=0, column=0, columnspan=4, rowspan=5, dpi=100, title="Transient Analysis Simulation")
        self.resizable(False, False)
    
    
    def get_command(self, *args)->Command:
        return self.commands    
    
    
    def do(self, *args):
        self.graphics.moving()
    
    
    def quit(self, *args):
        self.destroy()
    
    
    def get_parse_args(self):
        identified_values = []
        for input_ in range(len(HeatImp.inputs)):
            counter = 1
            for parse_in in HeatImp.parse_inputs[input_]:
                try:
                    parse = parse_in(self.values[input_].get())
                except ValueError:
                    if counter<len(HeatImp.parse_inputs[input_]):
                        pass
                    elif HeatImp.can_be_none[input_]:
                        identified_values.append(None)
                    elif counter >= len(HeatImp.parse_inputs[input_]):
                        raise ValueError("Couldn't interpret "+HeatImp.inputs[input_])
                else:
                    identified_values.append(parse)
                    break
                counter +=1
        return identified_values
    


if __name__ == "__main__":
    app = HeatImp(actions={"do":print})
    app.get_command().add_action("foo", app.get_parse_args)
    app.mainloop()
