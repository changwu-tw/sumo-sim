#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import matplotlib.pyplot as plt
import networkx as nx
import os
import sys

import anony
import utils

from collections import deque
from itertools import permutations
from random import random, shuffle

# import sys
# sys.path.append('../')

p_pf = 0.01
p_pd = 0.75
p_shift = 0.6

number_of_node = 10

G = nx.DiGraph()

letters = 'abcdefghijklmnopqrst' * 5
linkage = dict(zip(range(1, 101), letters))

d = {}
for i in range(1, number_of_node + 1):
    d["a{0}".format(i)] = deque([i, i + 20, i + 40, i + 60, i + 80])


def addCertToCert(nodes):
    edges = permutations(nodes, 2)
    for e in edges:
        if random() < p_pf and random() < p_pd:
            G.add_edge(*e)
    return G


def getNodes():
    nodes = []
    for k, v in d.items():
        if random() < p_shift:
            d[k].rotate(-1)
        nodes.append(v[0])
    return nodes


def saveToPng(G, i, var='initial'):
    dotname = 'pic/{:03}{}.dot'.format(i, var)
    nx.write_dot(G, dotname)
    pngname = 'pic/{:03}_{}.png'.format(i, var)
    cmd = 'sfdp -x -Goverlap=prism -Tpng {} > {}'.format(dotname, pngname)
    os.system(cmd)


def deleteDot():
    os.system('rm -f {}'.format(" ".join(glob.glob('pic/*.dot'))))


def deletePng():
    os.system('rm -f {}'.format(" ".join(glob.glob('pic/*.png'))))


if __name__ == '__main__':
    deletePng()

    end = (int)(sys.argv[1])
    for i in range(1, end + 1):
        G = addCertToCert(getNodes())
        if G.nodes():
            saveToPng(G, i)
            H = nx.DiGraph()
            H = nx.relabel_nodes(G, linkage)
            saveToPng(H, i, 'linkage')
            A = anony.anonymize(H)
            saveToPng(A, i, 'perturb')

    deleteDot()

    utils.outputToHTML()


# nx.draw(G)
# plt.show()
