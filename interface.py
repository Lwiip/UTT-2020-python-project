#from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile 
import pandas as pd

import filtering
import date
import inputs
import detectdelimiter


def compute(dfdata, dfilterb, dsort, headers):
    """
    Function get user inputs from the GUI, and apply all filters on the dataframe.

    :param dfdata: dataframe, dataframe created with the opened file
    :param dfilterb: dictionnary, dictionnary of inputs needed to build the dictionnary needed to apply filters
    :param dsort: dictionnary, dictionnary needed to build asort (list of columns to sort)
    :param headers: array, headers of the dataframe
    """

    #init
    dfilter = {}
    asort = []

    #get inputs from user and construct dictionnary and array needed for the compute part
    for header in headers:
        #get checkbox and save it in dfilter
        dfilter["cselect_{0}".format(header)] = dfilterb["cselect_{0}".format(header)].get()
        #get regex and save it in dfilter
        dfilter["cregex_{0}".format(header)]= dfilterb["cregex_{0}".format(header)].get()
        
        if dsort["csort_{0}".format(header)].get() == True:
            asort.append(header)
            dfilter["csort_{0}".format(header)] = dfilterb["csort_{0}".format(header)].get()


    ##############################################################################
    #Apply filters
    ##############################################################################
    #Apply selection
    dfdata = filtering.applySelection(dfdata, dfilter)
    #Apply sorting
    if len(asort) != 0:
        dfdata = filtering.applySort(dfdata, asort, dfilter)
    #Apply regex
    dfdata = filtering.applyRegex(dfdata, dfilter)

    ##############################################################################
    #Refresh GUI to show changes
    ##############################################################################
    tree.delete(*tree.get_children()) 
    showTable(dfdata)

    ##############################################################################
    #Button Export to save the dataframe to a file
    ##############################################################################
    #set button save
    buttonSave = tk.Button(commandFrame, text="Save", command = lambda: saveFile(dfdata))
    buttonSave.place(relx=0.9, rely=0.1)


def setinputsGraphic(dfdata, headers):
    """
    Function to setup user inputs in the GUI, and create the compute button to allow user to apply filters on the dataframe.

    :param dfdata: dataframe, dataframe created with the opened file
    :param headers: array, list of headers of the dataframe
    """

    #init needed for graphic interface 
    totalcolumn = len(headers)
    size = round((1920/totalcolumn)/9)
    count = 0

    #init same model as dfilter command line but for button
    dfilterb = {}
    dsort = {}
    asort = []
    
    #setup user inputs in the GUI
    for header in headers:
        #grid configuration (take all the space and add a little of padding)
        inputsFrame.columnconfigure(count, weight=1,pad=0.1)

        #label to print column name
        label = tk.Label(inputsFrame,text=header, width=size)
        label['font']=('Arial', 8)
        label.grid(row=1, column=count)

        #checkbutton selection
        dfilterb["cselect_{0}".format(header)] = tk.BooleanVar() 
        check1 = tk.Checkbutton(inputsFrame, text='delete column', width=size, var=dfilterb["cselect_{0}".format(header)])
        check1.grid(row=2, column=count)

        #regex inputs
        dfilterb["cregex_{0}".format(header)] = tk.StringVar() 
        dfilterb["cregex_{0}".format(header)].set(".*")
        entree = tk.Entry(inputsFrame, textvariable=dfilterb["cregex_{0}".format(header)], width=size)
        entree.grid(row=3, column=count)

        #sort inputs
        dsort["csort_{0}".format(header)] = tk.BooleanVar() 
        check2 = tk.Checkbutton(inputsFrame, text='sort', width=size, var=dsort["csort_{0}".format(header)] )
        check2.grid(row=4, column=count)
        dfilterb["csort_{0}".format(header)] = tk.BooleanVar() 
        check3 = tk.Checkbutton(inputsFrame, text='asc (desc by dft)', width=size, var=dfilterb["csort_{0}".format(header)] )
        check3.grid(row=5, column=count)
        
        count = count + 1 

    #set button compute and launch compute function when the user clic on it.
    buttonCompute = tk.Button(commandFrame, text="Compute", command = lambda: compute(dfdata, dfilterb, dsort, headers))
    buttonCompute.place(relx=0.48, rely=0.1)


#function to show the table
def showTable(df):
    """
    Function to show on the GUI the dataframe

    :param df:dataframe, dataframe to show on the GUI
    """
    tree["column"] = list(df.columns)
    tree["show"] = "headings"

    #show table headers
    for column in tree["column"]:
        tree.heading(column, text = column)

    #show table values
    dfRows = df.to_numpy().tolist()
    for row in dfRows:
        tree.insert("", "end", values = row)
    

#function to open log file
def openFile():
    """
    open a file, autodetect the delimiter and open it as a dataframe. Apply on that dataframe some processing
    """
    #open the GUI explorer file
    log= askopenfilename(initialdir="./",
                           filetypes =(("Csv Files",".csv"),("All Files",".*")),
                           title = "Choose a file"
                           )
    print (log)
    
    #Using try in case user types in unknown file or close without choosing a file.
    try:
        with open(log,"r") as file:
            
            #Clean the tree widget needed to show the dataframe in the GUI, needed if you open another file
            tree.delete(*tree.get_children()) 
            for widget in inputsFrame.winfo_children():
                widget.destroy()   

        
            ##############################################################################
            #Delimiter
            ############################################################################## 
            filename = file.name
            #List of predefined delimiters 
            ddelimiters = {'doublecode':'"','ptvirgule':';', 'virgule':',', 'antislash':'\\', 'arobase':'@', 'pipe':'|'}
            #Automatic detection delimiter 
            finaldelimiter = detectdelimiter.getautodelimiter(filename,ddelimiters)

            ##############################################################################
            #dataframe processing
            ##############################################################################
            dfdata = pd.read_csv(filename,sep=finaldelimiter,engine='python')
            #Get list of headers from the file imported
            headers = list(dfdata.columns)
            #auto detect dates and convert columns to date format if date
            dfdata = date.columnIsDate(dfdata,headers)
            
            
            #setinputs function
            setinputsGraphic(dfdata, headers)
            #showTable function
            showTable(dfdata)
        
    #Exception handling
    except FileNotFoundError:
        tk.messagebox.showerror("No file exists")
    except:
        tk.messagebox.showerror("Error")


def saveFile(dfdata):
    """
    Function to save the filtered dataframe to a csv file.

    :param dfdata: dataframe, filtered dataframe
    """
    #open the GUI explorer to save the file
    file = asksaveasfile(initialdir="./",
                           filetypes =(("Csv Files",".csv"),("All Files",".*")),
                           title = "Save a file"
                           )
    #save the dataframe to a csv 
    dfdata.to_csv(file.name, header=True,index=False, encoding='utf-8', sep=';')
        

    


############################################################################################################################################################
#Interface main
############################################################################################################################################################

#main window     
fenetre = tk.Tk()
fenetre.geometry('1920x1080')
fenetre.resizable(1, 1)
Title = fenetre.title( "Projet Python")

#Command Panel
commandFrame = ttk.LabelFrame(fenetre, text="Commande")
commandFrame.place(relx=0, rely=0.02, height=50, width=1920)
#button file, openFile function
buttonFile = tk.Button(commandFrame, text="File", command = openFile)
buttonFile.place(relx=0.1, rely=0.1)

#Inputs Panel
inputsFrame = ttk.LabelFrame(fenetre, text="Inputs")
inputsFrame.place(relx=0, rely=0.085, height=140, width=1920)

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