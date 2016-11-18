"""
Created on June 15 15:25:01 2016

@author: Xianguang yan

"""
import csv
import sys
import os

from ABIFReader import *
from os.path import isdir, isfile, join


# runs the translation script
# Converts name field .FSA -> .CSV
def convertFSA(fileName):
    csvList = fileName.split('.')
    csvList[1] = '.csv'
    return ''.join(csvList)


# Converts Data FSA -> CSV
def script(directory, destination, name):
    """
    Main function that does conversion from FSA -> CSV
    :param directory:
    :param destination:
    :param name:
    :return:
    """
    reader3 = ABIFReader(directory)
    data = [reader3.getData('DATA', 1), reader3.getData('DATA', 2), reader3.getData('DATA', 3),
            reader3.getData('DATA', 4), reader3.getData('DATA', 105)]
    csvName = convertFSA(name)
    print 'Created this file: ' + csvName
    print 'Got Data...'
    print 'Writing Data...'
    print 'Data directory with csv file: ' + destination
    os.chdir(destination)
    print csvName

    # Writes To Destination
    with open(csvName, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(['Blue', 'Green', 'Yellow', 'Red', 'Orange'])
        writer.writerows(zip(*data))

if __name__ == "__main__":
    directory = '/Users/kevkim/GitHub/CSV-to-FSA-script/CSV FOLDER/Allelic ladder - 10-14-16-5-21 PM.fsa'
    directory_sg = '/Users/kevkim/GitHub/CSV-to-FSA-script/CSV FOLDER/KevinTxtAllelicLadder.sg1'
    destination = '/Users/kevkim/GitHub/CSV-to-FSA-script/CSV FOLDER'
    name = 'Allelic ladder - 10-14-16-5-21 PM.fsa'

    # reader3 = ABIFReader(directory)
    # reader3.showEntries()

    SG1_reader = SG1_Reader(directory_sg)

    """
    Collect all data in list_of_data
    """
    list_of_data = []
    dict_of_data = {}
    for i in SG1_reader.entries:
        data = SG1_reader.getData(i.name, i.number)

        list_of_data.append(data)


    # data = [reader3.getData('DATA', 1), reader3.getData('DATA', 2), reader3.getData('DATA', 3),
    #         reader3.getData('DATA', 4), reader3.getData('DATA', 105)]
    # data2 = [reader3.getData('DATA', 5), reader3.getData('DATA', 6), reader3.getData('DATA', 7),
    #         reader3.getData('DATA', 8), reader3.getData('DyeN', 1)]
    print list_of_data

