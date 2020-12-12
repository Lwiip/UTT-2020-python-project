    
import os

def outfile_csv(outfilename,dfdata):
    """
    Generation of the output file in CSV format

    :param outfilename:string, output file specified by the user
    :param dfdata:dataframe, dataframe with all filters applied
    """
   
    #Check if the old file exist and remove
    if os.path.isfile(outfilename):
        print ("INFORMATION : Remove the old file",outfilename)
        os.remove(outfilename) 

    #Create the out file 
    dfdata.to_csv(outfilename, header=True,index=False, encoding='utf-8', sep=';')
    print ("INFORMATION : The file",outfilename,"is created")