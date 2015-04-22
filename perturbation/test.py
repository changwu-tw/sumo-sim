# import pandas as pd

# s = pd.Series([1,2,3,4,5], index=["a","b","c","d","e"])

# print s.index.values
# print s.values

# # print s[3], s["d"]
# # print s[1:3]
# # print s['b':'d']

# # print list(s.iteritems())

# index = s.index
# # print index.__class__.mro()
# print index.values

# from random import randint
# print randint(0, 10000000)
# import random

# for i in range(100000):
#     if random.random() < 1e-7:
#         print "@@"

import networkx as nx

G = nx.Graph()

G.add_node(11, color='red')
G.add_node(11, color='blue')
G.add_edges_from([(1, 2), (31, 32), (10, 12)])
print G.nodes()
# for i in G.nodes():
    # print G.node(i)['color'] = 'red'
    # print G.node[i]
    # print dict(i)
    # print i['color']
print G.nodes(data=True)
