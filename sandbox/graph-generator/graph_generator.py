#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from glob import glob
from random import random, shuffle

import networkx as nx
import pandas as pd

import utils

p = 0.5


def load_Vnodes():
    global virtual_nodes
    with open('dictionary', 'rb') as f:
        virtual_nodes = f.read().split(',')


def get_Vnodes():
    global virtual_nodes
    return virtual_nodes.pop(0)


def inject_noise(G):
    load_Vnodes()
    # add node
    if random() < p:
        u = G.nodes()
        shuffle(u)
        v = get_Vnodes()
        if random() < p:
            G.add_edge(u[0], v)
        else:
            G.add_edge(v, u[0])
    else:
        H = nx.complement(G)
        e = H.edges()
        shuffle(e)
        G.add_edge(*e[0])
    return G


def get_graph_info(G):
    """Convert graph into tabular data
    row = node, degree, in_degree, out_degree
    """
    nodes = G.nodes()
    in_degrees = []
    out_degrees = []
    for i in nodes:
        in_degrees.append(G.in_degree(i))
        out_degrees.append(G.out_degree(i))
    degrees = zip(in_degrees, out_degrees)
    return zip(*[nodes, degrees, in_degrees, out_degrees])


def statistic(G):
    df = pd.DataFrame(get_graph_info(G), columns=['node', 'degree', 'in_deg', 'out_deg'])
    print df.degree.value_counts()


def outputToHTML():
    pics = glob('pics/*.png')

    with open('demo.html', 'w') as f:
        f.write('<table border="1">')
        f.write('<tbody>')

        for i in pics:
            f.write('<tr>')
            f.write('<td><img src="{}" />'.format(i))
            f.write('</tr>')

        f.write('</tbody>')
        f.write('</table>')


# In[6]:

created = []

dir = 'pics'
utils.deletePng(dir)
for i in range(1, 501):
    G = nx.DiGraph()
    G.add_edges_from([(2, 1), (3, 1)])
    for _ in range(1):
        G = inject_noise(G)

    isSkip = False
    for H in created:
        if nx.is_isomorphic(G, H):
            isSkip = True

    if not isSkip:
        nx.write_dot(G, 'pics/{:03}.dot'.format(i))
        cmd = 'sfdp -x -Goverlap=prism -Tpng pics/{} > pics/{}'.format('{:03}.dot'.format(i), '{:03}.png'.format(i))
        os.system(cmd)
    created.append(G)
utils.deleteDot(dir)

outputToHTML()


created = []

dir = 'pics2'

utils.deletePng(dir)
for i in range(1, 501):
    G = nx.DiGraph()
    G.add_edges_from([(2, 1), (3, 1)])
    for _ in range(2):
        G = inject_noise(G)

    isSkip = False
    for H in created:
        if nx.is_isomorphic(G, H):
            isSkip = True

    if not isSkip:
        nx.write_dot(G, 'pics2/{:03}.dot'.format(i))
        cmd = 'sfdp -x -Goverlap=prism -Tpng pics2/{} > pics2/{}'.format('{:03}.dot'.format(i), '{:03}.png'.format(i))
        os.system(cmd)
    created.append(G)
utils.deleteDot(dir)

outputToHTML()

dir = 'pics3'

utils.deletePng(dir)
for i in range(1, 501):
    G = nx.DiGraph()
    G.add_edges_from([(2, 1), (3, 1)])
    for _ in range(3):
        G = inject_noise(G)

    isSkip = False
    for H in created:
        if nx.is_isomorphic(G, H):
            isSkip = True

    if not isSkip:
        nx.write_dot(G, 'pics2/{:03}.dot'.format(i))
        cmd = 'sfdp -x -Goverlap=prism -Tpng pics3/{} > pics3/{}'.format('{:03}.dot'.format(i), '{:03}.png'.format(i))
        os.system(cmd)
    created.append(G)
utils.deleteDot(dir)

outputToHTML()

