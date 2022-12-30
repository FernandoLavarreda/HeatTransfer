import re
import tkinter as tk
import tkinter.ttk as ttk
from typing import Callable
import traceback

def parse_action(action:str):
    """
    Function to parse arguments and commands from string input
    """
    pattern = r"\w+"
    arguments = r"-\w+\s+((\d+\.{0,1}\d*)|(\w+))"
    
    match = re.search(pattern, action)
    
    if match == None:
        raise ValueError("Could not find an action to excecute")
    
    match_args = re.finditer(arguments, action[match.end()-1:])
    
    parsed = {
            'action': match.group(),
            'args':{},
            }
    
    option = r"-\w+"
    number = r" \d+\.{0,1}\d*"
    string = r" [a-z_A-Z0-9]+"
    if not match_args == None:
        for m in match_args:
            opt_val = m.group()
            opt = re.search(option, opt_val).group()[1:]
            if re.search(number, opt_val) != None:
                val = float(re.search(number, opt_val).group()[1:])
            else:
                val = re.search(string, opt_val).group()[1:]
            parsed['args'][opt] = val
    return parsed
    



class Command(ttk.Frame):
    
    def __init__(self, actions:dict, *args, **kwargs):
        """
        For actions provide a dictionary with str as keys for commands and functions/callables for actions to perform
        """
        super().__init__(*args, **kwargs)
        self.out = tk.StringVar()
        self.ins = tk.StringVar()
        self.commands = ttk.Entry(master=self, textvariable=self.ins)
        self.output = ttk.Label(master=self, textvariable=self.out)
        self.actions = actions
        
        
        self.commands.bind("<Return>", self.request)
        self.commands.pack(expand=True, fill=tk.X)
        self.output.pack(expand=True, fill=tk.X)
        
        
        
    
    def request(self, *args):
        self.out.set("")
        interpreted = parse_action(self.ins.get())
        if interpreted["action"] in self.actions:
            try:
                if len(interpreted["args"]):
                    self.actions[interpreted["action"]](**interpreted["args"])
                else:
                    self.actions[interpreted["action"]]()
            except TypeError as e:
                arg = re.search("'.+'", str(e)).group()
                print(e)
                self.out.set("Not a valid argument ("+arg+") for command: "+interpreted["action"])
            except ValueError as f:
                print(f)
                self.out.set(f)
            except AssertionError as fe:
                print(fe)
                self.out.set(fe)
        else:
            self.out.set("Command not recognized")
    
    
    def add_action(self, command:str, action:Callable):
        self.actions[command] = action
    
    
    def focus(self, *args):
        self.commands.focus_set()
    
    
    


if __name__ == "__main__":
    print(parse_action("Fernado -sp fer -comi fer -h 10.s"))

