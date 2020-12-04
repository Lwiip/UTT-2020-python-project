# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import pandas as pd
#from IPython.display import display


#function to show the table
def showTable(pd):

    tree["column"] = list(pd.columns)
    tree["show"] = "headings"

    totalcolumn = len(tree["column"])
    relativesize = 1 / totalcolumn
    test = 0

    for column in tree["column"]:
        tree.heading(column, text = column)

        #test insertion valeur
        value = StringVar() 
        value.set(column)
        entree = Entry(table, textvariable=value, width=24)
        #entree.pack(side=LEFT)
        entree.place(relx=test, rely=0.02)
        test = test + relativesize 

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

            showTable(data)

    #Exception handling
    except FileNotFoundError:
        messagebox.showerror("No file exists")
    except:
        messagebox.showerror("Error")

    

#main window     
fenetre = Tk()
fenetre.geometry('1344x756')
fenetre.resizable(1, 1)
Title = fenetre.title( "Projet Python")

#Command Panel
commandFrame = ttk.LabelFrame(fenetre, text="Commande")
commandFrame.place(relx=0, rely=0.02, height=100, width=1920)
buttonFile = Button(commandFrame, text="File", command = OpenFile)
buttonFile.place(relx=0, rely=0.1)

#Table Panel
table = ttk.LabelFrame(fenetre, text="Table")
table.place(relx=0, rely=0.15, height=860, width=1920)
#Treeview
tree = ttk.Treeview(table)
tree.place(rely=0.05, relwidth = 1, relheight = 1)

# Constructing scrollbar 
hsb = ttk.Scrollbar(table,  orient ="horizontal",  command = tree.xview) 
hsb.pack(side ='top', fill ='x') 
vsb = ttk.Scrollbar(table, orient="vertical", command=tree.yview)
vsb.pack(side='right', fill='y')
tree.configure(xscrollcommand = hsb.set, yscrollcommand=vsb.set) 


fenetre.mainloop()