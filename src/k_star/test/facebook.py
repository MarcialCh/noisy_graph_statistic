#!/usr/bin/env python
import time

import networkx as nx
import numpy as np
import glob
import os, os.path

from k_star import baseline
from k_star import upper
from src.util.utils import C, induced_subgraph

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
    k = 3
    n = len(network.nodes)

    price_points = {}
    for node in network.nodes:
        price_points[node] = 1


    # Exp-1: Accuracy influenced by privacy budget.
    for epsilon in range(-6, 4):
        node_degree = dict(nx.degree(network))
        unperturbed_star_num = {}
        perturbed_total = 0.0
        total = 0
        for node, unperturbed_degree in node_degree.items():
            unperturbed_star_num[node] = C(unperturbed_degree, k - 1)
            total += unperturbed_star_num[node]
        #perturbed_answer = baseline.total_num_from_privacy_budget(unperturbed_star_num, 10 ** epsilon, k)
        perturbed_answer = upper.total_num_from_privacy_budget(network, unperturbed_star_num, 10**epsilon, k)
        accuracy = 1 - abs(perturbed_answer - total) / abs(perturbed_answer + total)
        print("%s:total" % (total))
        print("%s:accuracy %f" % (epsilon, accuracy))
    

    # Exp-2: Impact of payment on variance.
    for variance in range(1, 6):
        total_price = baseline.total_price_from_variance(network, 40 * variance, price_points, k, 5* 10 ** 3)
        #total_price = upper.total_price_from_variance(network, 40 * variance, price_points, k, 5* 10 ** 3, 1000)
        print("%s:variance %f" % (variance, total_price / n))



    # Exp-4: Running Time    
    for data_proportion in range(1, 11):
        subgraph_node_num = int(0.1 * data_proportion * n)
        subgraph = induced_subgraph(network, subgraph_node_num)
        time_start = time.perf_counter()
        #total_price = baseline.total_price_from_variance(subgraph, 40, price_points, k, 10**3)
        total_price = upper.total_price_from_variance(subgraph, 40, price_points, k, 10 ** 3, 1000)
        time_end = time.perf_counter()
        print("%s:data_proportion %f" % (data_proportion, time_end-time_start))

    for k_examine in range(2, 11):
        subgraph_node_num = n
        subgraph = induced_subgraph(network, subgraph_node_num)
        time_start = time.perf_counter()
        #total_price = baseline.total_price_from_variance(subgraph, 40, price_points, k_examine, 10**3)
        total_price = upper.total_price_from_variance(subgraph, 40, price_points, k_examine, 1)
        time_end = time.perf_counter()
        print("%s:k %f" % (k_examine, time_end - time_start))
