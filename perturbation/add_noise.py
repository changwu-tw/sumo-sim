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


def getVnodes():
    global virtual_nodes
    return virtual_nodes.pop(0)


def saveGraph(G, current, index, dir):
    # Save graph to gml
    nx.write_gml(G, '{}/{}_{}.gml'.format(dir, index, current))

    # Save graph to png
    helper.saveToDotGraph(G, '{}/{}_{}'.format(dir, index, current))


def graphInfo(G):
    helper.draw_table(G)
    helper.graph_info(G)


def method(G):
    num_of_necessary_vnodes = (int)(math.ceil(G.number_of_nodes()*percentage))
    num_of_necessary_vedges = (int)(math.ceil(G.number_of_edges()*percentage))

    """
    Add confusing nodes
    """
    # print 'Add confusing nodes'

    nodelist = G.nodes()
    random.shuffle(nodelist)

    confusing_nodes = []
    for u in nodelist[:num_of_necessary_vnodes]:
        v = getVnodes()
        G.add_edge(u, v, color='green')
        G.add_node(v, color='blue', style='filled')
        confusing_nodes.append(v)

    """
    Add confusing edges
    """
    # print 'Add confusing edges'

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

    H = nx.DiGraph()
    I = nx.DiGraph()

    for i in xrange(0, len(events), 60):
        # Orignal subgraph
        G = nx.DiGraph()
        edges = events[np.logical_and(events['time'] > i, events['time'] < (i+60))]
        for e in edges:
            G.add_edge(e[0], e[1])
        current = '{}_{:0>4d}_{:0>4d}'.format(curr_dir, i, (i+60))
        # saveGraph(G, current, '1', curr_dir)

        H.add_edges_from(G.edges())
        saveGraph(H, 'merge_'+current, '1', curr_dir)

        # Perturbation graph
        # G = method(G)
        # saveGraph(G, current, '2', curr_dir)

        I = method(H)
        saveGraph(I, 'merge_'+current, '2', curr_dir)



    # np.select[events['time'] > 0, events['time'] < 60]

    # # G = nx.DiGraph()
    # for row in rows:
    #     print row[2]




    # G = nx.DiGraph()
    # edges = genfromtxt(filepath, delimiter=' ', dtype=ndtype)
    # for e in edges:
    #     G.add_edge(e[0], e[1])

    # # filename
    # if not os.path.exists(curr_dir):
    #     os.makedirs(curr_dir)

    # current = '{}_{}'.format(curr_dir, time)
    # # current = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

    # saveGraph(G, current, '1', curr_dir)


    # # Perturbation
    # G = method(G)
    # saveGraph(G, current, '2', curr_dir)


if __name__ == '__main__':
    main()
