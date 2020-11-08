import pandas as pd 
import filtering
import argparse
import sys
import os

##########################
#Import file and get headers from the file
##########################
#Import data with specific delimiter as a panda dataframe
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="Indicate the csv or txt file to be processed")   
parser.add_argument("-d", "--delimiter", help='Specify the file delimiter. By default the delimiter is ";" [Example: -d ","]')   
args = parser.parse_args()
if args.file:
    filename=args.file #Retrieving the file specified in the command line
else:
    print ("error: indicate the csv or txt filename to be processed")
    sys.exit()

if args.delimiter:
    sepfile=args.delimiter #Retrieve the delimiter specified in the command line 
else:
    #Default Delimiter ";"
    sepfile="\;"

#Checks if the file specified in the command line exists 
if not os.path.isfile(filename):
    print (filename,": File not found")
    sys.exit()

dfdata = pd.read_csv(filename,sep=sepfile,engine='python')

#Copy the dataframe
dfdataworking = dfdata.copy()

#Get list of headers from the file imported
headers = list(dfdataworking.columns)
dfdataworking['date'] = pd.to_datetime(dfdataworking['date'])


##########################
#Get info from user
##########################
#Array sorting
asort = []
asort = ['date']

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
#dfilter['csort_nom']=False
#dfilter['csort_lieu']=True
dfilter['csort_date']=True



##########################
#Apply inputs from user
##########################
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





    

