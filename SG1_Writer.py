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
        self.filename = fn
        self.file = open(fn, 'wb')

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
        packed_tdir_num = struct.pack('>i', 1) # 10 - 13 (int = 4 bytes)
        self.file.write(packed_tdir_num)

        # Element Type
        packed_tdir_element_type = struct.pack('>h', 1023) # 14, 15 (short = 2 bytes)
        self.file.write(packed_tdir_element_type)

        # Element Size
        packed_tdir_element_size = struct.pack('>h', 28) # 16, 17 (short = 2 bytes)
        self.file.write(packed_tdir_element_size)

        # Number of Elements
        packed_tdir_num_elements = struct.pack('>i', 10) # 18 - 21 (int = 4 bytes)
        self.file.write(packed_tdir_num_elements)

        # Data Size = Element Size * Number of Elements
        packed_tdir_data_size = struct.pack('>i', 280) # 22 - 25
        self.file.write(packed_tdir_data_size)

        # Data offset pos - Don't need to write this...

        # Data offset
        global_data_offset = 70438
        packed_tdir_data_offset = struct.pack('>i', global_data_offset) # 26 - 29 (int = 4 bytes)
        self.file.write(packed_tdir_data_offset)

        # Data handle = 0

        packed_tdir_data_handle = struct.pack('>i', 0) #30 - 33
        self.file.write(packed_tdir_data_handle)

        # DirEntry Unused space (pg 10)
        # 34 - 128
        for it in range(47):
            packed_unused_2_bytes = struct.pack('>h', 0)
            self.file.write(packed_unused_2_bytes)


        # dir = DirEntryWriter(self)
        self.seek(struct.unpack('>i', packed_tdir_data_offset)[0])

        """Entries"""

        """TRAC/DATA (0-4 entries)"""
        df = pd.read_csv('/Users/kevkim/GitHub/CSV-to-FSA-script/CSV FOLDER/data_to_csv.csv', index_col=0)
        # Contains a list of list of the dye values.
        list_of_list = df.values.tolist()
        # value for the offset position in which the data is stored.
        data_data_offset = 128

        for a, dye in itertools.izip([1, 2, 3, 4, 105], list_of_list):
            # Iterating through a list of numbers that corresponds with the number variable.

            # dataoffsetpos0 = self.tell()

            # Name
            T = struct.pack('c', 'T')
            R = struct.pack('c', 'R')
            A = struct.pack('c', 'A')
            C = struct.pack('c', 'C')
            for letters in [T, R, A, C]:
                self.file.write(letters)

            # Number - Use i to fill number during iteration
            packed_TRAC_num = struct.pack('>i', a)
            self.file.write(packed_TRAC_num)

            # Element Type (Always 4 for DATA)
            packed_TRAC_element_type = struct.pack('>h', 4)
            self.file.write(packed_TRAC_element_type)

            # dataoffsetpos1 = self.tell()

            # Element Size (Always 2 for DATA)
            packed_TRAC_element_size = struct.pack('>h', 2)
            self.file.write(packed_TRAC_element_size)

            # dataoffsetpos2 = self.tell()

            # Number of Elements (7031 for this specific DATA)
            number_of_elements = 7031
            packed_TRAC_num_elements = struct.pack('>i', number_of_elements)
            self.file.write(packed_TRAC_num_elements)

            # Data Size = Element Size * Number of Elements
            # For this data set, all the values are 14062
            data_size = 14062
            packed_TRAC_data_size = struct.pack('>i', data_size)
            self.file.write(packed_TRAC_data_size)

            # Data offset pos - Don't need to write this...
            dataoffsetpos3 = self.tell()

            # Data offset (need to increment by 14062)
            packed_TRAC_data_offset = struct.pack('>i', data_data_offset)
            self.file.write(packed_TRAC_data_offset)

            # Data handle = 0 ALWAYS (I Think)
            packed_TRAC_data_handle = struct.pack('>i', 0)
            self.file.write(packed_TRAC_data_handle)

            """ Need to actually put data now..."""

            # dataoffsetpos4 = str(self.tell())
            global_data_offset+=28

            self.seek(data_data_offset)
            data_data_offset += data_size

            # dataoffsetpos5 = self.tell()

            # 2) Iterate over those data and store them into file a byte at a time
            for value in dye:
                packed_TRAC_data_data = struct.pack('>h', value)
                self.file.write(packed_TRAC_data_data)

            self.seek(global_data_offset)

            dataoffsetpos6 = self.tell()
            print "b"

        """Dye# (entry 5)"""
        dye_data_offset = 327680
        dataoffsetpos7 = self.tell()
        # Name
        D = struct.pack('c', 'D')
        Y = struct.pack('c', 'y')
        E = struct.pack('c', 'e')
        num = struct.pack('c', '#')
        for i in [D, Y, E, num]:
            self.file.write(i)

        # Number
        packed_DYE_num = struct.pack('>i', 1)
        self.file.write(packed_DYE_num)

        # Element Type (Always 4 for DATA)
        packed_DYE_element_type = struct.pack('>h', 4)
        self.file.write(packed_DYE_element_type)

        # Element Size (Always 2 for DATA)
        packed_DYE_element_size = struct.pack('>h', 2)
        self.file.write(packed_DYE_element_size)

        # Number of Elements (1 element for DYE)
        packed_DYE_num_elements = struct.pack('>i', 1)
        self.file.write(packed_DYE_num_elements)

        # Data Size = Element Size * Number of Elements
        # for dye, the data size is 2
        packed_DYE_data_size = struct.pack('>i', 2)
        self.file.write(packed_DYE_data_size)

        # Data offset pos - Don't need to write this...
        dataoffsetpos8 = self.tell()

        # Data offset
        DYE_data_offset = 327680
        packed_DYE_data_offset = struct.pack('>i', DYE_data_offset)
        self.file.write(packed_DYE_data_offset)

        # Data handle = 0 ALWAYS (I Think)
        packed_DYE_data_handle = struct.pack('>i', 0)
        self.file.write(packed_DYE_data_handle)

        dataoffsetpos14 = self.tell()

        """ Need to actually put data now..."""

        # dataoffsetpos4 = str(self.tell())
        global_data_offset += 28

        # Go To where the data is supposed to be stored
        self.seek(DYE_data_offset)
        # data_data_offset += packed_DYE_data_size

        dataoffsetpos11 = self.tell()

        # Add 5 because there's a total of 5 dyes
        packed_DYE_data_data = struct.pack('>h', 5)
        self.file.write(packed_DYE_data_data)

        self.seek(global_data_offset)

        dataoffsetpos12 = self.tell()

        print "a"
        # global_data_offset += 28

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
            packed_DATE_num = struct.pack('>i', date+1)
            self.file.write(packed_DATE_num)

            # Element Type (Always 10 for DATE)
            packed_DATE_element_type = struct.pack('>h', 10)
            self.file.write(packed_DATE_element_type)

            # Element Size (Always 4 for DATE)
            packed_DATE_element_size = struct.pack('>h', 4)
            self.file.write(packed_DATE_element_size)

            # Number of Elements (1 element for DATE)
            packed_DATE_num_elements = struct.pack('>i', 1)
            self.file.write(packed_DATE_num_elements)

            # Data Size = Element Size * Number of Elements
            # for dye, the data size is 2
            packed_DATE_data_size = struct.pack('>i', 4)
            self.file.write(packed_DATE_data_size)

            # DATE offset
            dataoffsetpos24 = self.tell()
            DATE_data_offset = 132123409
            packed_DATE_data_offset = struct.pack('>i', DATE_data_offset)
            self.file.write(packed_DATE_data_offset)

            # Data handle = 0 ALWAYS (I Think)
            packed_DATE_data_handle = struct.pack('>i', 0)
            self.file.write(packed_DATE_data_handle)

            """ Need to actually put data now..."""

            # dataoffsetpos4 = str(self.tell())
            global_data_offset += 28

            # Go To where the data is supposed to be stored
            self.seek(DATE_data_offset)
            # data_data_offset += packed_DYE_data_size

            dataoffsetpos21 = self.tell()

            # Add 5 because there's a total of 5 dyes
            year = struct.pack('>h', 2016)
            self.file.write(year)
            month = struct.pack('B', 11)
            self.file.write(month)
            day = struct.pack('B', 17)
            self.file.write(day)

            self.seek(global_data_offset)

            dataoffsetpos22 = self.tell()

        """RUNT / time (entry 8 and 9)"""

        for time in range(2):
            dataoffsetpos9 = self.tell()

            # Name
            RRR = struct.pack('c', 'R')
            UUU = struct.pack('c', 'U')
            NNN = struct.pack('c', 'N')
            TTT = struct.pack('c', 'T')
            for l in [RRR, UUU, NNN, TTT]:
                self.file.write(l)

            # Number
            packed_TIME_num = struct.pack('>i', time+1)
            self.file.write(packed_TIME_num)

            # Element Type (Always 10 for time)
            packed_TIME_element_type = struct.pack('>h', 11)
            self.file.write(packed_TIME_element_type)

            # Element Size (Always 4 for time)
            packed_TIME_element_size = struct.pack('>h', 4)
            self.file.write(packed_TIME_element_size)

            # Number of Elements (1 element for DATE)
            packed_TIME_num_elements = struct.pack('>i', 1)
            self.file.write(packed_TIME_num_elements)

            # Data Size = Element Size * Number of Elements
            # for dye, the data size is 2
            packed_TIME_data_size = struct.pack('>i', 4)
            self.file.write(packed_TIME_data_size)

            # DATE offset
            dataoffsetpos34 = self.tell()
            TIME_data_offset = 201326592
            packed_TIME_data_offset = struct.pack('>i', TIME_data_offset)
            self.file.write(packed_TIME_data_offset)

            # Data handle = 0 ALWAYS (I Think)
            packed_TIME_data_handle = struct.pack('>i', 0)
            self.file.write(packed_TIME_data_handle)

            """ Need to actually put data now..."""

            # dataoffsetpos4 = str(self.tell())
            global_data_offset += 28

            # Go To where the data is supposed to be stored
            self.seek(TIME_data_offset)
            # data_data_offset += packed_DYE_data_size

            dataoffsetpos31 = self.tell()

            # Add time
            hour = struct.pack('B', 12)
            self.file.write(hour)
            minute = struct.pack('B', 0)
            self.file.write(minute)
            seconds = struct.pack('B', 0)
            self.file.write(seconds)
            microseconds = struct.pack('B', 0)
            self.file.write(microseconds)

            self.seek(global_data_offset)

            dataoffsetpos32 = self.tell()

            print "Almost done"


    def store_data(self):
        pass

    def write_header(self):
        packed_S = struct.pack('c', 'S')
        packed_G = struct.pack('c', 'G')
        packed_1 = struct.pack('c', '1')
        packed_F = struct.pack('c', 'F')
        l = [packed_S, packed_G, packed_1, packed_F]
        for i in l:
            self.file.write(i)

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