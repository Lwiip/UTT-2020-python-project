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
#Import file
###################################################
parser = argparse.ArgumentParser()
parser.add_argument("-g", "--graphic", help="Indicate to open the program in graphical mode", action="store_true")  
parser.add_argument("-f", "--file", help="Indicate the csv or txt file to be processed")   
parser.add_argument("-d", "--delimiter", help='Specify the file delimiter [Example: -d ";"] otherwise by default the delimiter is detected automatically.')   
parser.add_argument("-o", "--outfile", help='Specify the name of the csv file to export the result' )
args = parser.parse_args()


#if -g option, open interface script
if args.graphic is not False:
    import interface
    sys.exit()

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
#Retrieve the delimiter specified in the command line 
if args.delimiter:
    finaldelimiter = args.delimiter 
else:
    #List of predefined delimiters 
    ddelimiters = {'doublecode':'"','ptvirgule':';', 'virgule':',', 'antislash':'\\', 'arobase':'@', 'pipe':'|'}
    #Automatic detection of the delimiter 
    finaldelimiter = detectdelimiter.getautodelimiter(filename,ddelimiters)


##############################################################################
#dataframe processing
##############################################################################
dfdata = pd.read_csv(filename,sep=finaldelimiter,engine='python')

#Get list of headers from the file imported
headers = list(dfdata.columns)
#auto detect dates and convert columns to date format if date
dfdata = date.columnIsDate(dfdata,headers)


##############################################################################
#Get info from user
##############################################################################
print(dfdata[:5])

#Get data from user in command line style, return dictionnary and array
dfilter, asort = inputs.inputscommandline(headers)

   
##############################################################################
#Apply filters
##############################################################################
print("------------------------------- Init")
print(dfdata[:5])

#Apply selection
print("------------------------------- Selection")
dfdata = filtering.applySelection(dfdata, dfilter)
print(dfdata[:5])

#Apply sorting
print("------------------------------- Sorting")
if len(asort) != 0:
    dfdata = filtering.applySort(dfdata, asort, dfilter)
print(dfdata[:5])

#Apply regex
print("------------------------------- Regex")
dfdata = filtering.applyRegex(dfdata, dfilter)
print(dfdata[:5])


##############################################################################
#Export to a file
##############################################################################
#if -o option (outfile)
if args.outfile:

    #Define the out filename
    outfilename=args.outfile

    #Generating the output file in CSV
    print("------------------------------- outfile")
    outfile.outfile_csv(outfilename,dfdata)

