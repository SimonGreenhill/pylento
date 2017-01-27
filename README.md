# PyLento

[![Build Status](https://travis-ci.org/SimonGreenhill/pylento.svg?branch=master)](https://travis-ci.org/SimonGreenhill/pylento)
[![Coverage Status](https://coveralls.io/repos/SimonGreenhill/pylento/badge.svg?branch=master&service=github)](https://coveralls.io/github/SimonGreenhill/pylento?branch=master)

A python library for calculating phylogenetic splits and creating Lento plots from a nexus file.

A Lento plot shows each split (i.e. a grouping of taxa) and its associated support (i.e. amount of sites or cognates that support it) above the horizontal axis. Sites that conflict with a given split are shown below the axis. There's more on the the [theory here](https://www.ctu.edu.vn/~dvxe/Bioinformatic/Software/BIT%20Software/theory.html) and in Lento et al (1995). 

Here is a *Lento plot* showing the splits in the Ramu-Lower Sepik language cognates from [TransNewGuinea.org](http://transnewguinea.org).

![Lento Plot](https://github.com/SimonGreenhill/pylento/blob/master/doc/rls.png)

Lento plots are described in:

```
```

## Usage: Command line

*Basic usage:*

```shell
> pylento

usage: pylento [-h] [-p PLOT] [--label] [--nosingles] input
```

*Display splits:*

```shell
> pylento doc/ramu.nex

1    72    0    angoram:chambri:kopar:murik:tabriak:yimas
2    41    0    aruamu:kanggape:kire:tanggu
3    20    0    tanggu
4    20    0    aruamu
5    19    0    kire
6    18    0    kanggape
7    14    0    yimas
8    13    0    chambri
9    13    0    murik
10    13    0    tabriak
11    13    0    kopar
12    12    0    angoram
13    6    6    chambri:kopar:murik:tabriak:yimas
14    4    11    angoram:chambri:kopar:tabriak:yimas
15    2    13    angoram:murik:tabriak:yimas
16    2    6    kopar:murik:yimas
17    1    6    chambri:kopar:murik:yimas
18    1    1    aruamu:kire
19    1    1    kanggape:kire
```

i.e. the split of (angoram:chambri:kopar:murik:tabriak:yimas) has 72 sites (=cognates) supporting it
and no conflicting sites. In contrast the split (angoram:chambri:kopar:tabriak:yimas) has 4 sites 
supporting it and 11 conflicting with it.

*Plot file to rls.png*

```shell
pylento -p rls.png doc/rls.nex rls.png
```

## Usage: Library

```python
from nexus import NexusReader
nex = NexusReader('doc/rls.nex')
L = Lento(nex.data.matrix)
print(L.splits)
```
Note: you don't need [python-nexus](https://pypi.python.org/pypi/python-nexus/1.35) to use this, you just need a data matrix that looks something 
like:

```python
matrix = {
    'A': ['1', '1', '1', '1', '0', '1', '0', '1', '1'],
    'B': ['1', '1', '1', '0', '0', '0', '0', '1', '0'],
    'C': ['1', '1', '0', '0', '1', '0', '1', '0', '0'],
    'D': ['1', '0', '0', '0', '0', '0', '1', '0', '1']
}
L = Lento(matrix)
```


## References:

* Lento, G.M., Hickson, R.E., Chambers G.K., and Penny, D. (1995) Use of spectral analysis to test hypotheses on the origin of pinninpeds. J. Mol. Biol. Evol., 12, 28-52. 
