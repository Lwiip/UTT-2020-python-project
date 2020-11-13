
def inputscommandline(headers):
    """
    Return dictionnary with inputs from user and array of column to sort

    :param headers: array, headers from the file imported
    """

    #init
    dfilter = {}
    asort = []

    for header in headers:
        print("-------------------column: {0}, choice, if null press enter".format(header))

        #Selection of columns to keep
        dfilter["cselect_{0}".format(header)] = bool(input ("Do you want to delete the column (yes or nothing (for no)): "))
        if dfilter["cselect_{0}".format(header)] == '':
            dfilter["cslect_{0}".format(header)] = False
        if dfilter["cselect_{0}".format(header)] == True:
            continue

        #Selection to know which column to sort in ascending mode or descending
        sort = input ("Do you want to sort this column (enter yes or nothing, default is no): ")
        if sort == 'yes':
            asort.append(header)
            ascordesc = input ("True for ascending (or nothing), False for descending: ")
            if ascordesc == "True" or ascordesc == "":
                dfilter["csort_{0}".format(header)] = True
            if ascordesc == "False":
                dfilter["csort_{0}".format(header)] = False

        #Selection of regex to apply
        dfilter["cregex_{0}".format(header)] = input ("Enter a regex: ")
        if dfilter["cregex_{0}".format(header)] == '':
            dfilter["cregex_{0}".format(header)] = '.*'

    return dfilter, asort