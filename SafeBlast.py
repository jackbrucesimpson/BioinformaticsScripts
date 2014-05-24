#! /usr/bin/env python

#-------------------------------------------------------------------------------
# Name:        SafeBlast
# Purpose:     Program that runs a blast without crashing due to timeout/loss of connection
#
# Author:      Jack Simpson
#
# Created:     07/05/2014
#-------------------------------------------------------------------------------
import time
# These modules come with the BioPython library
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML

def blast_seqs(each_seq):
    ''' Takes a sequence and runs a blast search '''
    # My blast parameters, let me know if they could be better optimised for shorter primers
    blast_handle = NCBIWWW.qblast("blastn", "nt", each_seq, expect=0.04, hitlist_size = 1000, word_size=7)
    blast_result = NCBIXML.read(blast_handle)
    blast_handle.close()
    for alignment in blast_result.alignments:
        for hsp in alignment.hsps:
            return alignment.title

def main():
    # some example sequences
    seq_list = ["GCGGTTCCCACTGGTATT","AAAGCTCATGTTGAAGCTCC","GGAGCTTCAACATGAGCTTT","AATACCAGTGGGAACCGC"]

    for each_seq in seq_list:
        print(each_seq)
        # This is where I use exceptions so that the program doesn't crash if Blast fails
        connected = False
        while not connected:
            try:
                blast_result = blast_seqs(each_seq)
                print blast_result
                connected=True
                time.sleep(3)
            except:
                print("Server busy, will sleep and try again in 10 minutes")
                time.sleep(600)

if __name__ == '__main__':
    main()