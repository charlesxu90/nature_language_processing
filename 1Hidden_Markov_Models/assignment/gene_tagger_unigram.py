#! /usr/bin/python 

__author__="Charles Xu <charlesxu90@gmail.com>"
__date__="$June 2, 2015"

import sys
from collections import defaultdict
import math

"""
Inplementation of 1-gram 
"""

"""
First, read the frequency data; get counts for each (word, tag) pair and tag.
Then, get max C(word, tag) over all tags.
"""

def read_counts(counts_f, counts, word_dict, uni_tag):
    """
    Read the counts_file and get the counts for (word, tag) pair and tag.
    """

    for l in counts_f:
        line = l.strip().split(' ')
        if line[1] == 'WORDTAG':
            counts[(line[3], line[2])] = int(line[0])
            word_dict.append(line[3])
        elif line[1] == '1-GRAM':
            uni_tag[(line[2])] = int(line[0])


def counts_tagger(counts, word_dict, uni_tag, tagger):
    """
    Based on counts and uni_tag, get the emission probability for all (word, tag) pair
    """

    for word in word_dict:
        max_tag = ''
        max_val = 0.0
        for tag in uni_tag:
            if float(counts[(word, tag)])/float(uni_tag[(tag)]) > max_val:
                max_val = float(counts[(word, tag)])/float(uni_tag[(tag)])
                max_tag = tag

        tagger[(word)] = max_tag

def tag_gene(dev_f, out_f, tagger):
    """
    Tag the dev file using the counts and unigram counts data based on unigram model.
    """
    
    for l in dev_f:
        line = l.strip()
        if line:
            if line in tagger:
                out_f.write("%s %s\n" % (line, tagger[(line)]))
            else:
                out_f.write("%s %s\n" % (line, tagger[('_RARE_')]))
        else:
            out_f.write("\n")

def usage():
    print """
    python ./gene_tagger_unigram.py [counts_file] [dev_file] > [output_file]
        Read in a gene counts input file and a gene dev input file and produce a work tag file.
        """

if __name__ == "__main__":

    if len(sys.argv)!=3:  # Exactly two input files
        usage()
        sys.exit(2)

    try:
        counts_f = file(sys.argv[1], "r")
    except IOError:
        sys.stderr.write("ERROR: Cannot read inputfile %s. \n" % sys.argv[1])
        sys.exit(1)

    counts = defaultdict(int)
    uni_tag = defaultdict(int)
    word_dict = []
    
    read_counts(counts_f, counts, word_dict, uni_tag)
    counts_f.close()

    #for i in counts:
    #    sys.stderr.write("%s %d\n" % (str(i), counts[i] ))
   
    #for i in word_dict:
    #    sys.stderr.write("%s\n" % (str(i)))
    #for i in uni_tag:
    #    sys.stderr.write("%s %d\n" % (str(i), uni_tag[i]))

    tagger = {}
    counts_tagger(counts, word_dict, uni_tag, tagger)

    try:
        dev_f = file(sys.argv[2], "r")
    except IOError:
        sys.stderr.write("ERROR: Cannot read inputfile %s. \n" % sys.argv[2])
        sys.exit(1)

    tag_gene(dev_f, sys.stdout, tagger)
    dev_f.close()

