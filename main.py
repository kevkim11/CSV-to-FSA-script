import csv
import sys
import os

# import matplotlib.pyplot as plt

from ABIFReader import *
from SG1_Reader import SG1_Reader
from SG1_Writer import *
from os.path import isdir, isfile, join

import pandas as pd

def plot_dyes(list_list_dyes, list_of_baseline_x = [], list_of_baseline_y = [], scatter = False):
    """
    Takes a list of list of the five dyes and then plots each of them.
    Commenting out some of the lines if I don't want to plot them.

    :param list_list_dyes:
    :param list_of_baseline_x: optional list - list of x's to plot for the baseline to be subtracted
    :param list_of_baseline_y: optional list - list of y's to plot for the baseline to be subtracted
    :param scatter:
    :return:
    """
    fig = plt.figure()
    plot = fig.add_subplot(111)

    x_axis = [x for x in range(len(list_list_dyes[3]))]

    if scatter == True and len(list_of_baseline_x)!= 0:
        plot.scatter(list_of_baseline_x, list_of_baseline_y, c="red", label='Scatter')
    elif scatter == False and len(list_of_baseline_x)!= 0:
        plot.plot(list_of_baseline_x, list_of_baseline_y, c="red", label='Plot')
    plot.plot(x_axis, list_list_dyes[0], c="blue", label='Flu')
    plot.plot(x_axis, list_list_dyes[1], c="green", label='Joe')
    plot.plot(x_axis, list_list_dyes[2], c="orange", label='TMR')
    plot.plot(x_axis, list_list_dyes[3], c="red", label='CXR')
    plot.plot(x_axis, list_list_dyes[4], c="black", label='WEN')

    """
    Set the x and y coordinate labels
    """
    plot.set_xlabel('quarter Seconds')
    plot.set_ylabel('ADC-Counts')
    """
    delta click event function
    """
    # Keep track of x/y coordinates, part of the find_delta_onclick
    xcoords = []
    ycoords = []
    def find_delta_onclick(event):
        global ix, iy
        global coords
        ix, iy = event.xdata, event.ydata
        xcoords.append(ix)
        ycoords.append(iy)
        print 'x = %s, y = %s' % (ix, iy)
        if len(xcoords) % 2 == 0:
            delta_x = abs(xcoords[-1] - xcoords[-2])
            delta_y = abs(ycoords[-1] - ycoords[-2])
            print 'delta_x = %d, delta_y = %d' % (delta_x, delta_y)
        coords = [ix, iy]
        return coords
    # connect the onclick function to the to mouse press
    fig.canvas.mpl_connect('button_press_event', find_delta_onclick)
    """
    add a for each plot
    """
    legend = plt.legend(loc='upper left', fontsize='small')
    return plot

def main():
    """
    1) read_csv (just need to access the raw data somehow)
    2) Get the 5 dyes
    3) Write it as a FSA/SG1 binary file.
        SG1_Writer class does this.
    """
    df = pd.read_csv('/Users/kevkim/GitHub/CSV-to-FSA-script/CSV FOLDER/data_to_csv.csv', index_col=0)
    list_of_list = df.values.tolist()
    SG1_Writer('CSV FOLDER/output.sg1', list_of_list)


if __name__ == "__main__":
    main()
    # """
    # Variables
    # """
    # # Directory variables
    # directory = '/Users/kevkim/GitHub/CSV-to-FSA-script/CSV FOLDER/Allelic ladder - 10-14-16-5-21 PM.fsa'
    # directory_sg = '/Users/kevkim/GitHub/CSV-to-FSA-script/CSV FOLDER/KevinTxtAllelicLadder.sg1'
    # directory_sg_out = '/Users/kevkim/GitHub/CSV-to-FSA-script/CSV FOLDER/output.sg1'
    # destination = '/Users/kevkim/GitHub/CSV-to-FSA-script/CSV FOLDER'
    # name = 'Allelic ladder - 10-14-16-5-21 PM.fsa'
    #
    # sg1_1 = '/Users/kevkim/GitHub/CSV-to-FSA-script/CSV FOLDER/KevinTxtAllelicLadder.sg1'
    # sg1_2 = '/Users/kevkim/GitHub/CSV-to-FSA-script/CSV FOLDER/310_converted_10_14_matrix.txt.sg1'
    # sg1_3 = '/Users/kevkim/GitHub/CSV-to-FSA-script/CSV FOLDER/310_converted_11_9_Matrix_10mW.txt.sg1'
    #
    # # Dataframe/list_to_list variable
    # df = pd.read_csv('/Users/kevkim/GitHub/CSV-to-FSA-script/CSV FOLDER/data_to_csv.csv', index_col=0)
    # # Contains a list of list of the dye values.
    # list_of_list = df.values.tolist()
    #
    # #######################
    # """
    # Write
    # """
    #
    # SG1_Writer(directory_sg_out, list_of_list)
    # SG1_reader = SG1_Reader(directory_sg_out)
    # a = SG1_reader.storeEntries()
    # Dye1 = SG1_reader.getData('Dye#', 1)
    # DATE1 = SG1_reader.getData('RUND', 1)
    # TIME1 = SG1_reader.getData('RUNT', 1)
    # print "a"
    # data1 = [SG1_reader.getData('TRAC', 1), SG1_reader.getData('TRAC', 2), SG1_reader.getData('TRAC', 3),
    #         SG1_reader.getData('TRAC', 4), SG1_reader.getData('TRAC', 105)]
    # """
    # Read
    # """
    # # SG1_1_reader = SG1_Reader(sg1_1)
    # # SG1_2_reader = SG1_Reader(sg1_2)
    # # SG1_3_reader = SG1_Reader(sg1_3)
    # # a = SG1_1_reader.storeEntries()
    # # b = SG1_2_reader.storeEntries()
    # # c = SG1_3_reader.storeEntries()
    # # print "a"
    # # # SG1_reader.showEntries()
    # # #
    # # # SG1_reader.storeEntries()
    # #
    # #
    # # data1 = [SG1_1_reader.getData('TRAC', 1), SG1_1_reader.getData('TRAC', 2), SG1_1_reader.getData('TRAC', 3),
    # #         SG1_1_reader.getData('TRAC', 4), SG1_1_reader.getData('TRAC', 105)]
    # # data2 = [SG1_2_reader.getData('TRAC', 1), SG1_2_reader.getData('TRAC', 2), SG1_2_reader.getData('TRAC', 3),
    # #         SG1_2_reader.getData('TRAC', 4), SG1_2_reader.getData('TRAC', 105)]
    # # data3 = [SG1_3_reader.getData('TRAC', 1), SG1_3_reader.getData('TRAC', 2), SG1_3_reader.getData('TRAC', 3),
    # #         SG1_3_reader.getData('TRAC', 4), SG1_3_reader.getData('TRAC', 105)]
    # # # one = SG1_reader.getData('TRAC', 1)
    # # # two = SG1_reader.getData('TRAC', 2)
    # # # Dye_num = SG1_reader.getData('Dye#', 1)
    # # DATE1 = SG1_1_reader.getData('RUND', 1)
    # # DATE2 = SG1_3_reader.getData('RUND', 1)
    # # TIME1 = SG1_1_reader.getData('RUNT', 1)
    # # TIME2 = SG1_3_reader.getData('RUNT', 1)
    # print "a"
    # # a = pd.DataFrame(data)
    # # a.to_csv('/Users/kevkim/GitHub/CSV-to-FSA-script/CSV FOLDER/data_to_csv.csv')
    # # for i in data:
    # #     print i
    #
    # print "a"
    # #
    # # plot_dyes(data)
    # # plt.show()
    #
    # # with open(directory_sg_out, 'rb') as f:
    # #     a = f.read(4)
    # #     print a
    #
    #     # myArr = bytearray(f.read(4))
