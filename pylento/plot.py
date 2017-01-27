#!/usr/bin/env python
#coding=utf-8
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

DEFAULT_COLORS = (
    (31/255, 119/255, 180/255),
    (214/255, 39/255, 40/255)
)


def plot_lento(LObj, showlabels=False, singles=True, filename=None, colors=DEFAULT_COLORS):
    splits = list(LObj.iter_splits())
    
    if not singles:
        splits = [s for s in splits if s.ntaxa > 1]
    
    x = range(len(splits))
    
    if showlabels:
        labels = [repr(s) for s in splits]
    else:
        labels = [_ + 1 for _ in x]
    
    ax = plt.subplot(1, 1, 1)
    # remove chartjunk
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    
    ax.bar(
        x,
        [s.support for s in splits],
        width=1, color=DEFAULT_COLORS[0],
        align="center"
    )
    ax.bar(
        x,
        [- s.conflict for s in splits],
        width=1,
        color=DEFAULT_COLORS[1],
        align="center"
    )
    
    plt.plot()
    plt.xlabel("Split", fontsize=16)
    plt.ylabel("Strength", fontsize=16)
    plt.xticks(x, labels, rotation='vertical', fontsize=8)
    plt.margins(0.05)
    plt.subplots_adjust(bottom=0.20)
    plt.tight_layout()
    
    if filename:
        plt.savefig(filename)
    return plt
