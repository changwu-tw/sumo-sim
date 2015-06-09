import networkx as nx


def main():
    G = nx.DiGraph()
    G.add_edges_from([(2, 1), (3, 1)])

    H = nx.DiGraph()
    H.add_edges_from([('B', 'A'), ('C', 'A')])

    print nx.is_isomorphic(G, H)


if __name__ == '__main__':
    main()
