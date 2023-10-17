import math
from src.util.utils import C, compute_price

from numpy.random import laplace


def total_num_from_privacy_budget(numbers, epsilon, k):
    star_num = 0.0
    total_node_num = len(numbers)
    for node, num in numbers.items():
        global_sensitivity = 2 * C(total_node_num - 1, k - 1)
        variance = 2 * pow(global_sensitivity / epsilon, 2)
        star_num += num + laplace(scale=math.sqrt(variance / 2))
    return star_num


def total_price_from_variance(graph, variance, price_points, k, b):
    total_price = 0.0
    total_node_num = len(graph.nodes)
    for node in graph.nodes:
        global_sensitivity = k * C(total_node_num - 1, k - 1)
        epsilon = global_sensitivity / pow(variance / 2, 0.5)
        total_price += compute_price(price_points[node], epsilon, b)
    return total_price
