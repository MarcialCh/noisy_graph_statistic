#!/usr/bin/env python
import time

import networkx as nx
import numpy as np
import glob
import os, os.path

from degree import degree
from k_star import upper
from src.util.utils import k_cliques, induced_subgraph

pathhack = os.path.dirname(os.path.realpath(__file__))

feat_file_name = "%s/feature_map.txt" % (pathhack,)
feature_index = {}  # numeric index to name
inverted_feature_index = {}  # name to numeric index
network = nx.Graph()
ego_nodes = []


def parse_featname_line(line):
    line = line[(line.find(' ')) + 1:]  # chop first field
    split = line.split(';')
    name = ';'.join(split[:-1])  # feature name
    index = int(split[-1].split(" ")[-1])  # feature index
    return index, name







def load_edges():
    global network
    edge_file = open("D:/file/noisy_graph_statistic/src/facebook_combined.txt", "r")
    for line in edge_file:
        # nodefrom nodeto
        split = [int(x) for x in line.split(" ")]
        node_from = split[0]
        node_to = split[1]
        network.add_edge(node_from, node_to)


def load_network():
    """
    Load the network.  After calling this function, facebook.network points to a networkx object for the facebook data.

    """
    load_edges()


def feature_matrix():
    n_nodes = network.number_of_nodes()
    n_features = len(feature_index)

    X = np.zeros((n_nodes, n_features))
    for i, node in enumerate(network.nodes()):
        X[i, :] = network.nodes[node]['features']

    return X


def universal_feature(feature_index):
    """
    Does every node have this feature?

    """
    return len([x for x in network.nodes() if network.nodes[x]['feautures'][feature_index] > 0]) // network.order() == 1


if __name__ == '__main__':
    print("Running tests.")
    print("Loading network...")
    load_network()
    print("done.")

    failures = 0


    def Ftest(actual, expected, test_name):
        global failures  # lol python scope
        try:
            print("testing %s..." % (test_name,))
            assert actual == expected, "%s failed (%s != %s)!" % (test_name, actual, expected)
            print("%s passed (%s == %s)." % (test_name, actual, expected))
        except AssertionError as e:
            print(e)
            failures += 1


    Ftest(network.order(), 4039, "order")
    Ftest(network.size(), 88234, "size")
    Ftest(round(nx.average_clustering(network), 4), 0.6055, "clustering")
    k= 3
    total = 0
    n = len(network.nodes)

    price_points = {}
    for node in network.nodes:
        price_points[node] = 1
    '''
    # Exp-1: Accuracy influenced by privacy budget.
    for epsilon in range(-6, 4):
        node_degree = dict(nx.degree(network))
        perturbed_answer = degree.total_num_from_privacy_budget(node_degree, 10 ** epsilon)
        total = 0
        for unperturbed_degree in node_degree.values():
            total += unperturbed_degree
        accuracy = 1 - abs(perturbed_answer - total) / abs(perturbed_answer + total)
        print("%s:accuracy %f" % (epsilon, accuracy))

    # Exp-2: Impact of payment on variance.
    for variance in range(1, 6):
        total_price = degree.total_price_from_variance(network, 40 * variance, price_points, 1)
        print("%s:variance %f" % (variance, total_price / n))



    
    for data_proportion in range(1, 11):
        subgraph_node_num = int(0.1 * data_proportion * n)
        subgraph = induced_subgraph(network, subgraph_node_num)
        time_start = time.perf_counter()
        total_price = degree.total_price_from_variance(subgraph, 40, price_points, 10**3)
        time_end = time.perf_counter()
        print("%s:data_proportion %f" % (data_proportion, time_end-time_start))
    '''
