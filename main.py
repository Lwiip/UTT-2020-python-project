import pandas as pd 

#Import data with specific delimiter as a panda dataframe
dfdata = pd.read_csv("sites-agriculture-urbaine.csv",sep=';') 

#Get list of headers from the file imported
headers = list(dfdata.columns) 

#Create dictionnary, key is the collumns of the file, value is the regex pattern
dfilter = {}
for header in headers:
    dfilter["cfilter_{0}".format(header)] = '.*'

#Random regex pattern, this will come from the user
dfilter['cfilter_nom']='quartier'
dfilter['cfilter_lieu']='Louis'
dfilter['cfilter_contact']='^iss.*'


#Change all the types of the dataframe to str, needed for apply contains function
dfdatacopy = dfdata.applymap(str)
#print (dfdatacopy.dtypes)


for header in headers:
    pattern = str(dfilter["cfilter_{0}".format(header)])
    print("=>>>>>>>>>>>>>>>>>>>>>>> ",pattern)
    dfdatacopy = dfdatacopy[dfdatacopy[header].str.contains(pattern)==True]
print(dfdatacopy)    








    

