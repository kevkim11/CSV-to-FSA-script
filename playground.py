import csv
import sys
import os

from ABIFReader import *
from os.path import isdir, isfile, join

from struct import *

# a = pack('hhl', 1, 2, 3)
# print a
# b = unpack('hhl', '\x01\x00\x02\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00')
# print b

directory = '/Users/kevkim/GitHub/CSV-to-FSA-script/CSV FOLDER/Allelic ladder - 10-14-16-5-21 PM.fsa'
directory1 = '/Users/kevkim/GitHub/CSV-to-FSA-script/CSV FOLDER/KevinTxtAllelicLadder.sg1'


def primUnpack(format, file, nb):
    x = struct.unpack(format, file.read(nb))
    return x[0]

def readNextChar(file):
    return primUnpack('c', file, 1)

def read_next_string(file, size):
    chars = [readNextChar(file) for i in range(size)]
    return ''.join(chars)

with open(directory1, 'rb') as f:
    # type = read_next_string(f, 4)
    print "hi"
    # myArr = bytearray(f.read(10))
    # print myArr

    # print "hi"
