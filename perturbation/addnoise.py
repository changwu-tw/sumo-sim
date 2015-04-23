#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
NUMBER_OF_ACCUSED = 4
NUMBER_OF_K = 2
COLOR_OF_FAKE_NODE = "#01DF01"  # GREEN
COLOR_OF_FAKE_EDGE = "#2E64FE"  # BLUE
COLOR_OF_CONVICETED_NODE = "#FE2E2E"



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


def findUniqueDegree(hash):
    hash = OrderedDict(sorted(dict(hash).items(), reverse=True, key=lambda t: t[0]))
    return [k for k, v in hash.iteritems() if v == 1]


def getGraphData(G):
    nodes = G.nodes()
    in_degrees = []
    out_degrees = []
    for i in nodes:
        in_degrees.append(G.in_degree(i))
        out_degrees.append(G.out_degree(i))
    degrees = zip(in_degrees, out_degrees)
    return zip(*[nodes, degrees, in_degrees, out_degrees])


def uniqueNodes(df):
    uni_deg = findUniqueDegree(df['degree'].value_counts())
    conviction_nodes, non_anonymize_nodes = nonAnonymizeNodes(df, uni_deg)
    return conviction_nodes, non_anonymize_nodes


def nonAnonymizeNodes(df, unique_degree):
    non_anonymize_nodes = []
    conviction_nodes = []
    for i in unique_degree:
        index = df.index[df['degree'] == i][0]
        node = df.loc[index]['node']
        if df.loc[index]['in_deg'] < NUMBER_OF_ACCUSED:
            non_anonymize_nodes.append(node)
        else:
            print "@@"
            conviction_nodes.append(node)
    return conviction_nodes, non_anonymize_nodes


def getVertex2(conviction_nodes):
    if conviction_nodes:
        return conviction_nodes.pop()
    else:
        return getVnodes()


def add_noise(G, vertex1, number_of_in_degs_need, number_of_out_degs_need, conviction_nodes):
#######
    # print vertex1, number_of_in_degs_need, number_of_out_degs_need, conviction_nodes

    for i in range(number_of_in_degs_need):
#######
        # print "@@@ 5 @@@"
        vertex2 = getVnodes()
        G.add_node(vertex1, color=COLOR_OF_FAKE_NODE, style='filled')
        G.add_node(vertex2, color=COLOR_OF_FAKE_NODE, style='filled')
        G.add_edge(vertex2, vertex1, color=COLOR_OF_FAKE_EDGE)
#######
        print "{} ---> {}".format(vertex2, vertex1)

    for i in range(number_of_out_degs_need):

#######
        # print "@@@ 6 @@@"

        vertex2 = getVertex2(conviction_nodes)
        while G.has_edge(vertex1, vertex2):
            vertex2 = getVertex2(conviction_nodes)

        G.add_node(vertex1, color=COLOR_OF_FAKE_NODE, style='filled')
        G.add_node(vertex2, color=COLOR_OF_FAKE_NODE, style='filled')
        G.add_edge(vertex1, vertex2, color=COLOR_OF_FAKE_EDGE)

#######
        print "{} ---> {}".format(vertex1, vertex2)

    return G


def updateConvictedColor(G, conviction_nodes):
    for i in conviction_nodes:
        G.add_node(i, color=COLOR_OF_CONVICETED_NODE, style='filled')
    return G


def anonymize(G):
#######
    graphInfo(G)
#######
    convicted = []

    df = pd.DataFrame(getGraphData(G), columns=['node', 'degree', 'in_deg', 'out_deg'])

    unique_degree = findUniqueDegree(df['degree'].value_counts())
    conviction_nodes, non_anonymize_nodes = nonAnonymizeNodes(df, unique_degree)
    convicted += conviction_nodes
#######
    print 'conviction', conviction_nodes
    print 'anonymize', non_anonymize_nodes
#######

    for node in non_anonymize_nodes:
#######
        print 'node -->', node
        conviction_tmp_nodes, non_anonymize_tmp_nodes = uniqueNodes(df)
        convicted += conviction_tmp_nodes
        if node in non_anonymize_tmp_nodes:
            node_row = df[df['node'] == node].values[0]
            node, degree, in_deg, out_deg = node_row[0], node_row[1], node_row[2], node_row[3]
#######
            # print '處理 node', node
            # Find candidates
            candidates = df['node'][ (df['in_deg'] == in_deg) & (df['out_deg'] < out_deg) ].values.tolist()
#######
            # print "candidates --> ", candidates

            if candidates:
#######
                # print "@@@ 1 @@@"
                cf = df[ (df['in_deg'] == in_deg) & (df['out_deg'] < out_deg) ]
                cf_degree = cf.sort('out_deg', ascending=False).head(1)['degree'].values.tolist()[0]

                cf_nodes = df['node'][ df['degree'] == cf_degree].values.tolist()
                if len(cf_nodes) > NUMBER_OF_K:
#######
                    print "從過去的點挑一個"
                    # print "@@@ 3 @@@"
                    vertex = random.choice(cf_nodes)

                    G = add_noise(G, vertex, in_deg-cf_degree[0], out_deg-cf_degree[1], conviction_nodes)
                    df = updateDataframe(G)
                    # graphInfo(G)
                    # print "modify one"
                else:
                    for vertex in cf_nodes:
#######
                        print "K個點一起更新"
                        # print "@@@ 4 @@@"
                        G = add_noise(G, vertex, in_deg-cf_degree[0], out_deg-cf_degree[1], conviction_nodes)
                        df = updateDataframe(G)
                    # graphInfo(G)
#######
                    # print "modify multiple"

            else:
#######
                # print "@@@ 2 @@@"
                print "產生全新的點"
                vertex = getVnodes()
                G = add_noise(G, vertex, in_deg, out_deg, conviction_nodes)

                df = updateDataframe(G)
#######
                # print "create new one"
#######
    graphInfo(G)

    G = updateConvictedColor(G, list(set(convicted)))

    df = pd.DataFrame(getGraphData(G), columns=['node', 'degree', 'in_deg', 'out_deg'])
    unique_degree = findUniqueDegree(df['degree'].value_counts())
    conviction_nodes, non_anonymize_nodes = nonAnonymizeNodes(df, unique_degree)
    if non_anonymize_nodes:
        print "還有餘孽啊..@@"

    return G

def updateDataframe(G):
    return pd.DataFrame(getGraphData(G), columns=['node', 'degree', 'in_deg', 'out_deg'])


def main():
    curr_dir = sys.argv[1]
    # time = sys.argv[2]


    # Generate a cert-cert graph
    ndtype = [('u', int), ('v', int), ('time', float)]
    # filepath = '../edgelist/{}_accusation_list.txt'.format(curr_dir)
    filepath = '../edgelist/0423_0.5_{}_accusation_list.txt'.format(curr_dir)

    events = genfromtxt(filepath, delimiter=' ', dtype=ndtype)

    G = nx.DiGraph()

    index = 1
    # for i in xrange(0, len(events), 60):
    for i in xrange(0, 480, 60):
        # H = nx.DiGraph()

        # Retrieve graph per minute
        edges = events[np.logical_and(events['time'] > i, events['time'] < (i+60))].tolist()
        if len(edges) > 0:
            for e in edges:
                G.add_edge(e[0], e[1])
                # H.add_edge(e[0], e[1])

            # Filename
            filename = '{}_{:0>4d}'.format(curr_dir, (i+60))

            # timeslot version
            # saveGraph(H, filename, curr_dir)

            # if timeslot == True: continue

            # Orignal graph
            saveGraph(G, filename, curr_dir)

            print 'time:', i
            G = anonymize(G)

            saveGraph(G, filename, curr_dir)


if __name__ == '__main__':
    main()
