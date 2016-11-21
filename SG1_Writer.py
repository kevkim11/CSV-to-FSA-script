import struct
import datetime

from ABIFReader import *

from DirEntry import *



class SG1_Writer:
    """
    Class to create SG1 binary files using a list of list of 5 dyes.
    Has similar structure to that of an FSA file.
    """
    def __init__(self, fn):
        self.filename = fn
        self.file = open(fn, 'wb')
        # self.file.write('SG1F')  # self.type = self.readNextString(4)
        # s = struct.Struct('c')
        # values = ('S', 'G', '1', 'F')
        # packed_data = s.pack(*values)

        """Header"""
        packed_S = struct.pack('c', 'S')
        packed_G = struct.pack('c', 'G')
        packed_1 = struct.pack('c', '1')
        packed_F = struct.pack('c', 'F')
        l = [packed_S, packed_G, packed_1, packed_F]
        for i in l:
            self.file.write(i)

        """Version"""
        packed_101 = struct.pack('>h', 101)
        self.file.write(packed_101)

        """Directory Entry"""

        # Name
        packed_t = struct.pack('c', 't')
        packed_d = struct.pack('c', 'd')
        packed_i = struct.pack('c', 'i')
        packed_r = struct.pack('c', 'r')
        for i in [packed_t, packed_d, packed_i, packed_r]:
            self.file.write(i)

        # Number
        packed_tdir_num = struct.pack('>i', 1)
        self.file.write(packed_tdir_num)

        # Element Type
        packed_tdir_element_type = struct.pack('>h', 1023)
        self.file.write(packed_tdir_element_type)

        # Element Size
        packed_tdir_element_size = struct.pack('>h', 28)
        self.file.write(packed_tdir_element_size)

        # Number of Elements
        packed_tdir_num_elements = struct.pack('>i', 10)
        self.file.write(packed_tdir_num_elements)

        # Data Size = Element Size * Number of Elements
        packed_tdir_data_size = struct.pack('>i', 280)
        self.file.write(packed_tdir_data_size)

        # Data offset pos - Don't need to write this...

        # Data offset
        packed_tdir_data_offset = struct.pack('>i', 70438)
        self.file.write(packed_tdir_data_offset)

        # Data handle = 0
        packed_tdir_data_handle = struct.pack('>i', 0)
        self.file.write(packed_tdir_data_handle)

        # dir = DirEntryWriter(self)
        self.seek(struct.unpack('>i', packed_tdir_data_offset)[0])

        """Entries"""
        """TRAC/DATA"""

        for i in [1, 2, 3, 4, 105]:
            # Iterating through a list of numbers that corresponds with the number variable.

            # Name
            T = struct.pack('c', 'T')
            R = struct.pack('c', 'R')
            A = struct.pack('c', 'A')
            C = struct.pack('c', 'C')
            for i in [T, R, A, C]:
                self.file.write(i)

            # Number - Use i to fill number during iteration
            packed_TRAC_num = struct.pack('>i', i)
            self.file.write(packed_TRAC_num)

            # Element Type (Always 4 for DATA)
            packed_TRAC_element_type = struct.pack('>h', 4)
            self.file.write(packed_TRAC_element_type)

            # Element Size (Always 2 for DATA)
            packed_TRAC_element_size = struct.pack('>h', 2)
            self.file.write(packed_TRAC_element_size)

            # Number of Elements (7031 for this specific DATA)
            packed_TRAC_num_elements = struct.pack('>i', 7031)
            self.file.write(packed_TRAC_num_elements)

            #TODO - Start here next time
            # Data Size = Element Size * Number of Elements
            packed_TRAC_data_size = struct.pack('>i', 14062)
            self.file.write(packed_TRAC_data_size)

            # Data offset pos - Don't need to write this...

            # Data offset
            packed_TRAC_data_offset = struct.pack('>i', 128)
            self.file.write(packed_TRAC_data_offset)

            """ Need to actually put data now..."""

            # Data handle = 0 ALWAYS (I Think)
            packed_tdir_data_handle = struct.pack('>i', 0)
            self.file.write(packed_tdir_data_handle)
        #
        # # dir = DirEntryWriter(self)
        # self.seek(struct.unpack('>i', packed_tdir_data_offset)[0])

        # if self.type != 'SG1F':
        #     self.close()
        #     raise SystemExit("error: No SG1F file '%s'" % fn)
        # self.version = self.readNextShort()
        # dir = DirEntry(self)
        # self.seek(dir.dataoffset)
        # self.entries = [DirEntry(self) for i in range(dir.numelements)]

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