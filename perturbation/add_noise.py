#!/usr/bin/env python

import itertools
import logging
import math
import random

import sys
sys.path.append('../..')

from datetime import datetime
from random import choice

import networkx as nx
from numpy import genfromtxt

from sumo_sim import helper

# 18728 words
with open('dictionary', 'rb') as f:
    virtual_nodes = f.read().split(',')

percentage = 0.2

logging.basicConfig(level=logging.INFO)
# logging.basicConfig(filename='run.log',level=logging.DEBUG)
# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def getVnodes():
    global virtual_nodes
    return virtual_nodes.pop(0)


def saveGraph(G, current, index):
    # Save graph to gml
    nx.write_gml(G, '{}_{}.gml'.format(index, current))

    # Save graph to png
    helper.saveToDotGraph(G, '{}_{}'.format(index, current))


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


def test():
    import timeit
    print(timeit.timeit('main()',
        setup='from __main__ import main', number=100))


def info():
    G = nx.read_gml('1_2015-03-10-21-53-54.gml')
    graphInfo(G)
    G = nx.read_gml('2_2015-03-10-21-53-54.gml')
    graphInfo(G)


def main():
    curr_dir = sys.argv[1]
    time = sys.argv[2]

    # Generate a cert-cert graph
    # G = helper.vehicle_accusation_graph(20, 0.1)
    ndtype = [('a', int), ('b', int), ('c', float)]

    filepath = '../edgelist/{}_accusation_list.txt'.format(curr_dir)

    G = nx.DiGraph()
    edges = genfromtxt(filepath, delimiter=' ', dtype=ndtype)
    for e in edges:
        if e[0] != e[1]:
            G.add_edge(e[0], e[1])

    # For filename
    current = '{}_{}'.format(curr_dir, time)
    # current = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

    # print 'Generate a new cert-cert graph'
    saveGraph(G, current, '1')
    # graphInfo(G)

    G = method(G)
    saveGraph(G, current, '2')
    # graphInfo(G)


if __name__ == '__main__':
    main()
    # info()
    # test()
