from __future__ import division, print_function

import sys
import argparse

class Block(object):
    """Defines a block of memory addresses"""
    def __init__(self, num=0, utime=0):
        self.num = int(num)
        self.utime = int(utime)

    def __repr__(self):
        return str(self.num)

class Cache(object):
    """Defines the cache object, which can hold a number of blocks"""
    def __init__(self, bsize, bcount, assoc, htime, mtime, repl="F"):
        self.bsize = int(bsize)
        self.bcount = int(bcount)
        self.assoc = int(assoc)
        self.htime = int(htime)
        self.mtime = int(mtime)
        self.repl = str(repl)
        
        self.blist = [None] * bcount
        self.blocks = {}
        self.hcount = 0
        self.mcount = 0

    def fetch(self, addr):
        bnum = addr // self.bsize
        b = self.blocks.setdefault(bnum, Block(bnum))
        
        if b in self.blist:
            self.hcount += 1
            return
        
        self.mcount += 1
        if self.assoc == 1: # Direct Mapping
            self.blist[bnum % self.bcount] = b


    def stats(self):
        hrate = self.hcount / (self.hcount + self.mcount)
        mrate = self.mcount / (self.hcount + self.mcount)
        amat = self.htime + (mrate * self.mtime)
        print("Hit Rate: {}".format(hrate))
        print("Average Memory Access Time: {}".format(amat))

def parseConfig():
    """Provides an interface for parsing command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-S', '--bsize', 
        type=int, required=True,
        help="Size of a block in words."
    )
    parser.add_argument('-C', '--bcount', 
        type=int, required=True,
        help="Number of blocks in the cache."
    )
    parser.add_argument('-A', '--assoc', 
        type=int, required=True,
        help="Associativity, 1=Direct, 2=Two-Way Set, ..."
    )
    parser.add_argument('-H', '--htime', 
        type=int, required=True,
        help="Hit time in cycles"
    )
    parser.add_argument('-M', '--mtime', 
        type=int, required=True,
        help="Miss time in cycles"
    )
    return parser.parse_args()

def main():
    # Parse the input arguments and construct the Cache Object
    a = parseConfig()
    c = Cache(a.bsize, a.bcount, a.assoc, a.htime, a.mtime, "F")

    # Read an address from stdin and attempt to fetch it in the Cache
    for line in sys.stdin:
        c.fetch(int(line, 0))
    
    # Print the Cache stats at the end of the program
    c.stats()
    print(c.blist)

if __name__ == "__main__":
    main()
