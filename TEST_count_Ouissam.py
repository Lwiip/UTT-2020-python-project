import argparse
import csv
import os
import sys

import pandas as pd

import date
import filtering

##########################
#Import file, set delimiter, find and convert dates
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
    sepfile=";"

#Checks if the file specified in the command line exists 
if not os.path.isfile(filename):
    print (filename,": File not found")
    sys.exit()


print ("STEP 1 : -------------------------------------------------------------------")
with open(filename, 'r',encoding="utf-8") as f:
    reader=csv.reader(f,delimiter=sepfile)
    lignes = f.readlines()[0:5]
    for ligne in lignes:
        print (ligne)


print ("STEP 2 : -------------------------------------------------------------------")
with open(filename, 'r',encoding="utf-8") as f:
    reader=csv.reader(f,delimiter=sepfile)
    dfdata = pd.DataFrame([reader], index = None) 
    for val in list(dfdata[4]): 
        print(val)

print ("STEP 2.1 : -------------------------------------------------------------------")
dico = {'ptvirgule':[], 'virgule':[], 'antislash':[], 'arobase':[], 'pipe':[], 'espace':[]}
boucle=0
with open(filename, 'r',encoding="utf-8") as f:
    lignes = f.readlines()[0:5]
    for ligne in lignes:
        boucle=boucle+1
        vptvirgule=ligne.count(";")
        dico['ptvirgule'].append(vptvirgule)
        vvirgule=ligne.count(",")
        dico['virgule'].append(vvirgule)
        vantislash=ligne.count("\\")
        dico['antislash'].append(vantislash)
        varobase=ligne.count("@")
        dico['arobase'].append(varobase)
        vpipe=ligne.count("|")
        dico['pipe'].append(vpipe)
        vespace=ligne.count(" ")
        dico['espace'].append(vespace)
    for key,values in dico.items():
        print (key,values)
        print (values[0] == values[1])
        print (values[0] == values[2])
        print (values[0] == values[3])
        print (values[0] == values[4])
    
print ("STEP 3 : -------------------------------------------------------------------")
ptvirgule=0
virgule=0
antislash=0
arobase=0
pipe=0
espace=0

with open(filename, 'r',encoding="utf-8") as f:
    lignes = f.readlines()[0:5]
    for ligne in lignes:
        print ("\n == BOUCLE FOR == ", ligne)
        print ("===> i=';'",ligne.count(";"))
        ptvirgule=ptvirgule+ligne.count(";")
        print ("===> i=','",ligne.count(","))
        virgule=virgule+ligne.count(",")
        print ("===> i='\\'",ligne.count("\\"))
        antislash=antislash+ligne.count("\\")
        print ("===> i='@'",ligne.count("@"))
        arobase=arobase+ligne.count("@")
        print ("===> i='|'",ligne.count("|"))
        pipe=pipe+ligne.count("|")
        print ("===> i=' '",ligne.count(" "))
        espace=espace+ligne.count(" ")

if ptvirgule == max(ptvirgule,virgule,antislash,arobase,pipe,espace):
    print ("ptvirgule:",ptvirgule)
elif virgule == max(ptvirgule,virgule,antislash,arobase,pipe,espace):
    print ("virgule:",virgule)
elif antislash == max(ptvirgule,virgule,antislash,arobase,pipe,espace):
    print ("antislash:",antislash)
elif arobase == max(ptvirgule,virgule,antislash,arobase,pipe,espace):
    print ("arobase:",arobase)
elif pipe == max(ptvirgule,virgule,antislash,arobase,pipe,espace):
    print ("pipe:",pipe)
elif espace == max(ptvirgule,virgule,antislash,arobase,pipe,espace):
    print ("espace:",espace)

print ("ptvirgule=",ptvirgule,"virgule=",virgule,"antislash=",antislash,"arobase=",arobase,"pipe=",pipe,"espace=",espace)


print ("STEP 4 : -------------------------------------------------------------------")
CSV_Filename="OUTFILE.csv"
if os.path.isfile(CSV_Filename):
    print ("Suppression de l'ancien fichier:",CSV_Filename)
    os. remove(CSV_Filename)   #Suppression du fichier
    
with open(filename, 'r',encoding="utf-8") as infile, open(CSV_Filename,'w') as outfile: 
    for line in infile: 
        outfile.write(line.replace(' ',';'))

if os.path.isfile(filename):
    print (CSV_Filename,": Fichier créé")

print ("################################# FIN #################################")
