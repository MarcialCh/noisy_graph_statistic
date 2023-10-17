import networkx as nx
from src.util.utils import C, compute_price, perturb_mechanism
from numpy.random import laplace
import math


def upper_local_sensitivity_mapping(graph, epsilon_0, k):
    upper_local_sensitivity = {}
    degree = dict(nx.degree(graph))
    for node in graph.nodes:
        perturbed_degree = perturb_mechanism(degree[node], scale=2 / epsilon_0)
        neighbor_max_degree = 0
        for neighbor in graph[node]:
            neighbor_max_degree = max(neighbor_max_degree, degree[neighbor])
        perturbed_neighbor_degree = perturb_mechanism(neighbor_max_degree, scale=2 / epsilon_0)
        upper_local_sensitivity[node] = C(perturbed_degree, k - 1) + C(perturbed_neighbor_degree, k - 1)
    return upper_local_sensitivity


def total_num_from_privacy_budget(graph, numbers, epsilon, k, alpha=0.1):
    star_num = 0.0
    # initial privacy budget for local sensitivity
    epsilon_0 = alpha * epsilon
    upper_local_sensitivity = upper_local_sensitivity_mapping(graph, epsilon_0, k)
    for node, num in numbers.items():
        variance = 2 * pow(upper_local_sensitivity[node] / ((1 - alpha) * epsilon), 2)
        star_num += num + laplace(scale=math.sqrt(variance / 2))
    return star_num


def total_price_from_variance(graph, variance, price_points, k, b, alpha=0.1):
    total_price = 0.0
    epsilon_0 = alpha / math.sqrt(variance / 2)
    upper_local_sensitivity = upper_local_sensitivity_mapping(graph, epsilon_0, k)
    for node in graph.nodes():
        epsilon = upper_local_sensitivity[node] / pow(variance / 2, 0.5)
        total_price += compute_price(price_points[node], epsilon + epsilon_0, b)
    return total_price
