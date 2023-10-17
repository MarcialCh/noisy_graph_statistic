#!/usr/bin/env python
import networkx as nx
import os.path
from src.k_clique import baseline
from src.util.utils import induced_subgraph
from degree import degree
import time

pathhack = os.path.dirname(os.path.realpath(__file__))

network = nx.Graph()
ego_nodes = []


def load_edges():
    global network
    edge_file = open("D:/file/noisy_graph_statistic/src/email.txt", "r")
    for line in edge_file:
        # nodefrom nodeto
        split = [int(x) for x in line.split("\t")]
        node_from = split[0]
        node_to = split[1]
        network.add_node(node_from)
        network.add_node(node_to)
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



    k=3
    total = 0
    price_points = {}
    n = len(network.nodes)
    for node in network.nodes:
        price_points[node] = 1
    d = dict(nx.degree(network))
    print("average degree:", sum(d.values()) / len(network.nodes))
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
        total_price = degree.total_price_from_variance(network, 10 * variance, price_points, 1)
        print("%s:variance %f" % (variance, total_price / n))

   
    
    for data_proportion in range(1, 11):
        subgraph_node_num = int(0.1 * data_proportion * n)
        subgraph = induced_subgraph(network, subgraph_node_num)
        time_start = time.perf_counter()
        total_price = degree.total_price_from_variance(subgraph, 10, price_points, 10**3)
        #total_price = improve.total_price_from_variance(subgraph, 10, price_points, k, 10 ** 2, 1000)
        #total_price = two_phase.total_price_from_variance(subgraph, 10, price_points, k, 1)
        time_end = time.perf_counter()
        print("%s:data_proportion %f" % (data_proportion, time_end-time_start))
    '''
    for k_examine in range(3, 11):
        subgraph_node_num = n
        subgraph = induced_subgraph(network, subgraph_node_num)
        time_start = time.perf_counter()
        total_price = baseline.total_price_from_variance(subgraph, 10, price_points, k_examine, 10 ** 3)
        #total_price = improve.total_price_from_variance(subgraph, 10, price_points, k_examine, 10 ** 2, 1000)
        #total_price = two_phase.total_price_from_variance(subgraph, 10, price_points, k_examine, 1)
        time_end = time.perf_counter()
        print("%s:k %f" % (k_examine, time_end - time_start))
