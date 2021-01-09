import tkinter as tk

from pathlib import Path

class FinanceFrame(tk.LabelFrame):
    def updateTitle(self,day,profile):
        profileName = Path(profile).stem
        self.config(text="Finance of Days " + str(day) + " (Profile : " + profileName+")")


class dayButton(tk.Radiobutton):
    """
        base  button to select a day
    """
    def __init__(self,xx,yy,*args, **kwargs):
        super().__init__(*args, **kwargs)
        #config default
        self.config(value=self["text"],indicatoron=False)
        #pack the button
        self.pack()
        self.place(relx=xx,rely=yy,anchor=tk.NW)

class inputDataButton(tk.Button):
    """
        base  button for inputting data button
    """
    def __init__(self,xx,yy,typ,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTheme(typ)
        #pack the button
        self.pack()
        self.place(relx=xx,rely=yy,anchor=tk.NW)
    
    def setTheme(self,typ):
            if typ == "inc":
                self.config(bg="blue",fg="white")
            elif typ == "exp":
                self.config(bg="red",fg="white")

class incomeLabel(tk.Label):
    """
        base label for displaying income and expenses data
    """
    def __init__(self,xx,yy,*args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.config(bg="blue",fg="white")
        #pack the button
        self.pack()
        self.place(relx=xx,rely=yy,anchor=tk.NW)