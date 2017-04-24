from graph_tool import draw
from graph_tool import inference
from graph_tool import topology

MAX_VALUE = 2147483647
MAX_PATH_LENGTH = 3
MAX_PLOT_SIZE = 20000

def minimize_blockmodel_and_draw(sentence_graph):
    """
    block_state = inference.minimize_blockmodel_dl(sentence_graph.get_graph(), verbose=True)
    print("Drawing block model.....")
    block_state.draw(
        vertex_text=sentence_graph.get_word_vertex_properties(), 
        output_size=(MAX_PLOT_SIZE, MAX_PLOT_SIZE), 
        output="block-model-viz/test-1--directed.png")
    #"""
    #"""
    nested_block_state = inference.minimize_nested_blockmodel_dl(sentence_graph.get_graph(), verbose=True)
    print("Drawing hierarchical block model.....")
    draw.draw_hierarchy(
        nested_block_state, 
        vertex_text=sentence_graph.get_word_vertex_properties(), 
        output_size=(MAX_PLOT_SIZE, MAX_PLOT_SIZE), 
        output="block-model-viz/hierarchy-test-1.png")
    #"""

def similarity_test(sentence_graph_1, sentence_graph_2):
    similarity = topology.similarity(sentence_graph_1.get_graph(), sentence_graph_2.get_graph())
    print("Similarity: %s" % str(similarity))

def statistics_experiments(sentence_graphs):

    sentence_graph = sentence_graphs[0]
    print("sentence_graph graph: %s" % str(sentence_graph.get_graph()))
    
    shortest_paths = dict()
    for vertex_1 in sentence_graph.get_vertices():
        for vertex_2 in sentence_graph.get_vertices():
            if vertex_1 == vertex_2:
                continue

            all_shortest_paths_iterator  = topology.all_shortest_paths(sentence_graph.get_graph(), vertex_1, vertex_2) 
            #print("Iterating on path from %s to %s" % (sentence_graph.get_word_pos_tuple(vertex_1), sentence_graph.get_word_pos_tuple(vertex_2)))
            #print("all_shortest_paths_iterator: %s" % str(all_shortest_paths_iterator))
            saved_shortest_paths = []
            for shortest_path in all_shortest_paths_iterator:
                #print("shortest_path: %s" % str(shortest_path))
                shortest_path_length = 0
                for shortest_path_vertex_index in shortest_path:
                    #print("word_pos_tuple: %s" % str(sentence_graph.get_word_pos_tuple_by_index(shortest_path_vertex_index)))
                    shortest_path_length += 1
                if shortest_path_length <= MAX_PATH_LENGTH:
                    saved_shortest_paths.append(shortest_path.copy())

            if len(saved_shortest_paths) > 0:
                shortest_paths[(vertex_1, vertex_2)] = saved_shortest_paths

    print("\n\n\n=========================\n\n\n")
    for vertex_tuple, saved_shortest_paths in shortest_paths.items():
        vertex_1 = vertex_tuple[0]
        vertex_2 = vertex_tuple[1]
        print("Iterating on paths from %s to %s" % (sentence_graph.get_word_pos_tuple(vertex_1), sentence_graph.get_word_pos_tuple(vertex_2)))
        for saved_shortest_path in saved_shortest_paths:
            print("Path: %s" % str(saved_shortest_path))
            for shortest_path_vertex_index in saved_shortest_path:
                print("word_pos_tuple: %s" % str(sentence_graph.get_word_pos_tuple_by_index(shortest_path_vertex_index)))
            


    """ 
    for vertex in sentence_graph.get_vertices():
        result = shortest_paths_vertex_property_map[vertex]
        word, pos = sentence_graph.get_word_pos_tuple(vertex)
        print("word: %s, pos: %s: %s" % (word, pos, str(result)))
        for i in range(len(result)):
            print("result[%d] = %s" % (i, result[i]))
        print("")
        print("adjacent words: %s" % str(sentence_graph.get_vertex_out_neighbor_word_pos_tuples(vertex)))
    """

        #TODO I would really like to have something in sentence_graph to use here
        # something that gets all adjacent vertex words given a word