from graph_tool.all import Graph
from graph_tool.all import graph_draw
from graph_tool.all import load_graph

import os.path

# Draw the passed in sentence graph # TODO: make this comment more descriptive
def sentence_graph_draw(
        sentence_graph, 
        sentence,
        output_folder_name="sentence-graphs-visualization",
        output_file_name="sentence-graph-debug",
        file_extension=".png"):
    base_vertex_font_size = 128
    base_vertex_size = 200
    if len([x for x in sentence_graph.vertices()]) == 0:
        print("Empty sentence graph received, cannot draw, returning....")
        return
    max_in_degree = max([vertex.in_degree() for vertex in sentence_graph.vertices()])
    print("Max in degree in sentence graph is: %s" % str(max_in_degree))
    font_size_func =\
        lambda in_degree: 5 * min(128, max(32, (in_degree / max(1, max_in_degree))))

    vertex_font_size_property_map = sentence_graph.degree_property_map("in")
    for key in sentence_graph.vertices():
        vertex_font_size_property_map[key] =\
            font_size_func(vertex_font_size_property_map[key])
    vertex_size_property_map = sentence_graph.degree_property_map("in")
    for key in sentence_graph.vertices():
        vertex_size_property_map[key] =\
            base_vertex_size *\
                (vertex_size_property_map[key] / max(1, max_in_degree))

    output_file_name = output_file_name.replace("/", "-slash-")
    output_file_path = os.path.join(output_folder_name, output_file_name)
    shortened_output_file_path = output_file_path[:252]

    graph_draw(
        sentence_graph, 
        vertex_text=sentence_graph.vertex_properties["word"], 
        vertex_font_size=vertex_font_size_property_map,
        vertex_fill_color=sentence_graph.vertex_properties["vertex_color"],
        output_size=(20000, 20000), 
        output=shortened_output_file_path + file_extension)
    
def sentence_graph_file_path_from_sentence(
    sentence, 
    sentence_graphs_folder="sentence-graphs-storage",
    file_extension=".gt"):
    sentence = sentence.replace(" ", "-")
    sentence = sentence.replace("/", "-slash-")
    file_path = os.path.join(sentence_graphs_folder, sentence)
    shortened_file_path = file_path[:252]
    print("Returning sentence_graph_file_path_from_sentence as: %s" 
        % (shortened_file_path + file_extension))
    return shortened_file_path + file_extension

def save_sentence_graph_to_file(
        sentence_graph, output_file_path, file_format="gt"):
    sentence_graph.save(
        output_file_path,
        fmt=file_format)

def load_sentence_graph_from_file(input_file_path, file_format="gt"):
    try:
        return load_graph(input_file_path, fmt=file_format)
    except:
        return None
