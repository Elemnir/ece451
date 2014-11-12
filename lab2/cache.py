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
    def __init__(self, bsize, bcount, assoc, htime, mtime, repl="r"):
        self.bsize = int(bsize)   # Size of the Block in Words
        self.bcount = int(bcount) # Number of Blocks in the Cache
        self.assoc = int(assoc)   # Size of Associative Sets in the Cache
        self.htime = int(htime)   # Hit time in cycles
        self.mtime = int(mtime)   # Miss penalty in cycles
        self.repl = str(repl)     # Page replacement algorithm setting
        
        self.blist = [None] * self.bcount
        self.blocks = {}
        self.setcount = self.bcount // self.assoc
        self.hcount = 0
        self.mcount = 0

    def fetch(self, addr):
        # Update Recently Used Time
        for b in self.blist:
            if b is not None:
                b.utime += 1
        
        # Find the Block that corresponds to the given Address
        bnum = addr // self.bsize
        b = self.blocks.setdefault(bnum, Block(bnum))
        b.utime = 0

        # Cache Hit
        if b in self.blist:
            self.hcount += 1
            return
        
        # Cache Miss
        self.mcount += 1
        cindex = (bnum % self.bcount) * self.assoc
        if self.assoc == 1: # Direct Mapping
            self.blist[cindex] = b
        else:
            pass


    def stats(self):
        hrate = self.hcount / (self.hcount + self.mcount)
        mrate = self.mcount / (self.hcount + self.mcount)
        amat = self.htime + (mrate * self.mtime)
        print("Reads: {}".format(self.hcount + self.mcount))
        print("Hits: {}".format(self.hcount))
        print("Misses: {}".format(self.mcount))
        print("Hit Rate: {}".format(hrate))
        print("Miss Rate: {}".format(mrate))
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
    parser.add_argument('-R', '--pra',
        type=str, default="r",
        help="Page Replacement Algorithm: r=Random, l=LRU"
    )
    return parser.parse_args()

def main():
    # Parse the input arguments and construct the Cache Object
    a = parseConfig()
    c = Cache(a.bsize, a.bcount, a.assoc, a.htime, a.mtime, a.pra)

    # Read an address from stdin and attempt to fetch it in the Cache
    for line in sys.stdin:
        c.fetch(int(line, 0))
    
    # Print the Cache stats at the end of the program
    c.stats()
    print(c.blist)

if __name__ == "__main__":
    main()
