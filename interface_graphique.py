# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import pandas as pd
#from IPython.display import display




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
            #lec=UseFile.read()
            #print(UseFile.readline())
            data = pd.read_csv(UseFile, header=0, sep=';')
            #print(data)
            
            #df = pd.read_csv(lec)
            #pd.options.display.max_columns = None
            #lec changé par df

            tv.delete(*tv.get_children())
            
            tv["column"] = list(data.columns)
            tv["show"] = "headings"

            for column in tv["column"]:
                tv.heading(column, text = column)

            dfRows = data.to_numpy().tolist()
            #print(dfRows)
            for row in dfRows:
                tv.insert("", "end", values = row)

                #my_text.insert(END,lec)

    except FileNotFoundError:
        messagebox.showerror("No file exists")

    except:
        messagebox.showerror("Error")

        
utt = Tk()
utt.geometry("5000x500")
utt.resizable(1, 1)

Title = utt.title( "Projet Python")
my_text = ttk.LabelFrame(utt, text="Excel Data")
my_text.place(height=300, width=6000)

actionFrame = ttk.LabelFrame(utt, text="Commande")
#my_text.pack(pady=20)
actionFrame.place(height=100, width=6000, rely=0.8, relx=0)

buttonFile = Button(actionFrame, text="File", command = OpenFile)
buttonFile.place(rely=0.75, relx=0.1)

"""buttonApply = Button(actionFrame, text="Apply")
buttonFile.place(rely=0.7, relx=0.1)

buttonReset = Button(actionFrame, text="Reset")
buttonFile.place(rely=0.7, relx=0.4)"""

tv = ttk.Treeview(my_text)
tv.place(relwidth = 1, relheight = 1)

#scrolly = Scrollbar(my_text, orient="vertical")
#scrollx = Scrollbar(my_text, orient="horizontal")
scrolly.pack(side="left", fill="y")
scrollx.pack(side="bottom", fill="x")

tv.configure(xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)

#Menu Bar creation

"""
menu = Menu(utt)
utt.config(menu=menu)

file = Menu(menu)

file.add_command(label = 'Open', command = OpenFile)
file.add_command(label = 'Exit', command = utt.quit)

menu.add_cascade(label = 'File', menu = file)


#regex label


regex=Button(utt,text="Commande Regex")
#entryRegex.place(x=300,y=100)
champregex= Entry(utt)


regex.grid(row=1, column=0)
champregex.grid(row=2, column=0)
apply=Button(utt,text="Apply")
apply.grid(row=3,column=14)
reset=Button(utt,text="Reset")
reset.grid(row=4,column=14)
"""

#checking list


utt.mainloop()