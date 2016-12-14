"""
Learning more about struct and date time
hexadecimal
FSA/SG1 Files


"""
import struct
import itertools
import logging
from datetime import datetime


class SG1_Reader_simple:
    def __init__(self, fn):
        self.filename = fn
        self.file = open(fn, 'rb')
        self.type = self.readNextString(4)
        # self.file.seek(0)

    def readNextDate(self):
        a = self.readNextShort()
        b = self.readNextByte()
        c = self.readNextByte()
        d = datetime.date(a, b, c)
        return d

    def readNextShort(self):
        return self.primUnpack('>h', 2)

    def readNextByte(self):
        return self.primUnpack('B', 1)

    def readNextInt(self):
        return self.primUnpack('>i', 4)

    def primUnpack(self, format, nb):
        """

        :param format:
        :param nb: number of bytes
            'c'  1 - Char
            'B'  1 - Byte
            '>h' 2 - Short
            '>I' 4 - UnsignedInt
            '>i' 4 - Int
            '>l' 4 - Long
            '>f' 4 - Float
            '>d' 8 - Double

        :return:
        """
        x = struct.unpack(format, self.file.read(nb))
        return x[0]

"""Write"""
fn = '/Users/kevkim/GitHub/CSV-to-FSA-script/CSV FOLDER/playground2.sg1'
file = open(fn, 'wb')
date_data_offset = 132123420  # = 2016-11-28

# DATE offset
packed_DATE_data_offset = struct.pack('>i', date_data_offset)
file.write(packed_DATE_data_offset)

"""READ"""
SG1 = SG1_Reader_simple(fn)
x = SG1.readNextInt()

print "a"

# for date in range(1, 3):
#     logging.info("RUND" + str(date))
#     # Name
#     self.write_entry_name('R', 'U', 'N', 'D')
#     # Number (do a for loop and put i)
#     self.file.write(struct.pack('>i', date))
#     # Element Type (Always 10 for DATE)
#     self.file.write(struct.pack('>h', 10))
#     # Element Size (Always 4 for DATE)
#     self.file.write(struct.pack('>h', 4))
#     # Number of Elements (1 element for DATE)
#     self.file.write(struct.pack('>i', 1))
#     # Data Size = Element Size * Number of Elements
#     # for dye, the data size is 2
#     self.file.write(struct.pack('>i', 4))
#     # DATE offset
#     packed_DATE_data_offset = struct.pack('>i', date_data_offset)
#     self.file.write(packed_DATE_data_offset)
#     # Data handle = 0 ALWAYS (I Think)
#     packed_DATE_data_handle = struct.pack('>i', 0)
#     self.file.write(packed_DATE_data_handle)
