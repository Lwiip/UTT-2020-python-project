def applyregex(df, dfilter):
    #Change all the types of the dataframe to str, needed for apply contains function
    df.applymap(str)
    nulpattern = '.*'

    #Apply regex on each collumns
    headers = list(df.columns) 
    for header in headers:
        pattern = str(dfilter["cregex_{0}".format(header)])
        
        if pattern != nulpattern:
            print("=>>>>>>>>>>>>>>>>>>>>>>> ",pattern)
            df = df[df[header].str.contains(pattern)==True]

    return df


def applyselection(df, dfilter):

    headers = list(df.columns) 

    for header in headers:
        selection = dfilter["cselect_{0}".format(header)]
        if not selection:
            del df[header]

    return df
    