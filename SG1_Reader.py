
import struct
import datetime

from ABIFReader import *

from DirEntry import *

import pandas as pd

class SG1_Reader:
    """
    Class to read SG1 binary files.
    Has similar structure to that of an FSA file.
    """
    def __init__(self, fn):
        # type: (object) -> object
        self.filename = fn
        self.file = open(fn, 'rb')
        self.type = self.readNextString(4)
        if self.type != 'SG1F':
            self.close()
            raise SystemExit("error: No SG1F file '%s'" % fn)
        self.version = self.readNextShort()
        dir = DirEntry(self)
        self.seek(dir.dataoffset)
        # self.entries = [DirEntry(self) for i in range(dir.numelements)]
        self.entries = []
        for i in range(dir.numelements):
            self.entries.append(DirEntry(self))

    def getData(self, name, num=1):
        entry = self.getEntry(name, num)
        if not entry:
            raise SystemExit("error: Entry '%s (%i)' not found in '%s'" % (name, num, self.filename))
        self.seek(entry.mydataoffset()) # self.dataoffset
        data = self.readData(entry.elementtype, entry.numelements)
        if data != NotImplemented and len(data) == 1:
            return data[0]
        else:
            return data

    def showEntries(self):
        for e in self.entries:
            print e


    def storeEntries(self):
        """
        Custom method I made in order to better visualize the entries data.
        :return:
        """
        dict = {
            "name": [],
            "number": [],
            "elementtype": [],
            "elementsize": [],
            "numelements": [],
            "data size": [],
            "dataoffsetpos": [],
            "data offset": [],
            "data handle": []
        }
        for e in self.entries:
            dict["name"].append(e.name)
            dict["number"].append(e.number)
            dict["elementtype"].append(e.elementtype)
            dict["elementsize"].append(e.elementsize)
            dict["numelements"].append(e.numelements)
            dict["data size"].append(e.datasize)
            dict["dataoffsetpos"].append(e.dataoffsetpos)
            dict["data offset"].append(e.dataoffset)
            dict["data handle"].append(e.datahandle)

        df = pd.DataFrame(dict)
        return df

    def getEntry(self, name, num):
        for e in self.entries:
            if e.name == name and e.number == num:
                return e
        return None

    def readData(self, type, numelements):
        if type == 1:
            return [self.readNextByte() for i in range(numelements)]
        elif type == 2:
            return self.readNextString(numelements)
        elif type == 3:
            return [self.readNextUnsignedInt() for i in range(numelements)]
        elif type == 4:
            return [self.readNextShort() for i in range(numelements)]
        elif type == 5:
            return [self.readNextLong() for i in range(numelements)]
        elif type == 7:
            return [self.readNextFloat() for i in range(numelements)]
        elif type == 8:
            return [self.readNextDouble() for i in range(numelements)]
        elif type == 10:
            return [self.readNextDate() for i in range(numelements)]
        elif type == 11:
            return [self.readNextTime() for i in range(numelements)]
        elif type == 12:
            return [self.readNextThumb() for i in range(numelements)]
        elif type == 13:
            return [self.readNextBool() for i in range(numelements)]
        elif type == 18:
            return self.readNextpString()
        elif type == 19:
            return self.readNextcString()
        elif type >= 1024:
            return self.readNextUserData(type, numelements)
        else:
            return NotImplemented

    def readNextBool(self):
        return readNextByte(self) == 1

    def readNextByte(self):
        return self.primUnpack('B', 1)

    def readNextChar(self):
        return self.primUnpack('c', 1)

    def readNextcString(self):
        chars = []
        while True:
            c = self.readNextChar()
            if ord(c) == 0:
                return ''.join(chars)
            else:
                chars.append(c)

    def readNextDate(self):
        a = self.readNextShort()
        b = self.readNextByte()
        c = self.readNextByte()
        d = datetime.date(a, b, c)
        return d

    def readNextTime(self):
        a = self.readNextByte()
        b = self.readNextByte()
        c = self.readNextByte()
        d = self.readNextByte()
        e = datetime.time(a, b, c, d)
        return e

    def readNextDouble(self):
        return self.primUnpack('>d', 8)

    def readNextInt(self):
        return self.primUnpack('>i', 4)

    def readNextFloat(self):
        return self.primUnpack('>f', 4)

    def readNextLong(self):
        return self.primUnpack('>l', 4)

    def readNextpString(self):
        nb = self.readNextByte()
        chars = [self.readNextChar() for i in range(nb)]
        return ''.join(chars)

    def readNextShort(self):
        return self.primUnpack('>h', 2)

    def readNextString(self, size):
        chars = [self.readNextChar() for i in range(size)]
        return ''.join(chars)

    def readNextThumb(self):
        return (self.readNextLong(), self.readNextLong(), self.readNextByte(), self.readNextByte())

    def readNextUnsignedInt(self):
        return self.primUnpack('>I', 4)

    def readNextUserData(self, type, num):
        # to be overwritten in user's code
        return NotImplemented

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

    def close(self):
        self.file.close()

    def seek(self, pos):
        self.file.seek(pos)

    def tell(self):
        return self.file.tell()


SG1_TYPES = {1: 'byte', 2: 'char', 3: 'word', 4: 'short', 5: 'long', 7: 'float', 8: 'double', 10: 'date', 11: 'time', 12: 'thumb', 13: 'bool', 18: 'pString', 19: 'cString'}

class DirEntry:# Reader
    def __init__(self, reader):
        self.name = reader.readNextString(4)        # tag name
        self.number = reader.readNextInt()          # tag number
        self.elementtype = reader.readNextShort()   # element type code
        self.elementsize = reader.readNextShort()   # size in bytes of one element
        self.numelements = reader.readNextInt()     # number of elements in item
        self.datasize = reader.readNextInt()        # size in bytes of item
        self.dataoffsetpos = reader.tell()
        self.dataoffset = reader.readNextInt()      # item's data, or offset in file
        self.datahandle = reader.readNextInt()      # reserved

    def __str__(self):
        return "%s (%i) / %s (%i)" % (self.name, self.number, self.mytype(), self.numelements)

    def mydataoffset(self):
        if self.datasize <= 4:
            return self.dataoffsetpos
        else:
            return self.dataoffset

    def mytype(self):
        if self.elementtype < 1024:
            return SG1_TYPES.get(self.elementtype, 'unknown')
        else:
            return 'user'