    
import os

def outfile_csv(outfilename,dfdataworking):
    """
    Generation of the output file in CSV format

    :param outfilename : output file specified by the user
    :param dfdataworking : dataframe with regex applied
    """
   
    #Check if the old file exist and remove
    if os.path.isfile(outfilename):
        print ("INFORMATION : Remove the old file",outfilename)
        os.remove(outfilename) 

    #Create the out file 
    dfdataworking.to_csv (outfilename, header=True,index=True, index_label='NumLine', encoding='utf-8', sep=';')
    print ("INFORMATION : The file",outfilename,"is created")