import networkx as nx
from itertools import combinations, permutations
import random
import matplotlib.pyplot as plt

def random_degree_sequence_graph(sequence, seed=None, tries=10):
    DSRG = DegreeSequenceRandomGraph(sequence, seed=seed)
    for try_n in range(tries):
        try:
            return DSRG.generate()
        except nx.NetworkXUnfeasible:
            pass
    raise nx.NetworkXError('failed to generate graph in %d tries' % tries)


class DegreeSequenceRandomGraph(object):
    def __init__(self, degree, seed=None):
        if not nx.is_valid_degree_sequence(degree):
            raise nx.NetworkXUnfeasible('degree sequence is not graphical')
        if seed is not None:
            random.seed(seed)
        self.degree = list(degree)
        # node labels are integers 0,...,n-1
        self.m = sum(self.degree)/2.0 # number of edges
        try:
            self.dmax = max(self.degree) # maximum degree
        except ValueError:
            self.dmax = 0

    def generate(self):
        # remaining_degree is mapping from int->remaining degree
        self.remaining_degree = dict(enumerate(self.degree))

        # add all nodes to make sure we get isolated nodes
        self.graph = nx.Graph()
        self.graph.add_nodes_from(self.remaining_degree)

        # remove zero degree nodes
        for n, d in list(self.remaining_degree.items()):
            if d == 0:
                del self.remaining_degree[n]

        if len(self.remaining_degree) > 0:
            # build graph in three phases according to how many unmatched edges
            self.phase1()
            self.phase2()
            self.phase3()
        return self.graph

    def update_remaining(self, u, v, aux_graph=None):
        # decrement remaining nodes, modify auxilliary graph if in phase3
        if aux_graph is not None:
            # remove edges from auxilliary graph
            aux_graph.remove_edge(u,v)
        if self.remaining_degree[u] == 1:
            del self.remaining_degree[u]
            if aux_graph is not None:
                aux_graph.remove_node(u)
        else:
            self.remaining_degree[u] -= 1
        if self.remaining_degree[v] == 1:
            del self.remaining_degree[v]
            if aux_graph is not None:
                aux_graph.remove_node(v)
        else:
            self.remaining_degree[v] -= 1

    def p(self,u,v):
        # degree probability
        return 1 - self.degree[u]*self.degree[v]/(4.0*self.m)

    def q(self,u,v):
        # remaining degree probability
        norm = float(max(self.remaining_degree.values()))**2
        return self.remaining_degree[u]*self.remaining_degree[v]/norm

    def suitable_edge(self):
        # Check if there is a suitable edge that is not in the graph
        # True if an (arbitrary) remaining node has at least one possible
        # connection to another remaining node
        nodes = iter(self.remaining_degree)

        u = next(nodes) # one arbitrary node

        for v in nodes: # loop over all other remaining nodes
            print u, v
            if not self.graph.has_edge(u, v):
                return True
        exit(0)
        return False

    def phase1(self):
        # choose node pairs from (degree) weighted distribution
        # print sum(self.remaining_degree.values()) >= 2 * self.dmax**2
        while sum(self.remaining_degree.values()) >= 2 * self.dmax**2:
            u,v = sorted(random_weighted_sample(self.remaining_degree, 2))
            if self.graph.has_edge(u,v):
                continue
            if random.random() < self.p(u,v):  # accept edge
                self.graph.add_edge(u,v)
                self.update_remaining(u,v)

    def phase2(self):
        # choose remaining nodes uniformly at random and use rejection sampling
        while len(self.remaining_degree) >= 2 * self.dmax:
            norm = float(max(self.remaining_degree.values()))**2
            while True:
                u,v = sorted(random.sample(self.remaining_degree.keys(), 2))
                if self.graph.has_edge(u,v):
                    continue
                if random.random() < self.q(u,v):
                    break
            if random.random() < self.p(u,v):  # accept edge
                self.graph.add_edge(u,v)
                self.update_remaining(u,v)

    def phase3(self):
        # build potential remaining edges and choose with rejection sampling
        potential_edges = combinations(self.remaining_degree, 2)
        # build auxilliary graph of potential edges not already in graph

        # t = []
        # for (u, v) in potential_edges:
        #     if not self.graph.has_edge(u, v):
        #         t.append((u, v))
        # print t
        # exit(0)

        H = nx.Graph([(u, v) for (u, v) in potential_edges
                      if not self.graph.has_edge(u, v)])

        # nx.draw_graphviz(H, with_labels=True, node_size=800, alpha=0.5)
        # plt.show()
        # exit(0)

        while self.remaining_degree:
            if not self.suitable_edge():
                raise nx.NetworkXUnfeasible('no suitable edges left')

            while True:
                u, v = sorted(random.choice(H.edges()))
                if random.random() < self.q(u, v):
                    break
            if random.random() < self.p(u, v):  # accept edge
                self.graph.add_edge(u, v)
                self.update_remaining(u, v, aux_graph=H)

print random_degree_sequence_graph([0, 1, 2, 2, 3], seed=None, tries=10)
