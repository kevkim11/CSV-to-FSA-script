import struct
import datetime

from ABIFReader import *

class SG1_Writer:
    """
    Class to create SG1 binary files using a list of list of 5 dyes.
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