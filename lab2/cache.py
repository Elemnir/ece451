from __future__ import division, print_function

from random import randrange
from operator import attrgetter
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
    def __init__(self, bsize, bcount, assoc, htime, mtime, pra="r"):
        self.bsize = int(bsize)   # Size of the Block in Words
        self.bcount = int(bcount) # Number of Blocks in the Cache
        self.assoc = int(assoc)   # Size of Associative Sets in the Cache
        self.htime = int(htime)   # Hit time in cycles
        self.mtime = int(mtime)   # Miss penalty in cycles
        self.pra = str(pra)       # Page replacement algorithm setting
        
        # List of cached-in blocks
        self.blist = [None] * self.bcount
        
        # List of all referenced Blocks
        self.blocks = {}

        # Number of Sets in the Cache
        self.setcount = self.bcount // self.assoc
        
        # Records for number of hits and number of misses
        self.hcount = 0
        self.mcount = 0


    def fetch(self, addr):
        # Update Recently Used Time for each item in the cache
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
        cindex = (bnum % self.setcount) * self.assoc
        
        # If there's an empty space, put it there
        for i in range(self.assoc):
            if self.blist[cindex + i] == None:
                self.blist[cindex + i] = b
                break
        
        # Otherwise, invoke the page replacement algorithm
        else:
            if self.pra == "r": # Random Replacement algorithm
                i = randrange(self.assoc)
                self.blist[cindex + i] = b
            elif self.pra == "l": # Least Recently Used Replacement algorithm
                i = self.blist.index(max(self.blist[cindex:cindex+self.assoc], key=attrgetter("utime")))
                self.blist[i] = b


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
    parser.add_argument('-P', '--print_cache',
        action='store_true',
        help="If given, the final cache contents will be printed to stout"
    )
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
    parser.add_argument('-F', '--fname',
        type=str, default="",
        help="Name of file to use as input, defaults to stdin if not provided"
    )
    return parser.parse_args()


def main():
    # Parse the input arguments and construct the Cache Object
    a = parseConfig()
    c = Cache(a.bsize, a.bcount, a.assoc, a.htime, a.mtime, a.pra)
    if a.fname == "":
        source = sys.stdin
    else:
        source = open(a.fname)

    # Read an address from source and attempt to fetch it in the Cache
    for line in source:
        c.fetch(int(line, 0))
    
    # Print the Cache stats at the end of the program
    c.stats()
    
    if a.print_cache:
        print(c.blist)


if __name__ == "__main__":
    main()
