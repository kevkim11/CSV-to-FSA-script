# Author: Kevin Kim
# Version: 1.0.1, November 2016

import struct
import datetime

from ABIFReader import *

import pandas as pd

from DirEntry import *

import itertools



class SG1_Writer:
    """
    Class to create SG1 binary files using a list of list of 5 dyes.
    Has similar structure to that of an FSA file.
    """
    def write_header(self):
        # Always constant
        packed_S = struct.pack('c', 'S') # 0
        packed_G = struct.pack('c', 'G') # 1
        packed_1 = struct.pack('c', '1') # 2
        packed_F = struct.pack('c', 'F') # 3
        l = [packed_S, packed_G, packed_1, packed_F]
        for i in l:
            self.file.write(i)

    def write_version(self):
        # Always constant.
        packed_101 = struct.pack('>h', 101) # 4, 5 (2 bytes)
        self.file.write(packed_101)

    def __init__(self, fn, list_of_list = None):

        """"""
        """Variables"""
        self.filename = fn
        self.file = open(fn, 'wb')

        GLOBAL_DATA_OFFSET = 327400
        data_data_offset = 128

        """Header"""
        # 0-3 (4 bytes)
        self.write_header()

        """Version"""
         # 4, 5 (2 bytes)
        self.write_version()

        """Directory Entry"""
        # Name
        packed_t = struct.pack('c', 't') # 6
        packed_d = struct.pack('c', 'd') # 7
        packed_i = struct.pack('c', 'i') # 8
        packed_r = struct.pack('c', 'r') # 9
        for i in [packed_t, packed_d, packed_i, packed_r]:
            self.file.write(i)
        # Number
        self.file.write(struct.pack('>i', 1))  # 10 - 13 (int = 4 bytes)
        # Element Type
        self.file.write(struct.pack('>h', 1023)) # 14, 15 (short = 2 bytes)
        # Element Size
        self.file.write(struct.pack('>h', 28)) # 16, 17 (short = 2 bytes)
        # Number of Elements
        self.file.write(struct.pack('>i', 10)) # # 18 - 21 (int = 4 bytes)
        # Data Size = Element Size * Number of Elements
        self.file.write(struct.pack('>i', 280)) # 22 - 25
        # Data offset pos - Don't need to write this...
        # Data offset
        self.file.write(struct.pack('>i', GLOBAL_DATA_OFFSET)) # 26 - 29 (int = 4 bytes)
        # Data handle = 0 always
        self.file.write(struct.pack('>i', 0)) # 30 - 33
        # DirEntry Unused space (pg 10)
        # 34 - 128
        for it in range(47):
            self.file.write(struct.pack('>h', 0))
        # dir = DirEntryWriter(self)
        self.seek(GLOBAL_DATA_OFFSET)
        """Entries"""

        """TRAC/DATA (0-4 entries)"""
        # value for the offset position in which the data is stored.
        for TRAC_number, dye in itertools.izip([1, 2, 3, 4, 105], list_of_list):
            # Iterating through a list of numbers that corresponds with the number variable.
            global_data_offset_counter = 0
            dataoffsetpos0 = self.tell()
            # Name
            T = struct.pack('c', 'T')
            R = struct.pack('c', 'R')
            A = struct.pack('c', 'A')
            C = struct.pack('c', 'C')
            for letters in [T, R, A, C]:
                self.file.write(letters)
            global_data_offset_counter += 4
            # Number - int = 4 bytes
            self.file.write(struct.pack('>i', TRAC_number))
            global_data_offset_counter += 4
            # Element Type (Always 4 for DATA) short = 2 bytes
            self.file.write(struct.pack('>h', 4))
            global_data_offset_counter += 2
            # Element Size (Always 2 for DATA)
            self.file.write(struct.pack('>h', 2))
            global_data_offset_counter += 2
            # Number of Elements (7031 for this specific DATA)
            number_of_elements = len(dye)
            self.file.write(struct.pack('>i', number_of_elements))
            global_data_offset_counter += 4
            # Data Size = 2 (Element Size) * Number of Elements
            data_size = number_of_elements * 2
            self.file.write(struct.pack('>i', data_size))
            global_data_offset_counter += 4
            # Data offset pos - Don't need to write this...
            self.file.write(struct.pack('>i', data_data_offset))
            global_data_offset_counter += 4
            # Data handle = 0 ALWAYS (I Think)
            self.file.write(struct.pack('>i', 0))
            global_data_offset_counter += 4
            """ Need to actually put data now..."""
            GLOBAL_DATA_OFFSET += global_data_offset_counter # += 28
            self.seek(data_data_offset)
            for value in dye:
                self.file.write(struct.pack('>h', value))
            data_data_offset += data_size
            self.seek(GLOBAL_DATA_OFFSET)

        """Dye# (entry 5)"""
        dye_data_offset_counter = 0
        DYE_data_offset = 327680
        # Name
        D = struct.pack('c', 'D')
        Y = struct.pack('c', 'y')
        E = struct.pack('c', 'e')
        num = struct.pack('c', '#')
        for i in [D, Y, E, num]:
            self.file.write(i)
        # Number
        self.file.write(struct.pack('>i', 1))
        # Element Type (Always 4 for DATA)
        self.file.write(struct.pack('>h', 4))
        # Element Size (Always 2 for DATA)
        self.file.write(struct.pack('>h', 2))
        # Number of Elements (1 element for DYE)
        self.file.write(struct.pack('>i', 1))
        # Data Size = Element Size * Number of Elements
        # for dye, the data size is 2
        self.file.write(struct.pack('>i', 2))
        # Data offset pos - Don't need to write this...
        self.file.write(struct.pack('>i', DYE_data_offset))
        # Data handle = 0 ALWAYS (I Think)
        self.file.write(struct.pack('>i', 0))
        """ Need to actually put data now..."""
        GLOBAL_DATA_OFFSET += 28
        # Go To where the data is supposed to be stored
        self.seek(DYE_data_offset)
        self.file.write(struct.pack('>h', 5))
        self.seek(GLOBAL_DATA_OFFSET)

        """RUND / date (entry 6 and 7)"""
        # DATE_dataoffsetpos = 70626
        for date in range(2):
            dataoffsetpos9 = self.tell()
            # Name
            RR = struct.pack('c', 'R')
            UU = struct.pack('c', 'U')
            NN = struct.pack('c', 'N')
            DD = struct.pack('c', 'D')
            for i in [RR, UU, NN, DD]:
                self.file.write(i)
            # Number (do a for loop and put i)
            self.file.write(struct.pack('>i', date+1))
            # Element Type (Always 10 for DATE)
            self.file.write(struct.pack('>h', 10))
            # Element Size (Always 4 for DATE)
            self.file.write(struct.pack('>h', 4))
            # Number of Elements (1 element for DATE)
            self.file.write(struct.pack('>i', 1))
            # Data Size = Element Size * Number of Elements
            # for dye, the data size is 2
            self.file.write(struct.pack('>i', 4))
            # DATE offset
            dataoffsetpos24 = self.tell()
            DATE_data_offset = 132123409
            packed_DATE_data_offset = struct.pack('>i', DATE_data_offset)
            self.file.write(packed_DATE_data_offset)
            # Data handle = 0 ALWAYS (I Think)
            packed_DATE_data_handle = struct.pack('>i', 0)
            self.file.write(packed_DATE_data_handle)
            """ Need to actually put data now..."""
            GLOBAL_DATA_OFFSET += 28
            # Go To where the data is supposed to be stored
            self.seek(DATE_data_offset)
            # Add 5 because there's a total of 5 dyes
            year = struct.pack('>h', 2016)
            self.file.write(year)
            month = struct.pack('B', 11)
            self.file.write(month)
            day = struct.pack('B', 17)
            self.file.write(day)
            self.seek(GLOBAL_DATA_OFFSET)

        """RUNT / time (entry 8 and 9)"""
        for time in range(2):
            # Name
            RRR = struct.pack('c', 'R')
            UUU = struct.pack('c', 'U')
            NNN = struct.pack('c', 'N')
            TTT = struct.pack('c', 'T')
            for l in [RRR, UUU, NNN, TTT]:
                self.file.write(l)
            # Number
            self.file.write(struct.pack('>i', time+1))
            # Element Type (Always 10 for time)
            self.file.write(struct.pack('>h', 11))
            # Element Size (Always 4 for time)
            self.file.write(struct.pack('>h', 4))
            # Number of Elements (1 element for DATE)
            self.file.write(struct.pack('>i', 1))
            # Data Size = Element Size * Number of Elements
            # for dye, the data size is 2
            self.file.write(struct.pack('>i', 4))
            # DATE offset
            TIME_data_offset = 201326592
            self.file.write(struct.pack('>i', TIME_data_offset))
            # Data handle = 0 ALWAYS (I Think)
            self.file.write(struct.pack('>i', 0))
            """ Need to actually put data now..."""
            GLOBAL_DATA_OFFSET += 28
            # Go To where the data is supposed to be stored
            self.seek(TIME_data_offset)
            # Add time
            hour = struct.pack('B', 12)
            self.file.write(hour)
            minute = struct.pack('B', 0)
            self.file.write(minute)
            seconds = struct.pack('B', 0)
            self.file.write(seconds)
            microseconds = struct.pack('B', 0)
            self.file.write(microseconds)
            self.seek(GLOBAL_DATA_OFFSET)
            dataoffsetpos32 = self.tell()


    def store_data(self):
        pass

    def writeNextChar(self):
        return self.primPack('c', 1)

    def writeNextString(self, size):
        pass

    def writeNextShort(self):
        return self.primPack('>h', 2)

    def primPack(self, format, values):

        """

        :param format:
        :param nb: number of bytes
        :return:
        """
        s = struct.Struct(format)
        packed_data = s.pack(*values)
        # x = struct.pack(format, self.file.read(nb))
        self.file.write(packed_data)
        return packed_data

    # Properly close the files.
    def close(self):
        self.file.close()

    def seek(self, pos):
        self.file.seek(pos)

    def tell(self):
        return self.file.tell()

    def mydataoffset(self):
        if self.datasize <= 4:
            return self.dataoffsetpos
        else:
            return self.dataoffset