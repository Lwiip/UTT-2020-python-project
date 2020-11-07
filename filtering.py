import pandas as pd 

'''
Not optimized because recalculate each time all columns, change needed
'''
def applyregex(df, dfilter):
    #Change all the types of the dataframe to str, needed for apply contains function
    df.applymap(str)
    nulpattern = '.*'

    #Apply regex on each collumns
    headers = list(df.columns) 
    for header in headers:
        pattern = str(dfilter["cregex_{0}".format(header)])
        
        if pattern != nulpattern:
            #print("=>>>>>>>>>>>>>>>>>>>>>>> ",pattern)
            df = df[df[header].str.contains(pattern)==True]

    return df



def applyselection(df, dfilter):

    headers = list(df.columns) 

    for header in headers:
        selection = dfilter["cselect_{0}".format(header)]
        if not selection:
            del df[header]

    return df



'''
Sort by dates needs to be implemented
'''
def applysort(df, asort, dfilter):

    sorttype = []
    asortupper = []
    asortcustom = []

    for sortcolumn in asort:
        #Create array for the type of sorting (True ascending, Fasle descending)
        sorttype.append(dfilter["csort_{0}".format(sortcolumn)])

        #check if the column is of type object
        if df[sortcolumn].dtypes == object:
            #Create new column with uppercase to sort ignoring the case
            df["cupper_{0}".format(sortcolumn)] = df[sortcolumn].str.upper()
            #Create array with new name of upper columns needed to delete after the upper column 
            asortupper.append("cupper_{0}".format(sortcolumn))
            asortcustom.append("cupper_{0}".format(sortcolumn))
        else:
            asortcustom.append(sortcolumn)
    
    #sort with upper columns
    df.sort_values(by=asortcustom, inplace=True, ascending=sorttype) 

    #delete upper columns
    for column in asortupper:
         del df[column] 
    
    return df

    