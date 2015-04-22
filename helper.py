import itertools
import os
import random

from datetime import datetime

import matplotlib.pyplot as plt
import networkx as nx
import scipy as sp

from networkx.algorithms import bipartite
from networkx.generators.classic import complete_graph


def vehicle_accusation_graph(n, p, seed=None, directed=True):
    """Return a random vehicle accusation graph G_{n,p}.

    Chooses each of the possible edges with accusation probability p.

    Parameters
    ----------
    n : int
        The number of vehicles.
    p : float
        Probability for accusation.
    seed : int, optional
        Seed for random number generator (default=None).
    directed : bool, optional (default=True)
        If True return a directed graph
    """

    if directed:
        G=nx.DiGraph()
    else:
        G=nx.Graph()
    G.add_nodes_from(range(n))
    G.name='Vehicle_accusation_graph({}, {})'.format(n, p)
    if p<=0:
        return G
    if p>=1:
        return complete_graph(n,create_using=G)

    if not seed is None:
        random.seed(seed)

    if G.is_directed():
        edges=itertools.permutations(range(n),2)
    else:
        edges=itertools.combinations(range(n),2)

    for e in edges:
        if random.random() < p:
            G.add_edge(*e)

    """
    Remove all isolates in the graph & relabel the nodes of the graph
    """
    if nx.isolates(G):
        G.remove_nodes_from(nx.isolates(G))
        mapping = dict(zip(G.nodes(), range(G.number_of_nodes())))
        G = nx.relabel_nodes(G, mapping)

    return G


def draw_bipartite_graph(G):
    group_1, group_2 = bipartite.sets(G)

    pos = {x:(0 , float(i % 20) * 2) for i, x in enumerate(group_1)}
    pos.update({node: (18.3, 0 + float(i % 20) * 2) for i, node in enumerate(group_2)})
    nx.draw(G, pos, node_color='m', node_size=800, with_labels=True, width=1.3, alpha=0.4)


def saveToDotGraph(G, filename):
    """
    Save a graph to a PNG file.

    Parameters
    ----------
    G : graph

    filename : string

    """

    dotname = filename + '.dot'
    nx.write_dot(G, dotname)
    pngname = filename + '.png'

    # cmd = 'dot -n -Tpng {} > {}'.format(dotname, pngname)
    cmd = 'sfdp -x -Goverlap=prism -Tpng {} > {}'.format(dotname, pngname)

    # cmd = 'sfdp -x -Goverlap=scale -Tpng {} > {}'.format(dotname, pngname)
    if os.system(cmd) == 0:
        cmd = 'rm -f {}'.format(dotname)
        os.system(cmd)


def saveToNxGraph(G, filename):
    fig = plt.figure()
    plt.title(G.name)
    # pos = nx.spring_layout(G)
    pos = nx.graphviz_layout(G, prog='twopi', root=0)
    nx.draw(G, pos, node_color='b', node_size=800, with_labels=True, width=1.3, alpha=0.4)
    fig.savefig(filename)
    print 'Save to {}'.format(filename)



def draw_table(G):
    in_deg = []
    out_deg = []

    for i in G.nodes():
        in_deg.append(G.in_degree(i))
        out_deg.append(G.out_degree(i))

    in_degrees = ['[I]'] + in_deg
    out_degrees = ['[O]'] + out_deg
    degrees = ['[T]'] + [x + y for x, y in zip(in_deg, out_deg)]

    output = '{:^4}' * (nx.number_of_nodes(G)+1)

    print output.format(*(['Node'] + G.nodes()))
    print '-' * 4 * (nx.number_of_nodes(G)+1)
    print output.format(*in_degrees)
    print output.format(*out_degrees)
    print '-' * 4 * (nx.number_of_nodes(G)+1)
    print output.format(*degrees)
    print


def adjacency_matrix(G):
    A = nx.adjacency_matrix(G)
    print A.todense()
    print


def graph_info(G):
    nnodes=G.number_of_nodes()
    degree_sequence=nx.degree(G).values()
    freqs = {}
    for degree in degree_sequence:
        freqs[degree] = freqs.get(degree, 0) + 1

    print 'Name: {}'.format(G.name)
    print 'Type: {}'.format(', '.join([type(G).__name__]))
    print '#nodes: {}'.format(nnodes)
    print '#edges: {}'.format(G.number_of_edges())
    print 'degree sequence: {}'.format(degree_sequence)
    print 'degree frequency: {}'.format(freqs)
    print 'nodes: ' + ', '.join(str(i) for i in G.nodes())
    print 'edges: ' + ', '.join(str(i) for i in G.edges())
    print


def findNodesInDegreeIsEqualZero(G):
    l = []
    for node, degree in G.in_degree_iter():
        if degree == 0:
            l.append(node)
    return l
