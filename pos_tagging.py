# File: pos_tagging.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev



# PART B: POS tagging

from statements import *

# The tagset we shall use is:
# P  A  Ns  Np  Is  Ip  Ts  Tp  BEs  BEp  DOs  DOp  AR  AND  WHO  WHICH  ?

tagset = ['P',  'A',  'Ns',  'Np',  'Is',  'Ip',  'Ts',  'Tp',  'BEs',  'BEp',  'DOs',  'DOp',  'AR',  'AND',  'WHO',  'WHICH',  '?']

# Tags for words playing a special role in the grammar:

function_words_tags = [('a','AR'), ('an','AR'), ('and','AND'),
     ('is','BEs'), ('are','BEp'), ('does','DOs'), ('do','DOp'), 
     ('who','WHO'), ('which','WHICH'), ('Who','WHO'), ('Which','WHICH'), ('?','?')]
     # upper or lowercase tolerated at start of question.

function_words = [p[0] for p in function_words_tags]

# English nouns with identical plural forms (list courtesy of Wikipedia):

unchanging_plurals = ['bison','buffalo','deer','fish','moose','pike','plankton',
     'salmon','sheep','swine','trout']


def noun_stem (s):
    if s in unchanging_plurals:
        return s
    elif s.endswith('men'):
        return s[:-3] + 'man'
    else:
        return verb_stem(s)
    # add code here

lx1 = Lexicon()
lx1.add('John', 'P')
lx1.add('orange', 'N')
lx1.add('orange', 'A')
lx1.add('fish', 'N')
lx1.add('fish', 'I')
lx1.add('fish', 'T')
lx1.add('like', 'T')
lx1.add('duck', 'N')
lx1.add('fly', 'T')

def tag_word (lx,wd):
    """returns a list of all possible tags for wd relative to lx"""
    # add code here
    if wd in function_words:
        return [dict(function_words_tags)[wd]]

    # should handle the verb case too
    ns = noun_stem(wd)
    stem = ns or wd
    is_plural = (ns != '')

    cats = [t for t in ['P', 'N', 'A', 'I', 'T'] if stem in lx.getAll(t)]

    tags = []
    for cat in cats:
        if cat == 'N' and (wd in unchanging_plurals):
            add(tags, 'Ns')
        if cat in ['N']:
            suffix = 'p' if is_plural else 's'
            add(tags, cat + suffix)
        elif cat in ['I', 'T'] and (wd in unchanging_plurals):
            add(tags, cat + 'p')
        elif cat in ['I', 'T']:
            suffix = 's' if is_plural else 'p'
            add(tags, cat + suffix)
        else:
            add(tags, cat)
    return tags
    

def tag_words (lx, wds):
    """returns a list of all possible taggings for a list of words"""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word (lx, wds[0])
        tag_rest = tag_words (lx, wds[1:])
        return [[fst] + rst for fst in tag_first for rst in tag_rest]

# End of PART B.
