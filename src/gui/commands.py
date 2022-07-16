import re
import tkinter as tk
import tkinter.ttk as ttk




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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.out = tk.StringVar()
        self.ins = tk.StringVar()
        self.commands = ttk.Entry(master=self, textvariable=self.ins)
        self.output = ttk.Label(master=self, textvariable=self.out)
        
        
        
        self.commands.bind("<Return>", self.request)
        self.commands.pack(expand=True, fill=tk.X)
        self.output.pack(expand=True, fill=tk.X)
        
        
        
    
    def request(self, *args):
        print(parse_action(self.ins.get()))
    
    
        
    
    
    


if __name__ == "__main__":
    print(parse_action("Fernado -sp fer -comi fer -h 10.s"))

