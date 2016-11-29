# Author: Kevin Kim
# Version: 1.0.1, November 2016

import struct
import itertools

import logging

class SG1_Writer:
    """
    Class to create SG1 binary files using a list of list of 5 dyes.
    Has similar structure to that of an FSA file.
    """
    def write_header_type(self):
        logging.info('Started header')
        packed_S = struct.pack('c', 'S') # 0
        packed_G = struct.pack('c', 'G') # 1
        packed_1 = struct.pack('c', '1') # 2
        packed_F = struct.pack('c', 'F') # 3
        l = [packed_S, packed_G, packed_1, packed_F]
        for i in l:
            self.file.write(i)
        logging.info('Finished header')

    def write_entry_name(self, a, b, c, d):
        logging.info('write_entry_name started for %s', ''.join([a, b, c, d]))
        packed_1_char = struct.pack('c', a)
        packed_2_char = struct.pack('c', b)
        packed_3_char = struct.pack('c', c)
        packed_4_char = struct.pack('c', d)
        for packed_char in [packed_1_char, packed_2_char, packed_3_char, packed_4_char]:
            self.file.write(packed_char)

    def __init__(self, fn, list_of_list):
        """

        :param fn: string - filename and directory
        :param list_of_list: - list of list containing the values for joe, flu, tmr, cxr, and wen.
        """

        """Variables"""
        self.filename = fn
        self.file = open(fn, 'wb')

        """Header"""
        self.write_header_type() # 0-3 (4 bytes)
        """Version"""
        self.file.write(struct.pack('>h', 101))  # 4, 5 (2 bytes)

        """Directory Entry"""
        entry_data_offset = 327400
        # Name
        self.write_entry_name('t', 'd', 'i', 'r')
        # Number
        self.file.write(struct.pack('>i', 1))  # 10 - 13 (int = 4 bytes)
        # Element Type
        self.file.write(struct.pack('>h', 1023)) # 14, 15 (short = 2 bytes)
        # Element Size
        self.file.write(struct.pack('>h', 28)) # 16, 17 (short = 2 bytes)
        # Number of Elements
        self.file.write(struct.pack('>i', 10)) # # 18 - 21 (int = 4 bytes)
        # Data Size = Element Size * Number of Elements
        # For sg1 file, will always be 28*10=280
        self.file.write(struct.pack('>i', 280)) # 22 - 25
        # Data offset
        self.file.write(struct.pack('>i', entry_data_offset)) # 26 - 29 (int = 4 bytes)
        # Data handle = 0 always
        self.file.write(struct.pack('>i', 0)) # 30 - 33
        # DirEntry Unused space (pg 10) # 34 - 128
        for it in range(47):
            self.file.write(struct.pack('>h', 0))

        """Entries"""
        self.seek(entry_data_offset)
        """TRAC/DATA (0-4 entries)"""
        data_data_offset = 128
        for TRAC_number, dye in itertools.izip([1, 2, 3, 4, 105], list_of_list):
            # Iterating through a list of numbers that corresponds with the number variable.
            # Name
            self.write_entry_name('T', 'R', 'A', 'C')
            # Number - int = 4 bytes
            self.file.write(struct.pack('>i', TRAC_number))
            # Element Type (Always 4 for DATA) short = 2 bytes
            self.file.write(struct.pack('>h', 4))
            # Element Size (Always 2 for DATA)
            self.file.write(struct.pack('>h', 2))
            # Number of Elements (7031 for this specific DATA)
            number_of_elements = len(dye)
            self.file.write(struct.pack('>i', number_of_elements))
            # Data Size = 2 (Element Size) * Number of Elements
            data_size = 2 * number_of_elements
            self.file.write(struct.pack('>i', data_size))
            # Data offset pos - Don't need to write this...
            self.file.write(struct.pack('>i', data_data_offset))
            # Data handle = 0 ALWAYS (I Think)
            self.file.write(struct.pack('>i', 0))
            """ STORE DATA """
            entry_data_offset += 28
            self.seek(data_data_offset)
            for value in dye:
                self.file.write(struct.pack('>h', value))
            data_data_offset += data_size
            self.seek(entry_data_offset)

        """Dye# (entry 5)"""
        dye_data_offset = 327680
        # Name
        self.write_entry_name('D', 'y', 'e', '#')
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
        self.file.write(struct.pack('>i', dye_data_offset))
        # Data handle = 0 ALWAYS (I Think)
        self.file.write(struct.pack('>i', 0))
        """ STORE DATA """
        entry_data_offset += 28
        # Go To where the data is supposed to be stored
        self.seek(dye_data_offset)
        self.file.write(struct.pack('>h', 5))
        self.seek(entry_data_offset)

        """RUND / date (entry 6 and 7)"""
        # DATE_dataoffsetpos = 70626
        date_data_offset = 132123409
        for date in range(2):
            dataoffsetpos9 = self.tell()
            # Name
            self.write_entry_name('R', 'U', 'N', 'D')
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
            packed_DATE_data_offset = struct.pack('>i', date_data_offset)
            self.file.write(packed_DATE_data_offset)
            # Data handle = 0 ALWAYS (I Think)
            packed_DATE_data_handle = struct.pack('>i', 0)
            self.file.write(packed_DATE_data_handle)
            """ STORE DATA """
            entry_data_offset += 28
            # Go To where the data is supposed to be stored
            self.seek(date_data_offset)
            year = struct.pack('>h', 2016)
            self.file.write(year)
            month = struct.pack('B', 11)
            self.file.write(month)
            day = struct.pack('B', 17)
            self.file.write(day)
            self.seek(entry_data_offset)

        """RUNT / time (entry 8 and 9)"""
        TIME_data_offset = 201326592
        for time in range(2):
            # Name
            self.write_entry_name('R', 'U', 'N', 'T')
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
            self.file.write(struct.pack('>i', TIME_data_offset))
            # Data handle = 0 ALWAYS (I Think)
            self.file.write(struct.pack('>i', 0))
            """ STORE DATA """
            entry_data_offset += 28
            self.seek(TIME_data_offset)
            hour = struct.pack('B', 12)
            self.file.write(hour)
            minute = struct.pack('B', 0)
            self.file.write(minute)
            seconds = struct.pack('B', 0)
            self.file.write(seconds)
            microseconds = struct.pack('B', 0)
            self.file.write(microseconds)
            self.seek(entry_data_offset)

    # Properly close the files.
    def close(self):
        self.file.close()

    def seek(self, pos):
        self.file.seek(pos)

    def tell(self):
        return self.file.tell()