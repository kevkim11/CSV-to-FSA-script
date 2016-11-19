import csv
import sys
import os

import matplotlib.pyplot as plt

from ABIFReader import *
from SG1_Reader import *
from SG1_Writer import *
from os.path import isdir, isfile, join

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

if __name__ == "__main__":
    directory = '/Users/kevkim/GitHub/CSV-to-FSA-script/CSV FOLDER/Allelic ladder - 10-14-16-5-21 PM.fsa'
    directory_sg = '/Users/kevkim/GitHub/CSV-to-FSA-script/CSV FOLDER/KevinTxtAllelicLadder.sg1'
    directory_sg_out = '/Users/kevkim/GitHub/CSV-to-FSA-script/CSV FOLDER/output.sg1'
    destination = '/Users/kevkim/GitHub/CSV-to-FSA-script/CSV FOLDER'
    name = 'Allelic ladder - 10-14-16-5-21 PM.fsa'

    # reader3 = ABIFReader(directory)
    # reader3.showEntries()


    #
    # """
    # Collect all data in list_of_data
    # """
    # list_of_data = []
    # dict_of_data = {}
    # for i in SG1_reader.entries:
    #     data = SG1_reader.getData(i.name, i.number)
    #
    #     list_of_data.append(data)
    #
    #
    # # data = [reader3.getData('DATA', 1), reader3.getData('DATA', 2), reader3.getData('DATA', 3),
    # #         reader3.getData('DATA', 4), reader3.getData('DATA', 105)]
    # # data2 = [reader3.getData('DATA', 5), reader3.getData('DATA', 6), reader3.getData('DATA', 7),
    # #         reader3.getData('DATA', 8), reader3.getData('DyeN', 1)]
    # print list_of_data



    #######################
    """
    Write
    """

    # SG1_Writer(directory_sg_out)

    """
    Read
    """
    SG1_reader = SG1_Reader(directory_sg)
    print "a"

    # data = [SG1_reader.getData('TRAC', 1), SG1_reader.getData('TRAC', 2), SG1_reader.getData('TRAC', 3),
    #         SG1_reader.getData('TRAC', 4), SG1_reader.getData('TRAC', 105)]
    #
    # plot_dyes(data)
    # plt.show()

    # with open(directory_sg_out, 'rb') as f:
    #     a = f.read(4)
    #     print a

        # myArr = bytearray(f.read(4))
