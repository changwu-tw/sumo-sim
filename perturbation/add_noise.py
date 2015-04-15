#!/usr/bin/env python

import itertools
import math
import os
import random
import sys
sys.path.append('../..')

from datetime import datetime
from random import choice

import networkx as nx
import numpy as np
from numpy import genfromtxt

from sumo_sim import helper

# 18728 words
with open('dictionary', 'rb') as f:
    virtual_nodes = f.read().split(',')

percentage = 0.2
index = 0
timeslot = True


def getVnodes():
    global virtual_nodes
    return virtual_nodes.pop(0)


def saveGraph(G, filename, dir):
    global index
    index += 1
    helper.saveToDotGraph(G, '{}/{:0>3d}_{}'.format(dir, index, filename))


def graphInfo(G):
    helper.draw_table(G)
    helper.graph_info(G)


def method(G):
    num_of_necessary_vnodes = (int)(math.ceil(G.number_of_nodes()*percentage))
    num_of_necessary_vedges = (int)(math.ceil(G.number_of_edges()*percentage))

    # Add confusing nodes
    nodelist = G.nodes()
    random.shuffle(nodelist)

    confusing_nodes = []
    for u in nodelist[:num_of_necessary_vnodes]:
        v = getVnodes()
        G.add_edge(u, v, color='green')
        G.add_node(v, color='blue', style='filled')
        confusing_nodes.append(v)

    # Add confusing edges
    confusing_edges = [(u, v) for u in G.nodes() for v in confusing_nodes if u != v]
    random.shuffle(confusing_edges)

    num_of_total_edges = G.number_of_edges() + num_of_necessary_vedges

    for e in confusing_edges:
        G.add_edge(*e, color='red')
        if G.number_of_edges() == num_of_total_edges:
            break

    return G


def main():
    curr_dir = sys.argv[1]
    time = sys.argv[2]

    # Generate a cert-cert graph
    ndtype = [('u', int), ('v', int), ('time', float)]
    filepath = '../edgelist/{}_accusation_list.txt'.format(curr_dir)

    events = genfromtxt(filepath, delimiter=' ', dtype=ndtype)

    G = nx.DiGraph()

    index = 1
    for i in xrange(0, len(events)/3, 60):
        H = nx.DiGraph()

        # Retrieve graph per minute
        edges = events[np.logical_and(events['time'] > i, events['time'] < (i+60))]
        if edges.size > 0:
            for e in edges:
                G.add_edge(e[0], e[1])
                H.add_edge(e[0], e[1])

            # Filename
            filename = '{}_{:0>4d}'.format(curr_dir, (i+60))

            # timeslot version
            saveGraph(H, filename, curr_dir)

            if timeslot == True: continue

            # Orignal graph
            saveGraph(G, filename, curr_dir)

            # Perturbation grpah
            G = method(G)
            saveGraph(G, filename, curr_dir)


if __name__ == '__main__':
    main()
