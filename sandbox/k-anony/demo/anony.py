#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import shuffle

from numpy import genfromtxt
import numpy as np
import pandas as pd

NUMBER_OF_ACCUSED = 5
NUMBER_OF_K = 2
COLOR_OF_FAKE_NODE = "#01DF01"          # GREEN
COLOR_OF_FAKE_EDGE = "#2E64FE"          # BLUE
COLOR_OF_CONVICETED_NODE = "#FE2E2E"    # RED


with open('../dictionary', 'rb') as f:
    virtual_nodes = f.read().split(',')


def anonymize(G):
    """K-anonymization
    """
    convicted = []

    df = pd.DataFrame(getGraphData(G), columns=['node', 'degree', 'in_deg', 'out_deg'])
    conviction_nodes, non_anonymize_nodes = findNotKNodes(df)

    convicted += conviction_nodes
    while non_anonymize_nodes:
        node = non_anonymize_nodes.pop(0)
        # print "Processing Node {}".format(node)

        # Check non-anonymization nodes with unique degree
        conviction_tmp_nodes, non_anonymize_tmp_nodes = findNotKNodes(df)
        # print "% --->", non_anonymize_tmp_nodes
        convicted += conviction_tmp_nodes

        if node in non_anonymize_tmp_nodes:
            node_info = df[df.node == node].values[0].tolist()
            in_deg, out_deg = node_info[2], node_info[3]

            # Find the nodes with same in degree as well as smaller out degree with non-anonymization node
            cf = df[(df.in_deg == in_deg) & (df.out_deg < out_deg)]

            if not cf.empty:
                # Reverse sorting by nodes' out degree and retrieve their degree
                cf_degree = list(cf.sort('out_deg', ascending=False).degree.unique())
                cf_deg = cf_degree.pop(0)

                # Select the nodes with the highest degree
                cf_nodes = cf.node[cf.degree == cf_deg].values.tolist()

                shuffle(cf_nodes)
                if len(cf_nodes) >= (2 * NUMBER_OF_K - 1):
                    for i in range(NUMBER_OF_K - 1):
                        vertex = cf_nodes.pop(0)
                        G = add_noise(G, vertex, in_deg - cf_deg[0], out_deg - cf_deg[1], conviction_nodes)
                elif len(cf_nodes) > NUMBER_OF_K:
                    for i in range(len(cf_nodes) - NUMBER_OF_K):
                        vertex = cf_nodes.pop(0)
                        G = add_noise(G, vertex, in_deg - cf_deg[0], out_deg - cf_deg[1], conviction_nodes)
                    for i in range(2 * NUMBER_OF_K - 1 - len(cf_nodes)):
                        G = createNewNode(G, in_deg, out_deg, conviction_nodes)
                elif len(cf_nodes) <= NUMBER_OF_K:
                    for vertex in cf_nodes:
                        G = add_noise(G, vertex, in_deg - cf_deg[0], out_deg - cf_deg[1], conviction_nodes)
                        df = updateDataframe(G)
                    for i in range(NUMBER_OF_K - 1 - len(cf_nodes)):
                        G = createNewNode(G, in_deg, out_deg, conviction_nodes)
                else:
                    print "error"
            # No candidate node, so create new node
            else:
                for i in range(NUMBER_OF_K - 1):
                    G = createNewNode(G, in_deg, out_deg, conviction_nodes)
            # Update dataframe
            df = updateDataframe(G)
            conviction_nodes, non_anonymize_nodes = findNotKNodes(df)

    G = updateConvictedColor(G, list(set(convicted)))

    # test(G)
    # print df.degree.value_counts()
    return G


def getGraphData(G):
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


def updateDataframe(G):
    """Update dataframe based on current graph
    """
    return pd.DataFrame(getGraphData(G), columns=['node', 'degree', 'in_deg', 'out_deg'])


def findNotKDegree(df):
    """Find the unique degree from dataframe
    """
    return [k for k, v in dict(df).iteritems() if v < NUMBER_OF_K]


def findNotKNodes(df):
    """Find the nodes that do not staify K degree in the graph
    """
    NotKDegree = findNotKDegree(df.degree.value_counts())
    NotKDegree = sorted(NotKDegree, reverse=True)
    return nonAnonymizeNodes(df, NotKDegree)


def nonAnonymizeNodes(df, NotKDegree):
    """Return conviction nodes and non-anonymization nodes
    """
    non_anonymize_nodes = []
    conviction_nodes = []
    for i in NotKDegree:
        index = df.index[df['degree'] == i][0]
        node = df.loc[index]['node']
        if df.loc[index]['in_deg'] < NUMBER_OF_ACCUSED:
            non_anonymize_nodes.append(node)
        else:
            conviction_nodes.append(node)
    return conviction_nodes, non_anonymize_nodes


def getVertex2(conviction_nodes):
    """Get the end point from conviction nodes or virtual nodes pool
    """
    if conviction_nodes:
        return conviction_nodes.pop()
    else:
        return getVnodes()


def add_noise(G, vertex1, number_of_in_degs_need, number_of_out_degs_need, conviction_nodes):
    """Create required nodes and edges
    """
    for i in range(number_of_in_degs_need):
        vertex2 = getVnodes()
        # G.add_node(vertex1, color=COLOR_OF_FAKE_NODE, style='filled')
        G.add_node(vertex1)
        G.add_node(vertex2, color=COLOR_OF_FAKE_NODE, style='filled')
        G.add_edge(vertex2, vertex1, color=COLOR_OF_FAKE_EDGE)
        # print "add {} -> {}".format(vertex2, vertex1)

    for i in range(number_of_out_degs_need):
        vertex2 = getVertex2(conviction_nodes)
        while G.has_edge(vertex1, vertex2):
            vertex2 = getVertex2(conviction_nodes)
        # G.add_node(vertex1, color=COLOR_OF_FAKE_NODE, style='filled')
        G.add_node(vertex1)
        G.add_node(vertex2, color=COLOR_OF_FAKE_NODE, style='filled')
        G.add_edge(vertex1, vertex2, color=COLOR_OF_FAKE_EDGE)
        # print "add {} -> {}".format(vertex1, vertex2)
    # print
    return G


def add_noise1(G, vertex1, number_of_in_degs_need, number_of_out_degs_need, conviction_nodes):
    """Create required nodes and edges
    """
    for i in range(number_of_in_degs_need):
        vertex2 = getVnodes()
        G.add_node(vertex1, color=COLOR_OF_FAKE_NODE, style='filled')
        G.add_node(vertex2, color=COLOR_OF_FAKE_NODE, style='filled')
        G.add_edge(vertex2, vertex1, color=COLOR_OF_FAKE_EDGE)
        # print "add {} -> {}".format(vertex2, vertex1)

    for i in range(number_of_out_degs_need):
        vertex2 = getVertex2(conviction_nodes)
        while G.has_edge(vertex1, vertex2):
            vertex2 = getVertex2(conviction_nodes)
        G.add_node(vertex1, color=COLOR_OF_FAKE_NODE, style='filled')
        G.add_node(vertex2, color=COLOR_OF_FAKE_NODE, style='filled')
        G.add_edge(vertex1, vertex2, color=COLOR_OF_FAKE_EDGE)
        # print "add {} -> {}".format(vertex1, vertex2)
    # print
    return G


def updateConvictedColor(G, conviction_nodes):
    """Draw red color on conviction nodes
    """
    for i in conviction_nodes:
        G.add_node(i, color=COLOR_OF_CONVICETED_NODE, style='filled')
    return G


def createNewNode(G, in_deg, out_deg, conviction_nodes):
    """Create new node with particular degree
    """
    vertex = getVnodes()
    G = add_noise1(G, vertex, in_deg, out_deg, conviction_nodes)
    return G


def getVnodes():
    """Create virtual node
    """
    global virtual_nodes
    return virtual_nodes.pop(0)
