# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import pandas as pd


def getinputsGraphic(dfilterb, asort, headers):
    
    print("coucou")

    dfilter = {}
    for header in headers:
        #get checkbox and save it in dfilter
        dfilter["cselect_{0}".format(header)] = dfilterb["cselect_{0}".format(header)].get()

    print(dfilter)


def setinputsGraphic(headers):

    #init neede for graphic interface 
    totalcolumn = len(headers)
    size = round((1920/totalcolumn)/9)
    count = 0

    #init same model as dfilter command line but for button
    dfilterb = {}
    asort = []
    
    for header in headers:
        #grid configuration (take all the space and add a little of padding)
        inputsFrame.columnconfigure(count, weight=1,pad=0.1)

        #label to print column name
        label = Label(inputsFrame,text=header, width=size)
        label['font']=('Arial', 8)
        label.grid(row=1, column=count)

        #checkbutton selection
        dfilterb["cselect_{0}".format(header)] = tk.BooleanVar() 
        check = Checkbutton(inputsFrame, text='delete column', width=size, var=dfilterb["cselect_{0}".format(header)])
        check.grid(row=2, column=count)

        #regex inputs
        value = StringVar() 
        value.set(".*")
        entree = Entry(inputsFrame, textvariable=value,width=size)
        entree.grid(row=3, column=count)

        #sort inputs
        bouton = Button(inputsFrame,text='sort',width=size)
        bouton.grid(row=4, column=count)

        count = count + 1 

    #button compute
    buttonCompute = Button(commandFrame, text="Compute", command = lambda: getinputsGraphic(dfilterb, asort, headers))
    buttonCompute.place(relx=0.2, rely=0.1)

    return dfilterb, asort
    

#function to show the table
def showTable(pd):

    tree["column"] = list(pd.columns)
    tree["show"] = "headings"

    #show table headers
    for column in tree["column"]:
        tree.heading(column, text = column)

    #show table values
    dfRows = pd.to_numpy().tolist()
    for row in dfRows:
        tree.insert("", "end", values = row)



#function to open log file
def OpenFile():
    log= askopenfilename(initialdir="./",
                           filetypes =(("Csv Files",".csv"),("All Files",".*")),
                           title = "Choose a file."
                           )
    print (log)
    #Using try in case user types in unknown file or closes without choosing a file.
    try:
        with open(log,"r") as UseFile:
            data = pd.read_csv(UseFile, header=0, sep=';')
            headers = []
            headers = list(data.columns)
            

            #Clean widget, needed if you open another file
            for widget in tree.winfo_children():
                widget.destroy()
            for widget in inputsFrame.winfo_children():
                widget.destroy()
            
            #setinputs function
            dfilter, asort = setinputsGraphic(headers)
            #showTable function
            showTable(data)
            #getinputs
            #getinputsGraphic(dfilter, asort, headers)
        
    #Exception handling
    except FileNotFoundError:
        messagebox.showerror("No file exists")
    except:
        messagebox.showerror("Error")

        

    
  

#main window     
fenetre = Tk()
fenetre.geometry('1920x1080')
fenetre.resizable(1, 1)
Title = fenetre.title( "Projet Python")

#Command Panel
commandFrame = ttk.LabelFrame(fenetre, text="Commande")
commandFrame.place(relx=0, rely=0.02, height=50, width=1920)
buttonFile = Button(commandFrame, text="File", command = OpenFile)
buttonFile.place(relx=0, rely=0.1)


#Inputs Panel
inputsFrame = ttk.LabelFrame(fenetre, text="Inputs")
inputsFrame.place(relx=0, rely=0.09, height=120, width=1920)
#scrollbar = Scrollbar(inputsFrame, orient='horizontal')
#scrollbar.pack(side = 'top', fill = 'x')


#Table Panel
table = ttk.LabelFrame(fenetre, text="Table")
table.place(relx=0, rely=0.22, height=790, width=1920)
#Treeview
tree = ttk.Treeview(table)
tree.place(rely=0.02, relwidth = 1, relheight = 1)
# Constructing scrollbar 
hsb = ttk.Scrollbar(table,  orient ="horizontal",  command = tree.xview) 
hsb.pack(side ='top', fill ='x') 
vsb = ttk.Scrollbar(table, orient="vertical", command=tree.yview)
vsb.pack(side='right', fill='y')
tree.configure(xscrollcommand = hsb.set, yscrollcommand=vsb.set) 


fenetre.mainloop()