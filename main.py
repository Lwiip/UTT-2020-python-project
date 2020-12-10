import pandas as pd 
import filtering
import date
import inputs
import argparse
import outfile
import sys
import os
import detectdelimiter
from pathlib import Path

###################################################
#Import file, set delimiter, find and convert dates
###################################################
parser = argparse.ArgumentParser()
parser.add_argument("-g", "--graphic", help="Indicate to open the program in graphical mode", action="store_true")  
parser.add_argument("-f", "--file", help="Indicate the csv or txt file to be processed")   
parser.add_argument("-d", "--delimiter", help='Specify the file delimiter [Example: -d ";"] otherwise by default the delimiter is detected automatically.')   
parser.add_argument("-e", "--outfile", help='Specify the name of the csv file to export the result' )
args = parser.parse_args()


if args.graphic is not False:
    import interface
    sys.exit()
    #exec(open('interface.py').read())

if args.file and not args.graphic:
    #Retrieving the file specified in the command line
    filename=args.file 

    #Check if the file specified in the command line exists 
    if not os.path.isfile(filename): 
        print ("ERROR :", filename,"file not found")
        sys.exit()
else:
    print ("ERROR: indicate the csv or txt filename to be processed, or choose graphic option")
    sys.exit()


##############################################################################
#Get the delimiter
##############################################################################
if args.delimiter:
    #Retrieve the delimiter specified in the command line 
    finaldelimiter = args.delimiter 
else:
    #List of predefined delimiters 
    ddelimiters = {'doublecode':'"','ptvirgule':';', 'virgule':',', 'antislash':'\\', 'arobase':'@', 'pipe':'|'}
    #Automatic detection delimiter 
    finaldelimiter = detectdelimiter.getautodelimiter(filename,ddelimiters)


##############################################################################
#dataframe processing
##############################################################################
dfdata = pd.read_csv(filename,sep=finaldelimiter,engine='python')

#Copy the dataframe
dfdataworking = dfdata.copy()
#Get list of headers from the file imported
headers = list(dfdataworking.columns)
#auto detect dates and convert columns to date format if date
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
dfdataworking = filtering.applyRegex(dfdataworking, dfilter)
print(dfdataworking)


##########################v####################################################
#Export to a file
##############################################################################
if args.outfile:

    #Define the out file
    outfilename=args.outfile

    #Generating the output file in CSV
    print("------------------------------- outfile")
    outfile.outfile_csv(outfilename,dfdataworking)

