from glob import glob
import os

import networkx as nx
import matplotlib.pyplot as plt

BLUE = "#99CCFF"
GREEN = "#77DD77"
COLOR = GREEN


def deletePng(dir):
    os.system('rm -f {}'.format(" ".join(glob(dir + '/*.png'))))


def deleteDot(dir):
    os.system('rm -f {}'.format(" ".join(glob(dir + '/*.dot'))))


def show(G):
    nx.draw(G, with_labels=True, node_color=COLOR, node_size=1200, alpha=0.4)
