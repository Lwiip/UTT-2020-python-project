from dateutil.parser import parse
import pandas as pd 


def columnIsDate(df,headers):
    count = 0
    for i in df.iloc[0]:
        i = str(i)
        if isDate(i):
            columnheader = headers[count]
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