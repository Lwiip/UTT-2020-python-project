import pandas as pd 


def applyRegex(df, dfilter):
    """
    Return a dataframe with regex applied

    :param df: dataframe, dataframe under filtering
    :param dfilter: dictionnary, dictionnary with inputs from the user (including regex)
    """

    #Change all the types of the dataframe to str, needed to apply functions
    df.applymap(str)
    nulpattern = '.*'

    #Apply regex on each collumns
    headers = list(df.columns) 
    for header in headers:
        pattern = str(dfilter["cregex_{0}".format(header)])
        
        if pattern != nulpattern:
            if df[header].dtypes == 'datetime64[ns]':
                #if the type of the column is date, need to first translate it to string to apply regex.
                df = df[df[header].apply(lambda x: x.strftime('%Y-%m-%d')).str.contains(pattern)==True]
            elif df[header].dtypes != object:
                #if the type of the column is not object (for example int) need to first translate it to string to apply regex.
                df = df[df[header].apply(str).str.contains(pattern)==True]
            else:
                df = df[df[header].str.contains(pattern)==True]

    return df



def applySelection(df, dfilter):
    """
    Return a dataframe with selection applied

    :param df: dataframe, dataframe under filtering
    :param dfilter: dictionnary, dictionnary with inputs from the user (including selections of columns)
    """

    headers = list(df.columns) 

    for header in headers:
        selection = dfilter["cselect_{0}".format(header)]
        if selection:
            #delete the column
            del df[header]

    return df


def applySort(df, asort, dfilter):
    """
    Return a dataframe with sorting applied

    :param df: dataframe, dataframe under filtering
    :param asort: array, sepeify which colummn needs to be sorted
    :param dfilter: dictionnary, dictionnary with inputs from the user (including type of sort (ascending or descending)
    """

    sorttype = []
    asortupper = []
    asortcustom = []

    for sortcolumn in asort:
        #Create array for the type of sorting (True ascending, False descending)
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

    