from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import pandas as pd

import filtering
import date
import inputs
import detectdelimiter


##############################################################################
#Graphic functions
##############################################################################

def getinputsGraphic(dfilterb, dsort, headers):

    dfilter = {}
    asort = []
    for header in headers:
        #get checkbox and save it in dfilter
        dfilter["cselect_{0}".format(header)] = dfilterb["cselect_{0}".format(header)].get()
        #get regex and save it in dfilter
        dfilter["cregex_{0}".format(header)]= dfilterb["cregex_{0}".format(header)].get()
        
        if dsort["csort_{0}".format(header)].get() == True:
            asort.append(header)
            dfilter["csort_{0}".format(header)] = dfilterb["csort_{0}".format(header)].get()

    print(asort)
    print(dfilter)


def setinputsGraphic(headers):

    #init neede for graphic interface 
    totalcolumn = len(headers)
    size = round((1920/totalcolumn)/9)
    count = 0

    #init same model as dfilter command line but for button
    dfilterb = {}
    dsort = {}
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
        check1 = Checkbutton(inputsFrame, text='delete column', width=size, var=dfilterb["cselect_{0}".format(header)])
        check1.grid(row=2, column=count)

        #regex inputs
        dfilterb["cregex_{0}".format(header)] = StringVar() 
        dfilterb["cregex_{0}".format(header)].set(".*")
        entree = Entry(inputsFrame, textvariable=dfilterb["cregex_{0}".format(header)], width=size)
        entree.grid(row=3, column=count)

        #sort inputs
        #bouton = Button(inputsFrame,text='sort',width=size, command= lambda: sortbutton(header))
        #bouton.
        dsort["csort_{0}".format(header)] = tk.BooleanVar() 
        check2 = Checkbutton(inputsFrame, text='sort', width=size, var=dsort["csort_{0}".format(header)] )
        check2.grid(row=4, column=count)

        dfilterb["csort_{0}".format(header)] = tk.BooleanVar() 
        check3 = Checkbutton(inputsFrame, text='asc/desc', width=size, var=dfilterb["csort_{0}".format(header)] )
        check3.grid(row=5, column=count)
        

        count = count + 1 


    #set button compute
    buttonCompute = Button(commandFrame, text="Compute", command = lambda: getinputsGraphic(dfilterb, dsort, headers))
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
        
    #Exception handling
    except FileNotFoundError:
        messagebox.showerror("No file exists")
    except:
        messagebox.showerror("Error")

        

    


##############################################################################
#Interface
##############################################################################

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
inputsFrame.place(relx=0, rely=0.085, height=140, width=1920)
#scrollbar = Scrollbar(inputsFrame, orient='horizontal')
#scrollbar.pack(side = 'top', fill = 'x')


#Table Panel
table = ttk.LabelFrame(fenetre, text="Table")
table.place(relx=0, rely=0.24, height=770, width=1920)
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