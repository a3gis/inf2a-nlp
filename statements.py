# File: statements.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev

from collections import defaultdict

# PART A: Processing statements

def add(lst,item):
    if (item not in lst):
        lst.insert(len(lst),item)

class Lexicon:
    """stores known word stems of various part-of-speech categories"""
    # add code here
    def __init__(self):
        self.dic = defaultdict(lambda: [])
    
    def add(self, stem, cat):
        add(self.dic[cat], stem)
	
    def getAll(self, cat):
        return self.dic[cat]

class FactBase:
    # add code here
    def __init__(self):
        self.unary = defaultdict(lambda: [])
        self.binary = defaultdict(lambda: [])

    def addUnary(self, pred, e1):
        add(self.unary[pred], e1)

    def addBinary(self, pred, e1, e2):
        add(self.binary[pred], (e1, e2))

    def queryUnary(self, pred, e1):
        return e1 in self.unary[pred]

    def queryBinary(self, pred, e1, e2):
        return (e1, e2) in self.binary[pred]

import re

vowels = ['a', 'e', 'i', 'o', 'u']

def endswith_any(x, suffixes):
    return any(map(lambda s: x.endswith(s), suffixes))

def verb_stem(s):
    """extracts the stem from the 3sg form of a verb, or returns empty string"""
    # add code here
    if s.endswith('s'):
        if not endswith_any(s[:-1], ['s', 'x', 'y', 'z', 'ch', 'sh'] + vowels):
            return s[:-1]
        elif re.match('.*[aeiou]y$', s[:-1]):
            return s[:-1]
    if s.endswith('ies'):
        if re.match('.*[^aeiou]$', s[:-3]):
            if len(s) > 4:
                return s[:-3] + 'y'
            elif len(s) == 4:
                return s[:-1]
    if re.match('.*(o|x|ch|sh|ss|zz)es$', s):
        return s[:-2]
    if re.match('.*([^s]se|[^z]ze)s$', s):
        return s[:-1]
    if s == 'has':
        return 'have'
    if s.endswith('es') and not re.match('.*(i|o|s|x|z|ch|sh)es$', s):
        return s[:-1]
    return ''


def add_proper_name (w,lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w,'P')
        return ''
    else:
        return (w + " isn't a proper name")

def process_statement (lx,wlist,fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name (wlist[0],lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a','an']):
                lx.add (wlist[3],'N')
                fb.addUnary ('N_'+wlist[3],wlist[0])
            else:
                lx.add (wlist[2],'A')
                fb.addUnary ('A_'+wlist[2],wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add (stem,'I')
                fb.addUnary ('I_'+stem,wlist[0])
            else:
                msg = add_proper_name (wlist[2],lx)
                if (msg == ''):
                    lx.add (stem,'T')
                    fb.addBinary ('T_'+stem,wlist[0],wlist[2])
    return msg
                        
# End of PART A.

