#!/usr/bin/env python
#coding=utf-8
import os
import codecs


class Split(object):
    def __init__(self, taxa=None, support=0, conflict=0):
        self.taxa = taxa
        self.support = support
        self.conflict = conflict
    
    def __repr__(self):
        return ":".join(sorted(self.taxa))
    
    def __lt__(self, other):
        return self.support < other.support

    def __le__(self, other):
        return self.support <= other.support

    def __eq__(self, other):
        return (
            (self.taxa == other.taxa) and 
            (self.support == other.support) and 
            (self.conflict == other.conflict)
        )
    
    @property
    def ntaxa(self):
        return len(self.taxa)
        
    def is_conflicting(self, other):
        smaller, bigger = sorted([self.taxa, other.taxa], key=len)
        # no conflict if the small is completely nested:
        if all([s in bigger for s in smaller]):
            return False
        # no conflict if none of the small taxa is in bigger group
        elif all([s not in bigger for s in smaller]):
            return False
        else:
            return True
    
    def get_normalised(self, ratio):
        return self.conflict * ratio
        

class Lento(object):
    states_to_ignore = ['0', '?', '-']
    
    def __init__(self, matrix=None):
        self.matrix = matrix or {}
        self._splits = None
        self._normalising_ratio = None
        
    @property
    def ntaxa(self):
        return len(self.matrix)

    @property
    def nchar(self):
        return len(self.matrix[self.taxa[0]])
    
    @property
    def taxa(self):
        return sorted(self.matrix.keys())
    
    @property
    def total_splits(self):
        return self._get_total_splits(self.ntaxa)
    
    @property
    def splits(self):
        if self._splits is None:
            self.get_splits()
        return self._splits 
    
    @property
    def normalising_ratio(self):
        """
        Returns a float of the normalising ratio.
        
        Because a split can be incompatible with many other splits, the
        frequency of conflict can be larger then the support. Therefore, the
        conflict scores are normalized following Lento et al. (1995) by the
        ratio of the sum of all support values to conflict values.
        """
        if self._normalising_ratio is None:
            support = sum([self.splits[s].support for s in self.splits])
            conflict = sum([self.splits[s].conflict for s in self.splits])
            self._normalising_ratio = support / conflict
        return self._normalising_ratio
    
    def iter_splits(self):
        return sorted([self.splits[s] for s in self.splits], reverse=True)
    
    def _get_total_splits(self, n):
        return pow(2, n - 1)
    
    def get_splits(self):
        if self._splits is None:
            self._splits = {}
            # identify splits and support
            for i in range(0, self.nchar):
                states = set([
                    self.matrix[t][i] for t in self.taxa
                    if self.matrix[t][i] not in self.states_to_ignore
                ])
                for state in states:
                    s = Split([t for t in self.taxa if self.matrix[t][i] == state])
                    self._splits[repr(s)] = self._splits.get(repr(s), s)
                    self._splits[repr(s)].support += 1
        
            # identify conflicts
            for s in self.splits.values():
                s.conflict = sum([
                    o.support for o in self.splits.values() if s.is_conflicting(o)
                ])
        return self._splits
        
    def summary(self):
        return {
            'total': self.total_splits,
            'observed': len(self.splits),
            'supported': sum([self.splits[s].support for s in self.splits]),
            'conflicted': sum([self.splits[s].conflict for s in self.splits]),
        }
    
    def write(self, filename=None):
        buffer = []
        for i, s in enumerate(self.iter_splits(), 1):
            buffer.append("\t".join([
                "%d" % i,
                "%d" % s.support,
                "%d" % s.conflict,
                "%f" % s.get_normalised(self.normalising_ratio),
                "%s" % s,
            ]))
        buffer = "\n".join(buffer)
        
        if filename:
            with codecs.open(filename, 'w', encoding="utf8") as handle:
                handle.write(buffer)
        return buffer


