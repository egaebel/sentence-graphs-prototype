from graph_tool.all import Graph
from graph_tool.all import graph_draw
from graph_tool.all import load_graph

# Takes a list of sentence graphs, finds the common vertices between them and
# returns a list of copies of the sentence graphs with all the common vertices 
# removed, with the exception of sentence vertices that are part of the base 
# sentence that the sentence graph was constructed from
def reduce_sentence_graphs(sentence_graphs, reduction_threshold=0.7):
    print("sentence_graphs: %s" % str(sentence_graphs))
    sentence_graph_words = dict(
        _get_word_pos_tuples_from_sentence_graph(sentence_graphs[0]))
    print("\n\nsentence_graph_words (after creation):")
    print(sentence_graph_words)
    for i in range(1, len(sentence_graphs)):
        sentence_graph = sentence_graphs[i]
        for word_pos_count_tuple in _get_word_pos_tuples_from_sentence_graph(sentence_graph):
            if word_pos_count_tuple[0] in sentence_graph_words:
                sentence_graph_words[word_pos_count_tuple[0]] += 1
            else:
                sentence_graph_words[word_pos_count_tuple[0]] = 1

    print("\n\nsentence graph words (after tallying):")
    print(sentence_graph_words)

    for word_pos_tuple in sentence_graph_words.keys():
        if sentence_graph_words[word_pos_tuple] / len(sentence_graphs) >= 0.7:
            print("Removing word_pos_tuple from sentence_graph_words: %s" 
                % str(word_pos_tuple))
            del sentence_graph_words[word_pos_tuple]

    print("\n\nsentence graph words (after deletions):")
    print(sentence_graph_words)

    print("\n\n")
    reduced_sentence_graphs = []
    for sentence_graph in sentence_graphs:
        reduced_sentence_graph = sentence_graph.copy()

        print("iterating over edges in original: %s" % str([x for x in sentence_graph.edges()]))        
        for vertex in reversed(sorted([x for x in sentence_graph.vertices()])):
            word =\
                sentence_graph.vertex_properties["word"][vertex]
            part_of_speech =\
                sentence_graph.vertex_properties["part_of_speech"][vertex]
            print("Iterating on: %s" % str((word, part_of_speech)))
            # TODO: don't remove sentence vertices
            if (word, part_of_speech) not in sentence_graph_words:
                # TODO: Remove the vertices, after verifying when it is useful, maybe make this a parameter
                #reduced_sentence_graph.clear_vertex(vertex)
                _remove_edges_with_vertex(sentence_graph, reduced_sentence_graph, vertex)
                reduced_sentence_graph.remove_vertex(vertex)
                # sentence_graph.vertex_properties["vertex_color"][vertex] = [1, 1, 0, 0]
                print("Removed: %s" % str((word, part_of_speech)))
            print("iterating over edges: %s" % str([x for x in reduced_sentence_graph.edges()]))

        reduced_sentence_graphs.append(reduced_sentence_graph)

        print("iterating over edges: %s" % str([x for x in reduced_sentence_graph.edges()]))
        print("reduced sentence graph %s" % str(reduced_sentence_graph))
        for edge in reduced_sentence_graph.edges():
            print("Reduced sentence_graph edge: %s" % str(edge))
        print("\n\n")


    return reduced_sentence_graphs

def _remove_edges_with_vertex(basis_sentence_graph, sentence_graph, vertex):
    print("_remove_Edges sentence graph before: %s" % sentence_graph)
    print("Out edges:")
    for edge in basis_sentence_graph.get_out_edges(vertex):
        print((basis_sentence_graph.edge(edge[0], edge[1])))
        sentence_graph.remove_edge((basis_sentence_graph.edge(edge[0], edge[1])))
        sentence_graph.remove_edge((basis_sentence_graph.edge(edge[1], edge[0])))
    print("After reduced graph out edges: %s" % str([sentence_graph.edge(edge[0], edge[1]) for edge in sentence_graph.get_out_edges(vertex)]))
    print("In edges:")
    for edge in basis_sentence_graph.get_in_edges(vertex):
        print((basis_sentence_graph.edge(edge[0], edge[1])))
        sentence_graph.remove_edge((basis_sentence_graph.edge(edge[0], edge[1])))
    print("_remove_Edges sentence graph after: %s" % sentence_graph)

def _get_word_pos_tuples_from_sentence_graph(sentence_graph):
    return [((sentence_graph.vertex_properties["word"][x], 
        sentence_graph.vertex_properties["part_of_speech"][x]), 1)
            for x in sentence_graph.vertices()]