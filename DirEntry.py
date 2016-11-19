"""
The next 28 bytes comprise a single directory entry structure that points to the directory. A directory entry is a packed structure (no padding bytes) of the following form:
struct DirEntry{
  SInt32 name;
  SInt32 number;
  SInt16 elementtype;
  SInt16 elementsize;
  SInt32 numelements;
  SInt32 datasize;
  SInt32 dataoffset;
  SInt32 datahandle;
//tag name
//tag number
//element type code
//size in bytes of one element //number of elements in item //size in bytes of item //item's data, or offset in file //reserved
}
"""

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


class DirEntryWriter:
    def __init__(self, writer):
        self.name = 'tdir'  # str
        self.number = 1     # int
        self.elementtype = 1023      # int
        self.elementsize = 28        # int
        self.numelements = 10        # int
        self.datasize = 280          # int
        self.dataoffsetpos = 26      # int
        self.dataoffset = 70438      # int
        self.datahandle = 0          # int

    def __str__(self):
        return "%s (%i) / (%i)" % (self.name, self.number, self.numelements)