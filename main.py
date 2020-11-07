import pandas as pd 
import filtering

##########################
#Import file and get headers from the file
##########################
#Import data with specific delimiter as a panda dataframe
dfdata = pd.read_csv("sites-agriculture-urbaine.csv",sep=';') 
#Get list of headers from the file imported
headers = list(dfdata.columns) 


##########################
#Get info from user
##########################
#Array sorting
asort = []
asort = ['nom','lieu','cp']

#Create dictionnary, key is the columns of the file, value is the regex pattern, boolean value (print or not print), boolean value (ascending, descnedning or None sorting)
dfilter = {}
for header in headers:
    dfilter["cregex_{0}".format(header)] = '.*'
    dfilter["cselect_{0}".format(header)] = True
    dfilter["csort_{0}".format(header)] = None
#Random regex pattern, this will come from the user
dfilter['cregex_nom']='quartier'
dfilter['cregex_contact']='^iss.*'
#Random select, this will come from the user
dfilter['cselect_nom']=False
#Random sort, this will ccome from the user
dfilter['csort_nom']=False
dfilter['csort_lieu']=True
dfilter['csort_cp']=True



##########################
#Apply inputs from user
##########################
dfdataworking = dfdata.copy()
print(dfdataworking)
print("-------------------------------")

#Apply sorting
dfdataworking = filtering.applysort(dfdataworking, asort, dfilter)
print(dfdataworking)
print("-------------------------------")

#Apply selection
dfdataworking = filtering.applyselection(dfdataworking, dfilter)
print(dfdataworking)
print("-------------------------------")

#Apply regex
dfdataregex = filtering.applyregex(dfdataworking, dfilter)
print(dfdataregex)

##########################
#Export to a file
##########################





    

