#GUI for Transient Heat transfer Interactions
#Fernando Lavarreda

from typing import Tuple, List

import time
import math
import tkinter as tk
import tkinter.ttk as ttk
from functools import partial
from .commands import Command
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.pyplot import tight_layout
from tkinter.filedialog import asksaveasfilename
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from .inputs import read_float, read_int, read_list, read_linspace, mapping


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
        line = self.axis.plot(sequence[0][0], sequence[1][0])[0]
        self.render()
        for frame in range(len(sequence[0])):
            line.set_data(sequence[0][frame], sequence[1][frame])
            time.sleep(time_out)
            self.render()
    
    
    def static_drawing(self, sequence:Tuple[List[float], List[float]]):
        self.axis.plot(sequence[0], sequence[1])
        self.render()
    
    
    def moving(self):
        self.set_lims([-1.2*4/3, 1.2*4/3], [-1.2, 1.2])
        xs = [[0, math.cos(i/1_000*2*math.pi)] for i in range(1_000)]
        ys = [[0, math.sin(i/1_000*2*math.pi)] for i in range(1_000)]
        self.make_animation([xs, ys], time_out=0)
    
    
    


class HeatImp(tk.Tk):
    
    inputs = ["Biot", "Starting temperature", "Temperature of Surroundings", "Size", "Conductivity Constant", "Convection Constant", \
              "Specific Heat", "Density", "Diffusivity", "time", "lambdas", "dx", "coordinates"]
    parse_inputs = [(read_int, read_float)]*9+[(read_int, read_float, read_linspace, read_list), (read_int,), (read_int, read_float), (read_linspace, read_list)]
    can_be_none = [True, False, False, False, True, True, True, True, True, False, False, True, True]
    units = [(), ("C", "F"), ("C", "F"), ("m", "cm", "mm", "in"), (), (), (), (), (), (), (), (), ()]
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
        self.entries = []
        self.comboboxes = []
        crow = 0
        for input_ in self.inputs:
            ttk.Label(variables, text=input_).grid(row=crow*2, sticky=tk.NE+tk.SW)
            val = tk.StringVar()
            self.values.append(val)
            entry = ttk.Entry(variables, textvariable=val)
            entry.grid(row=crow*2+1, columnspan=1, sticky=tk.NE+tk.SW)
            self.entries.append(entry)
            combo = ttk.Combobox(variables, values=HeatImp.units[crow], state='readonly', width=4)
            self.comboboxes.append(combo)
            combo.grid(row=crow*2+1, column=2, sticky=tk.NE+tk.SW)
            crow+=1
        #--------------------------
        #Work with power user functionalities
        self.commands = Command(master=self, actions=actions)
        
        
        
        #--------------------------
        
        #Special bindings
        self.bind("<Alt-Up>", self.commands.focus)
        remainders = ["a", "s", "d", "f"]
        self.cursor = 0
        for i in range(len(HeatImp.inputs)):
            if i+1 > 9:
                self.bind(f"<Alt-{remainders[i-9]}>", self.focus)
            else:
                self.bind(f"<Alt-KeyPress-{i+1}>", self.focus)
            self.entries[i].bind("<Down>", self.focus)
            self.entries[i].bind("<Up>", self.focus)
            self.entries[i].bind("<Control-KeyPress-Right>", self.focus)
            self.comboboxes[i].bind("<Control-KeyPress-Left>", self.focus)
        #------------------------------
        
        #Add widgets to window
        variables.grid(row=0, column=4, rowspan=len(self.inputs)*2, sticky=tk.NE+tk.SW)
        self.commands.grid(row=6, column=0, columnspan=5, rowspan=2, sticky=tk.NE+tk.SW)
        self.graphics = Graphics(self, size=(8, 6), row=0, column=0, columnspan=4, rowspan=5, dpi=100, title="Transient Analysis Simulation")
        self.resizable(False, False)
    
    
    def get_command(self, *args)->Command:
        return self.commands
        
    
    def get_graphics(self, *args)->Graphics:
        return self.graphics
    
    
    def do(self, *args)->None:
        self.graphics.moving()
    
    
    def quit(self, *args)->None:
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
    
    
    def focus(self, entry:int, *args)->None:
        remainders = ["a", "s", "d", "f"]
        if entry.char in remainders:
            loc = remainders.index(entry.char)
            self.entries[loc+9].focus_set()
            self.cursor = loc+9
        elif entry.keysym == "Down":
            self.cursor += 1
            if self.cursor >= len(HeatImp.inputs):
                self.cursor = 0
            self.entries[self.cursor].focus_set()
        elif entry.keysym == "Up":
            self.cursor -= 1
            if self.cursor < 0:
                self.cursor = len(HeatImp.inputs)-1
            self.entries[self.cursor].focus_set()
        elif entry.keysym == "Right":
            self.comboboxes[self.cursor].focus_set()
        elif entry.keysym == "Left":
            self.entries[self.cursor].focus_set()
        elif entry.char:
            self.entries[int(entry.char)-1].focus_set()
            self.cursor = int(entry.char)-1
    
    
    def save_file(self, contents:str, title:str, defaultextension:str)->str:
        fln = asksaveasfilename(title=title, defaultextension=defaultextension)
        if fln:
            with open(fln, "w") as file:
                file.write(contents)
            return fln
        return ""


if __name__ == "__main__":
    app = HeatImp(actions={"do":print})
    app.get_command().add_action("foo", app.get_parse_args)
    app.mainloop()
