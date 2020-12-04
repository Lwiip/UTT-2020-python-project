# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import pandas as pd

def setinputs(pd):
    headers = []
    headers = list(pd.columns)

    totalcolumn = len(headers)
    relativesize = 1 / totalcolumn
    size = round((1920/totalcolumn)/9)
    pos = 0
    count = 0
    

    for column in headers:
        inputsFrame.columnconfigure(count, weight=1,pad=0.1)

        label1 = Label(inputsFrame,text=column, width=size)
        label1['font']=('Arial', 8)
        label1.grid(row=1, column=count)

        check = Checkbutton(inputsFrame, text='select/deselect', width=size)
        check.select()
        check.grid(row=2, column=count)

        value = StringVar() 
        value.set(".*")
        entree = Entry(inputsFrame, textvariable=value,width=size)
        entree.grid(row=3, column=count)

        bouton = Button(inputsFrame,text='sort',width=size)
        bouton.grid(row=4, column=count)

        pos = pos + relativesize 
        count = count + 1 



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
            
            #??? ça sert à quoi ?
            tree.delete(*tree.get_children())

            setinputs(data)
            showTable(data)

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