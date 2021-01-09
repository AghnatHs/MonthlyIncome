import tkinter as tk
import tkinter.messagebox as MessageBox

from tkinter.font import Font
from tkinter.filedialog import askopenfilename as askOpenFileName,asksaveasfilename as askSaveAsFileName
from math import copysign

from ui import *
from basedata import *
from formatting import *
from jsonfile import json_processing as json

"""
                     MonthlyIncome
    => calculate your income and expenses for a month <=
"""

TITLE  = "MonthlyIncome"
AUTHOR = "Aghnat HS"

PROFILE_DIR = "profiles" #initial directory
PROFILE_DEBUG = "profiles/template.json" #debug profile

PROFILE = PROFILE_DEBUG  

RESET_VALUE = [[],[]]

#COLOR
cl_lightblue = "#c9cbff"
cl_lightred = "#e5707e"

class App():

    def __init__(self):
        #Main Windows
        self.app = tk.Tk()
        self.app.resizable(0,0)
        self.app.geometry("640x480")
        self.app.title(f"{TITLE}")
        #Variable 
        self.daysObject = [] #list of selecting day button
        self.day = tk.IntVar() #variable to control day
        self.day.set(1)

        self.daysFinance = [] #store incomes and expenses data of each day
        #self.daysFinance = json.load_json(PROFILE_DEBUG)
        #Create GUI
        self.createMainGui()
        #ask profile for first time
        self.loadFinanceProfile(preventCancel=True)
        #Loop the Main Windows
        self.app.mainloop()

    """
        GUI
    """
    def createMainGui(self):
        #>>MainMenu
        self.mainMenu = tk.Menu(self.app)
        #MainMenu >> Profile
        self.profileMenu = tk.Menu(self.mainMenu,tearoff=False,activebackground=cl_lightblue,activeforeground="black")
        self.profileMenu.add_command(label="New",command=lambda:self.newFinanceProfile())
        self.profileMenu.add_command(label="Load",command=lambda:self.loadFinanceProfile())
        self.profileMenu.add_command(label="Save",command=lambda:self.saveFinanceProfile())
        #MainMenu >> About
        self.aboutMenu = tk.Menu(self.mainMenu,tearoff=False,activebackground=cl_lightblue,activeforeground="black")
        self.aboutMenu.add_command(label="About",command=lambda:self.createAbout())
        #MainMenu >> Cascade
        self.mainMenu.add_cascade(label="Profile",menu=self.profileMenu)
        self.mainMenu.add_cascade(label="About",menu=self.aboutMenu)
        
        #>>Inputting Income Frame (LEFT)
        self.financeFrameTempLabel = [] 
        self.financeFrameP = FinanceFrame(self.app,text="")
        self.financeFrame = tk.Frame(self.financeFrameP,width=320,height=480-48)
        self.financeFrameCanv = tk.Canvas(self.financeFrame,width=320,height=480-48)
        self.financeFrameP.place(relx=0.01,rely=0.005,anchor=tk.NW)
        self.financeFrame.pack(padx=3,pady=3)
        self.financeFrameCanv.pack()
        #income title in top
        self.incomeTitle = tk.Label(self.financeFrame,text="Income",bg="blue",fg="white")
        self.incomeTitle.place(relx=0.01,rely=0.005,anchor=tk.NW)
        #expenses title in top
        self.expensesTitle = tk.Label(self.financeFrame,text="Expense",bg="red",fg="white")
        self.expensesTitle.place(relx=0.5,rely=0.005,anchor=tk.NW)
        #create separate line
        self.financeFrameCanv.create_line((0,375,380,375))
        #entry for user to input a number
        self.inputNumber = tk.Entry(self.financeFrame,bg=cl_lightblue)
        self.inputNumber.place(relx=0.0125,rely=0.875,anchor=tk.NW)
        #command for input data button
        _incomeCommand = lambda:self.inputFinanceData(self.inputNumber.get(),0,self.day.get())
        _expensesCommand = lambda:self.inputFinanceData(self.inputNumber.get(),1,self.day.get())
        #input data button
        self.inputIncome = inputDataButton(0.01,0.93,"inc",self.financeFrame,text="+Income",relief=tk.GROOVE,command=_incomeCommand)
        self.inputExpenses = inputDataButton(0.20,0.93,"exp",self.financeFrame,text="-Expenses",relief=tk.GROOVE,command=_expensesCommand)
        #reset button
        self.resetButton = tk.Button(self.financeFrame,text="Reset",relief=tk.GROOVE,bg=cl_lightred,command=lambda:self.resetDayFinance(self.day.get()))
        self.resetButton.place(relx=0.875,rely=0.93,anchor=tk.NW)

        #>>Selecting Day Frame (RIGHT)
        self.dayFrameP = tk.LabelFrame(self.app,text="Days")
        self.dayFrame = tk.Frame(self.dayFrameP,width=275,height=150)
        self.dayFrameP.place(relx=0.545,rely=0.005,anchor=tk.NW)
        #calculate button
        self.calculate = tk.Button(self.dayFrame,text="Calculate",command=lambda : self.calculateFinance(),bg=cl_lightblue,relief=tk.GROOVE)
        self.calculate.place(relx=0.475,rely=0.82,anchor=tk.N)
        #create the main day button
        for i in range(0,10):
            x = 0+(i*0.1)
            text = " "+str(i+1)+" "
            if i == 9:
                text = str(i+1)
            self.daysObject.append(dayButton(x,0.1,self.dayFrame,text=text,variable=self.day))
        for i in range(10,20):
            x = 0+((i-10)*0.1)
            self.daysObject.append(dayButton(x,0.35,self.dayFrame,text=str(i+1),variable=self.day))
        for i in range(20,31):
            x = 0+((i-20)*0.1)
            self.daysObject.append(dayButton(x,0.61,self.dayFrame,text=str(i+1),variable=self.day))
        #set command for day button
        for dayObject in self.daysObject:
            dayObject.config(command=lambda:self.updatingFinanceFrame(self.day.get()))
        self.dayFrame.pack(padx=3,pady=3)
        #set the app menu to this main menu
        self.app.config(menu=self.mainMenu)
    def createAbout(self):
        #create main
        self.aboutMain = tk.Toplevel(self.app)
        self.aboutMain.resizable(0,0)
        self.aboutMain.geometry("400x200")
        self.aboutMain.title("About")
        #create main gui
        aboutLabelText = "MonthlyIncome\n=>calculate your income and expenses for a month<=\ncreated by Aghnat HS"
        self.aboutLabel = tk.Label(self.aboutMain,text=aboutLabelText)
        self.aboutLabel.place(relx=0.5,rely=0,anchor=tk.N)
        #focusing and looping
        self.aboutMain.focus()
        self.aboutMain.mainloop()
    
    """
        FinanceFrame
    """
    def updatingFinanceFrame(self,day):
        #destroy previous label
        for tempLabel in self.financeFrameTempLabel:
            tempLabel.destroy()
        #set title
        self.financeFrameP.updateTitle(day,PROFILE)

        #base variable
        dayNow = self.daysFinance[str(day)]
        #>>Income Label
        for i in range(len(dayNow[0])):
            incomeText = "+" + threeDigit(str(dayNow[0][i]))
            self.financeFrameTempLabel.append(incomeLabel(0.01,0.075+(i*0.05),self.financeFrame,text=incomeText))

        #>>Expenses Label
        for i in range(len(dayNow[1])):
            expensesText = "-" + threeDigit(str(dayNow[1][i]))
            self.financeFrameTempLabel.append(incomeLabel(0.5,0.075+(i*0.05),self.financeFrame,text=expensesText))         

    """
        Load and Save System
    """
    def resetDayFinance(self,day):
        global RESET_VALUE
        #reset value of current data day
        self.daysFinance[str(day)] = RESET_VALUE
        #realtime updating
        self.updatingFinanceFrame(day)    
    def newFinanceProfile(self):
        global PROFILE
        #store last profile directory
        tempDir = PROFILE
        PROFILE = askSaveAsFileName(title="New Profile",initialdir=PROFILE_DIR,defaultextension=".json",filetypes=[("profile files","*.json")])
        
        #if user cancel the procedure 
        if PROFILE == "" :
            #set the profile to last profile
            PROFILE = tempDir
        else:
            json.save_json(defaultJson,PROFILE)
            self.daysFinance = json.load_json(PROFILE )
            self.updatingFinanceFrame(self.day.get())
    def loadFinanceProfile(self,preventCancel=False):
        global PROFILE
        #store last profile directory
        tempDir = PROFILE
        PROFILE = askOpenFileName(title="Select Profile",initialdir=PROFILE_DIR,filetypes = [("profile files","*.json")])
        #if user cancel the procedure 
        if PROFILE == "" :
            #set the profile to last profile
            PROFILE = tempDir
            #prevent user to cancel 
            if preventCancel == True:
                if MessageBox.askyesno("Please Select a Profile","Do you want to quit?"):
                    self.app.destroy()
                else:
                    self.loadFinanceProfile(preventCancel=True)
        else:
            self.daysFinance = json.load_json(PROFILE)
            self.updatingFinanceFrame(self.day.get())
    def saveFinanceProfile(self):
        #save base data to json 
        json.save_json(self.daysFinance,PROFILE)
        MessageBox.showinfo("Saving Successfull",f"Profile Saved in:\n{PROFILE}")

    """
        Calculating System
    """
    def calculateFinance(self):  
        incomeList = []
        expensesList = []
        #get income and expenses in 30 days
        for day in range(1,31):
            for index in range(0,2):
                for amount in range(len(self.daysFinance[str(day)][index])):
                    if index == 0: incomeList.append(int(self.daysFinance[str(day)][index][amount]))
                    elif index == 1: expensesList.append(int(self.daysFinance[str(day)][index][amount]))
        
        #summary
        income = sum(incomeList)
        expenses = sum(expensesList)
        incomePerDay =  threeDigit("{:.2f}".format(income/30))
        expensesPerDay =  threeDigit("{:.2f}".format(expenses/30))
        summary = income - expenses
        #set the summary to minus or plus
        if copysign(1,summary) == 1:
            summary = "+" + threeDigit(summary)
        else:
            summary = "-" + threeDigit(str(summary).replace("-",""))
        #show the summary
        MessageBox.showinfo("Summary",f"income = {threeDigit(income)}\nexpenses = {threeDigit(expenses)}\nAverage Income/Day = {incomePerDay}\nAverage Expenses/Day = {expensesPerDay}\nSummary = {summary}")

    """
        Inputting Data
    """
    def inputFinanceData(self,amount,index,day):
        amount = str(amount)
        #try if input from user is a valid integer
        try:
            int(amount)
        except ValueError:
            MessageBox.showerror("Wrong Input","Please input a integer number \nex:12345")
        else:
            amount = amount.replace("-","")
            amount = amount.replace("+","")
            #add input from user to base data
            dayNow = self.daysFinance[str(day)]
            dayNow[index].append(amount)
            self.inputNumber.delete(0, 'end')
            #realtime update
            self.updatingFinanceFrame(day)      



base = App()
