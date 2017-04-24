# Takes a list of sentence graphs, finds the common vertices between them and
# returns a list of copies of the sentence graphs with all the common vertices 
# removed, with the exception of sentence vertices that are part of the base 
# sentence that the sentence graph was constructed from
def reduce_sentence_graphs(sentence_graphs, reduction_threshold=0.7):
    word_pos_count_tuples = [
        (word_pos_tuple, 1) for word_pos_tuple in sentence_graphs[0].get_word_pos_tuples()]
    sentence_graph_words = dict(word_pos_count_tuples)
    for i in range(1, len(sentence_graphs)):
        sentence_graph = sentence_graphs[i]
        for word_pos_tuple in sentence_graph.get_word_pos_tuples():
            if word_pos_tuple in sentence_graph_words:
                sentence_graph_words[word_pos_tuple] += 1
            else:
                sentence_graph_words[word_pos_tuple] = 1

    for word_pos_tuple in sentence_graph_words.keys():
        if sentence_graph_words[word_pos_tuple] / len(sentence_graphs) >= reduction_threshold:
            del sentence_graph_words[word_pos_tuple]

    reduced_sentence_graphs = []
    for sentence_graph in sentence_graphs:
        reduced_sentence_graph = sentence_graph.copy()

        for vertex in reversed(sorted(sentence_graph.get_vertices())):
            word = sentence_graph.get_word_vertex_properties()[vertex]
            part_of_speech = sentence_graph.get_pos_vertex_properties()[vertex]
            if (word, part_of_speech) not in sentence_graph_words:
                # TODO: Remove the vertices, after verifying when it is useful, 
                # maybe make this a parameter
                reduced_sentence_graph.remove_vertex(vertex)
                # TODO: don't remove sentence vertices, color them instead
                # sentence_graph.vertex_properties["vertex_color"][vertex] = [1, 1, 0, 0]

        reduced_sentence_graphs.append(reduced_sentence_graph)

    return reduced_sentence_graphs