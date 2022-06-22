import re
import tkinter as tk
import tkinter.ttk as ttk


class Command(ttk.Frame):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.out = tk.StringVar()
        self.ins = tk.StringVar()
        self.commands = ttk.Entry(master=self)
        self.output = ttk.Label(master=self, textvariable=self.out)
        
        
        self.commands.pack(expand=True, fill=tk.X)
        self.output.pack(expand=True, fill=tk.X)
        
    
    def bored(self):
        pass
    
    
    


if __name__ == "__main__":
    app = tk.Tk()
    app.mainloop()

