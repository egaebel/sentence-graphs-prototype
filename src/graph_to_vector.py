from sentence_graph import SentenceGraph

from scipy import optimize
import numpy as np

import random

INFINITY = np.iinfo(np.int32).max
DUMMY_VERTEX_VALUE = "___"

NODE_COST_MULTIPLIER = 1
COST_NODE_REPLACEMENT = 2 * NODE_COST_MULTIPLIER
COST_NODE_INSERTION = 1 * NODE_COST_MULTIPLIER
COST_NODE_DELETION = 1 * NODE_COST_MULTIPLIER

EDGE_COST_MULTIPLIER = 1
COST_EDGE_REPLACEMENT = 2 * EDGE_COST_MULTIPLIER
COST_EDGE_INSERTION = 1 * EDGE_COST_MULTIPLIER
COST_EDGE_DELETION = 1 * EDGE_COST_MULTIPLIER

def astar_sentence_graph_edit_distance(graph1, graph2):
    pass
    # Iterate over each word-pos
    #   # Iterate over each edge 
    #       # create neighbor graph
    #       # check cost of graph

def _graph_cost_heuristic(graph1, graph2):
    pass

def _sentence_graph_vertex_cost(
        sentence_graph1_word_pos_tuples, 
        sentence_graph2_word_pos_tuples, 
        i, 
        j):
    """
    Note that sentence_graph1_word_pos_tuples is assumed to have all word-pos tuples in the 
    same order as sentence_graph2_word_pos_tuples so that indices can be reasonably used for
    the cost matrix.

    Cost matrix structure:
    TODO
    """
    N = len(sentence_graph1_word_pos_tuples)
    M = len(sentence_graph2_word_pos_tuples)

    if i >= N and j >= M:
        return 0
    elif i < N and j >= M:
        if i == (j - M):
            return COST_NODE_DELETION
        else:
            return INFINITY
    elif i >= N and j < M:
        if (i - N) == j:
            return COST_NODE_INSERTION
        else:
            return INFINITY
    else:
        if sentence_graph1_word_pos_tuples[i] == sentence_graph2_word_pos_tuples[j]:
            return 0
        else:
            return COST_NODE_REPLACEMENT

def _sentence_graph_compute_edge_cost(
        sentence_graph1, 
        sentence_graph2, 
        sentence_graph1_word_pos_tuples, 
        sentence_graph2_word_pos_tuples, 
        i, 
        j):
    N_nodes = len(sentence_graph1_word_pos_tuples)
    M_nodes = len(sentence_graph2_word_pos_tuples)

    if i < N_nodes:
        vertex1 = sentence_graph1.get_vertex(
            sentence_graph1_word_pos_tuples[i][0], sentence_graph1_word_pos_tuples[i][1])
        neighbor_word_pos_tuples1 =\
            sentence_graph1.get_vertex_out_neighbor_word_pos_tuples(vertex1)\
            + sentence_graph1.get_vertex_in_neighbor_word_pos_tuples(vertex1)
        neighbor_word_pos_tuples1 = sorted(neighbor_word_pos_tuples1, key=lambda x: x[0] + x[1])

    if j < M_nodes:
        vertex2 = sentence_graph2.get_vertex(
            sentence_graph2_word_pos_tuples[j][0], sentence_graph2_word_pos_tuples[j][1])
        neighbor_word_pos_tuples2 =\
            sentence_graph2.get_vertex_out_neighbor_word_pos_tuples(vertex2)\
            + sentence_graph2.get_vertex_in_neighbor_word_pos_tuples(vertex2)
        neighbor_word_pos_tuples2 = sorted(neighbor_word_pos_tuples2, key=lambda x: x[0] + x[1])

    if i >= N_nodes and j >= M_nodes:
        return 0
    elif i < N_nodes and j >= M_nodes:
        if i == (j - M_nodes):
            return COST_EDGE_DELETION * len(neighbor_word_pos_tuples1)
        else:
            return INFINITY
    elif i >= N_nodes and j < M_nodes:
        if (i - N_nodes) == j:
            return COST_EDGE_INSERTION * len(neighbor_word_pos_tuples2)
        else:
            return INFINITY

    N_M = len(neighbor_word_pos_tuples1) + len(neighbor_word_pos_tuples2)

    cost_matrix = np.zeros((N_M, N_M))
    for i in range(N_M):
        for j in range(N_M):
            cost_matrix[i, j] = _sentence_graph_edge_cost(
                neighbor_word_pos_tuples1, 
                neighbor_word_pos_tuples2, 
                i, 
                j)

    row_indices, col_indices = optimize.linear_sum_assignment(cost_matrix)

    return cost_matrix[row_indices, col_indices].sum()


def _sentence_graph_edge_cost(
        neighbor_word_pos_tuples1, 
        neighbor_word_pos_tuples2, 
        i, 
        j):
    N = len(neighbor_word_pos_tuples1)
    M = len(neighbor_word_pos_tuples2)

    if i >= N and j >= M:
        return 0
    elif i < N and j >= M:
        if i == (j - M):
            return COST_EDGE_DELETION
        else:
            return INFINITY
    elif i >= N and j < M:
        if (i - N) == j:
            return COST_EDGE_INSERTION
        else:
            return INFINITY
    else:
        if neighbor_word_pos_tuples1[i] == neighbor_word_pos_tuples2[j]:
            return 0
        else:
            return COST_EDGE_REPLACEMENT

def approximate_sentence_graph_edit_distance(sentence_graph1, sentence_graph2):
    return approximate_graph_edit_distance(
        sentence_graph1, 
        sentence_graph2, 
        vertex_cost_func=_sentence_graph_vertex_cost,
        compute_edge_cost_func=_sentence_graph_compute_edge_cost)

def approximate_graph_edit_distance(
        sentence_graph1, 
        sentence_graph2,
        vertex_cost_func=_sentence_graph_vertex_cost,
        compute_edge_cost_func=_sentence_graph_compute_edge_cost):
    print("Approximating graph edit distance....")
    # Copy graphs
    sentence_graph1_copy = sentence_graph1.copy()
    sentence_graph2_copy = sentence_graph2.copy()

    sentence_graph1_word_pos_tuples = sorted(sentence_graph1_copy.get_word_pos_tuples(), key=lambda x: x[0] + x[1])
    sentence_graph2_word_pos_tuples = sorted(sentence_graph2_copy.get_word_pos_tuples(), key=lambda x: x[0] + x[1])

    N_M = sentence_graph1_copy.get_num_vertices() + sentence_graph2_copy.get_num_vertices()

    # Construct node cost matrix
    print("Constructing cost matrix of size %d....." % N_M)
    cost_matrix = np.zeros((N_M, N_M))
    for i in range(N_M):
        for j in range(N_M):
            # numpy indexes by row, column
            cost_matrix[i, j] =(
                vertex_cost_func(
                    sentence_graph1_word_pos_tuples, 
                    sentence_graph2_word_pos_tuples, 
                    i, 
                    j) 
                + compute_edge_cost_func(
                    sentence_graph1_copy, 
                    sentence_graph2_copy, 
                    sentence_graph1_word_pos_tuples, 
                    sentence_graph2_word_pos_tuples, 
                    i, 
                    j))
    print("Cost matrix constructed!")

    # Run the Hungarian algorithm on cost matrix
    print("Running Hungarian algorithm.....")
    row_indices, col_indices = optimize.linear_sum_assignment(cost_matrix)
    print("Finished running Hungarian algorithm!")

    # Use resulting cost matrix to determine the graph edit distance
    return cost_matrix[row_indices, col_indices].sum()

def select_prototype_graphs(graphs, dimensions):
    if len(graphs) <= dimensions:
        return graphs, [x for x in range(len(graphs))]
    # TODO: Make this actually be smart and not just select randomly
    prototype_graphs = dict()
    for i in range(dimensions):
        random_index = random.randint(0, len(graphs) - 1)
        while random_index in prototype_graphs:
            random_index = random.randint(0, len(graphs) - 1)
        prototype_graphs[random_index] = graphs[random_index]
    return prototype_graphs.values(), prototype_graphs.keys()

def sentence_graph_dissimilarity_embedding(
        sentence_graph, 
        prototype_sentence_graphs, 
        graph_edit_distance_func=approximate_sentence_graph_edit_distance):
    dissimilarity_vector = list()
    for prototype_sentence_graph in prototype_sentence_graphs:
        dissimilarity_vector.append(graph_edit_distance_func(sentence_graph, prototype_sentence_graph))
    return dissimilarity_vector

if __name__ == '__main__':
    sentence1 = "I went to a fantastic university."
    sentence2 = "I attended a great college."

    graph1 = None
    graph2 = None
    approximate_sentence_graph_edit_distance(graph1, graph2)