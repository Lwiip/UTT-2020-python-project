from dateutil.parser import parse
import pandas as pd 


def columnIsDate(df,headers):
    '''
    Return dataframe with updated types

    :param df:dataframe, dataframe from the file imported
    :param headers:array, headers from the file imported
    '''
    count = 0
    #Lecture de la première ligne de données
    for i in df.iloc[0]:
        i = str(i)
        #check if the format is a date
        if isDate(i):
            columnheader = headers[count]
            #type of the column to a date format
            df[columnheader] = pd.to_datetime(df[columnheader])
            count=count+1
        else:
            count=count+1
            continue

    return df


def isDate(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False