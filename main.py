import pandas as pd 
import filtering
import date
import inputs
import argparse
import sys
import os

##############################################################################
#Import file, set delimiter, find and convert dates
##############################################################################
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

#auto detect dates and convert columns to date format is date
dfdataworking = date.columnIsDate(dfdataworking,headers)



##############################################################################
#Get info from user
##############################################################################
print(dfdataworking[:5])

#Get data from user in command line style
dfilter, asort = inputs.inputscommandline(headers)


    

##############################################################################
#Apply inputs from user
##############################################################################
print("------------------------------- Init")
print(dfdataworking)

#Apply selection
print("------------------------------- Selection")
dfdataworking = filtering.applySelection(dfdataworking, dfilter)
print(dfdataworking)

#Apply sorting
print("------------------------------- Sorting")
if len(asort) != 0:
    dfdataworking = filtering.applySort(dfdataworking, asort, dfilter)
print(dfdataworking)

#Apply regex
print("------------------------------- Regex")
dfdataregex = filtering.applyRegex(dfdataworking, dfilter)
print(dfdataregex)

##########################v####################################################
#Export to a file
##############################################################################


