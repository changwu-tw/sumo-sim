#!/usr/bin/env python

import itertools
import math
import os
import random
import sys
sys.path.append('../..')

from collections import Counter
from collections import OrderedDict
from datetime import datetime
from random import choice

import networkx as nx
import numpy as np
from numpy import genfromtxt
import pandas as pd

from sumo_sim import helper

# 18728 words
with open('dictionary', 'rb') as f:
    virtual_nodes = f.read().split(',')


percentage = 0.2
index = 0
timeslot = False
NUMBER_OF_ACCUSED = 5
NUMBER_OF_K = 2


def memoize(f):
    cache = {}
    return lambda *args: cache[args] if args in cache else cache.update({args: f(*args)}) or cache[args]


def getVnodes():
    global virtual_nodes
    return virtual_nodes.pop(0)


def saveGraph(G, filename, dir):
    global index
    index += 1
    helper.saveToDotGraph(G, '{}/{:0>3d}_{}'.format(dir, index, filename))


def graphInfo(G):
    helper.draw_table(G)
    # helper.graph_info(G)


def method1(G):
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


def K_anonymize(G):
#######
    graphInfo(G)

    degrees = zip(G.in_degree().values(), G.out_degree().values())

    df = pd.DataFrame(data=zip(G.nodes(), degrees), columns=['id', 'deg'])
    d = dict(df['deg'].value_counts())
#######
    print d

    depressed_nodes = []
    processed_nodes = []
    for k, v in d.iteritems():
        if v == 1:
            node_id = df[df['deg'] == k].id.values[0]
            # print node_id
            ix = G.nodes().index(node_id)
            in_deg_num = G.in_degree().values()[ix]

            if in_deg_num <= NUMBER_OF_ACCUSED:
                processed_nodes.append(ix)
            else:
                depressed_nodes.append(G.nodes()[ix])
#######
    print "--" * 20
    print depressed_nodes
    print processed_nodes

    for nix in processed_nodes:
        vertex1 = getVnodes()

        in_deg_num = G.in_degree().values()[nix]
        out_deg_num = G.out_degree().values()[nix]

        for in_deg in range(in_deg_num):
            vertex2 = getVnodes()
            G.add_node(vertex1, color='blue', style='filled')
            G.add_node(vertex2, color='blue', style='filled')
            G.add_edge(vertex2, vertex1, color='green')
#######
            print "{} ---> {}".format(vertex2, vertex1)

        for out_deg in range(out_deg_num):
            try:
                vertex2 = depressed_nodes.pop()
            except:
                vertex2 =getVnodes()

            G.add_node(vertex1, color='blue', style='filled')
            G.add_node(vertex2, color='blue', style='filled')
            G.add_edge(vertex1, vertex2, color='green')
#######
            print "{} ---> {}".format(vertex1, vertex2)

    graphInfo(G)

    return G


def anonymize(G):
#######
    graphInfo(G)

    degrees = zip(G.in_degree().values(), G.out_degree().values())
    nodes = G.nodes()
    degree_table = dict(zip(nodes, degrees))

    # Sorting degree_table by degree
    sorted_table = OrderedDict()
    for k in sorted(degree_table, key=degree_table.get):
        sorted_table[k] = degree_table[k]
        print '{:3} -> {:6}'.format(k, degree_table[k])

    """
    Nodes need to be anonymized
    unique_degree & in degree is larger than a particular threshold
    """
    unique_degree = [k for k, v in Counter(sorted_table.values()).iteritems() if v == 1]
    non_anonymize_nodes = []
    conviction_nodes = []
    for deg in reversed(unique_degree):
        for k, v in sorted_table.iteritems():
            if deg == v:
                if deg[0] <= NUMBER_OF_ACCUSED:
                    non_anonymize_nodes.append(k)
                else:
                    conviction_nodes.append(k)
#######
    print 'conviction', conviction_nodes

    for anony in non_anonymize_nodes:
        vertex1 = anony
        in_deg, out_deg = sorted_table[vertex1]
#######
#Determine case by case

#######
        print 'non_anonymize', anony
        print '[IN, OUT] = [{}, {}]'.format(in_deg, out_deg)

        # Search weather there is same in_degree within existing nodes
        best_case = []
        # second_case = []
        worst_case = []
        for deg in sorted_table.values():
            # best case
            if deg[0] == in_deg and deg[1] < out_deg:
                best_case.append(deg)
            # second case
            # elif deg[0] < in_deg and deg[1] < out_deg:
                # second_case.append(deg)
            # worst case
            elif in_deg == 0 and deg[0] == 0 and deg[1] <= out_deg:
                worst_case.append(deg)

        b_checked = [k for k, v in Counter(best_case).iteritems() if v > NUMBER_OF_K]
        w_checked = [k for k, v in Counter(worst_case).iteritems() if v > NUMBER_OF_K]
        if best_case and b_checked:
            print 'Best'
            print Counter(best_case)
            b_node = b_checked[-1]
            print in_deg-b_node[0], out_deg-b_node[1]
            add_noise(G, vertex1, in_deg-b_node[0], out_deg-b_node[1], conviction_nodes)

            print "create best case"
            continue

        # if second_case:
        #     print 'Second'
        #     print Counter(second_case)

        elif worst_case and w_checked:
            print 'worst'
            print Counter(worst_case)
            w_node = w_checked[-1]
            print in_deg-w_node[0], out_deg-w_node[1]
            add_noise(G, vertex1, in_deg-w_node[0], out_deg-w_node[1], conviction_nodes)
            print "create worst case"
            continue

        else:
            vertex1 = getVnodes()
            add_noise(G, vertex1, in_deg, out_deg, conviction_nodes)
            print "create new one"


#######
    graphInfo(G)


    degrees = zip(G.in_degree().values(), G.out_degree().values())
    nodes = G.nodes()
    degree_table = dict(zip(nodes, degrees))

    # Sorting degree_table by degree
    sorted_table = OrderedDict()
    for k in sorted(degree_table, key=degree_table.get):
        sorted_table[k] = degree_table[k]
        # print '{:3} -> {:6}'.format(k, degree_table[k])

    """
    Nodes need to be anonymized
    unique_degree & in degree is larger than a particular threshold
    """
    unique_degree = [k for k, v in Counter(sorted_table.values()).iteritems() if v == 1]
    non_anonymize_nodes = []
    conviction_nodes = []
    for deg in unique_degree:
        for k, v in sorted_table.iteritems():
            if deg == v:
                if deg[0] <= NUMBER_OF_ACCUSED:
                    non_anonymize_nodes.append(k)
                else:
                    conviction_nodes.append(k)
#######
    a = [anony for anony in non_anonymize_nodes]
    if conviction_nodes and a:
        "==anothere round=="
        anonymize(G)

    return G





def add_noise(G, vertex1, number_of_in_degs_need, number_of_out_degs_need, conviction_nodes):
    for i in range(number_of_in_degs_need):
        vertex2 = getVnodes()
        # print vertex1, vertex2
        G.add_node(vertex1, color='blue', style='filled')
        G.add_node(vertex2, color='blue', style='filled')
        G.add_edge(vertex2, vertex1, color='green')
#######
        print "{} ---> {}".format(vertex2, vertex1)

    for i in range(number_of_out_degs_need):
        try:
            vertex2 = conviction_nodes.pop()
        except:
            vertex2 = getVnodes()
        # print vertex1, vertex2
        G.add_node(vertex1, color='blue', style='filled')
        G.add_node(vertex2, color='blue', style='filled')
        G.add_edge(vertex1, vertex2, color='green')
#######
        print "{} ---> {}".format(vertex1, vertex2)
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
    for i in xrange(0, len(events)/4, 20):
    # for i in xrange(0, 720, 60):
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
            # saveGraph(H, filename, curr_dir)

            if timeslot == True: continue

            # Orignal graph
            saveGraph(G, filename, curr_dir)

            if i == 120:
                break

            G = anonymize(G)
            saveGraph(G, filename, curr_dir)



#######################################
########## Perturbation grpah #########
            # G = method1(G)
            # saveGraph(G, filename, curr_dir)


if __name__ == '__main__':
    main()
