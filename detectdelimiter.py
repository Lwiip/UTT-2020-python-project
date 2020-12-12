import operator
import argparse

def computeoccurence(lignes, ddelimiters):
    """
    Adds to a dictionary (dico) the number of each predefined delimiter for the first 5 lines. 

    :param lignes:array, Recovery of the first 5 lines of the file 
    :param ddelimiters:dictionnary, aimed to retrieves the list of defined delimiters 
    """

    #init
    dico = {}
    for key, value in ddelimiters.items():
        dico["{0}".format(key)] = []

    #compute
    for ligne in lignes:
        # Add to dico : 'virgule': [0, 1, 1, 1, 1], 'ptvirgule': [8, 8, 8, 8, 8] ....
        for key, value in ddelimiters.items():  
            dico["{0}".format(key)].append(ligne.count(value))  

    return dico


def getdelimitername(dico):
    """
    Retrieves the dictionary (dico) and count the number of occurrences of the predefined delimiters  

    :param dico:dictionnary, number of each predefined delimiter for each first 5 lines
    """

    dshortlist = {}

    for key, values in dico.items():
        # A set is a collection that only keeps one copy of any object. So set([1,1,1,1,1,1]) is the same as set([1])
        # len(set(values)) == 1 check if all values are the same, if not, it's not the delimiter.
        if len(set(values)) == 1:
            dshortlist[key] = values[0]

    # return the name of the delimiter (max occurence)
    return max(dshortlist.items(), key=operator.itemgetter(1))[0]


def getautodelimiter(filename, ddelimiters):
    """
    Automatic delimiter detection

    :param filename:string, Input filename 
    :param ddelimiters:dictionnary, predefined delimiters
    """

    # Open the file csv or txt
    with open(filename, 'r',encoding="utf-8") as file:
        #read 5 first lines
        lignes = file.readlines()[0:5]
        #return the number of each predefined delimiter for the first 5 lines
        dico2 = computeoccurence(lignes, ddelimiters)
   
    #from the previous return, return the name of the delimiter
    delimitername = getdelimitername(dico2)
    finaldelimiter = ddelimiters[delimitername]

    return finaldelimiter

