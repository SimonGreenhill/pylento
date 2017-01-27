#!/usr/bin/env python
#coding=utf-8
import os
import sys
import argparse

try:
    from nexus import NexusReader
except ImportError:  # pragma: no cover
    raise ImportError("Please install python-nexus")

from .lento import Lento
from .plot import plot_lento

def parse_args(args):
    """Parses command line arguments"""
    descr = 'Constructs a tree from a classification table'
    parser = argparse.ArgumentParser(description=descr)
    parser.add_argument("input", help="inputfile")
    parser.add_argument(
        '-p', "--plot", dest='plot', default=None,
        help="plot file", action='store'
    )
    parser.add_argument(
        "--label", dest='label', default=False,
        help="plot with labels", action='store_true'
    )
    parser.add_argument(
        "--nosingles", dest='nosingles', default=False,
        help="ignore singleton taxa", action='store_true'
    )
    args = parser.parse_args(args)
    if not os.path.isfile(args.input):
        raise IOError("File %s does not exist" % args.input)
    return args


def main(args=None):  # pragma: no cover
    if args is None:
        args = sys.argv[1:]
    args = parse_args(args)
    L = Lento(NexusReader(args.input).data.matrix)
    
    print(L.write())

    if args.plot:
        plot_lento(
            L,
            filename=args.plot,
            showlabels=args.label,
            singles=not args.nosingles
        )
