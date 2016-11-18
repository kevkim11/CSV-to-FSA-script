
import struct
import datetime

from ABIFReader import *

class SG1_Reader:
    """
    Class to read SG1 binary files.
    Has similar structure to that of an FSA file.
    """
    def __init__(self, fn):
        self.filename = fn
        self.file = open(fn, 'rb')
        self.type = self.readNextString(4)
        if self.type != 'SG1F':
            self.close()
            raise SystemExit("error: No SG1F file '%s'" % fn)
        self.version = self.readNextShort()
        dir = DirEntry(self)
        self.seek(dir.dataoffset)
        self.entries = [DirEntry(self) for i in range(dir.numelements)]

    def getData(self, name, num=1):
        entry = self.getEntry(name, num)
        if not entry:
            raise SystemExit("error: Entry '%s (%i)' not found in '%s'" % (name, num, self.filename))
        self.seek(entry.mydataoffset())
        data = self.readData(entry.elementtype, entry.numelements)
        if data != NotImplemented and len(data) == 1:
            return data[0]
        else:
            return data

    def showEntries(self):
        for e in self.entries:
            print e

    def getEntry(self, name, num):
        for e in self.entries:
            if e.name == name and e.number == num:
                return e
        return None

    def readData(self, type, num):
        if type == 1:
            return [self.readNextByte() for i in range(num)]
        elif type == 2:
            return self.readNextString(num)
        elif type == 3:
            return [self.readNextUnsignedInt() for i in range(num)]
        elif type == 4:
            return [self.readNextShort() for i in range(num)]
        elif type == 5:
            return [self.readNextLong() for i in range(num)]
        elif type == 7:
            return [self.readNextFloat() for i in range(num)]
        elif type == 8:
            return [self.readNextDouble() for i in range(num)]
        elif type == 10:
            return [self.readNextDate() for i in range(num)]
        elif type == 11:
            return [self.readNextTime() for i in range(num)]
        elif type == 12:
            return [self.readNextThumb() for i in range(num)]
        elif type == 13:
            return [self.readNextBool() for i in range(num)]
        elif type == 18:
            return self.readNextpString()
        elif type == 19:
            return self.readNextcString()
        elif type >= 1024:
            return self.readNextUserData(type, num)
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
        return datetime.date(self.readNextShort(), self.readNextByte(), self.readNextByte())

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

    def readNextTime(self):
        return datetime.time(self.readNextByte(), self.readNextByte(), self.readNextByte(), self.readNextByte() * 10000)

    def readNextUnsignedInt(self):
        return self.primUnpack('>I', 4)

    def readNextUserData(self, type, num):
        # to be overwritten in user's code
        return NotImplemented

    def primUnpack(self, format, nb):
        """

        :param format:
        :param nb: number of bytes
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