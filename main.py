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
#Create dictionnary, key is the columns of the file, value is the regex pattern and boolean value (print or not print)
dfilter = {}
for header in headers:
    dfilter["cregex_{0}".format(header)] = '.*'
    dfilter["cselect_{0}".format(header)] = True
#Random regex pattern, this will come from the user
dfilter['cregex_nom']='quartier'
dfilter['cregex_lieu']='Louis'
dfilter['cregex_contact']='^iss.*'
#Random select, this will come from the user
dfilter['cselect_nom']=False


##########################
#Apply inputs from user
##########################
#Apply selection
dfdataworking = dfdata.copy()
dfdataworking = filtering.applyselection(dfdataworking, dfilter)

#Apply regex
dfdataregex = filtering.applyregex(dfdataworking, dfilter)
print(dfdataregex)


##########################
#Export to a file
##########################





    

