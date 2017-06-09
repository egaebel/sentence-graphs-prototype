from graph_tool.all import cairo_draw
from graph_tool.all import graph_draw
from graph_tool.all import graphviz_draw
from graph_tool.all import load_graph

from sentence_graph import SentenceGraph

import os.path

def cairo_sentence_graph_draw(
        sentence_graph, 
        sentence,
        output_folder_name="sentence-graphs-visualization",
        output_file_name="sentence-graph-debug",
        file_extension=".png",
        base_vertex_size=25,
        base_vertex_font_size=25):
    output_file_name = output_file_name.replace("/", "-slash-")
    output_file_path = os.path.join(output_folder_name, output_file_name)
    shortened_output_file_path = output_file_path[:252]

def graphviz_sentence_graph_draw(
        sentence_graph, 
        sentence,
        output_folder_name="sentence-graphs-visualization",
        output_file_name="sentence-graph-debug",
        file_extension=".png",
        base_vertex_size=25,
        base_vertex_font_size=25):
    output_file_name = output_file_name.replace("/", "-slash-")
    output_file_path = os.path.join(output_folder_name, output_file_name)
    shortened_output_file_path = output_file_path[:252]

    graphviz_draw(
        sentence_graph.get_graph(), 
        size=(50000, 50000), 
        output=shortened_output_file_path + "--graphviz" + file_extension,
        #vertex_text=sentence_graph.get_word_vertex_properties(), 
        vsize=base_vertex_size,
        #vertex_font_size=base_vertex_font_size,#vertex_font_size_property_map,
        output_format='png')#,
        #vcolor=sentence_graph.get_color_vertex_properties(),
        #ecolor=sentence_graph.get_color_edge_properties())    

# Draw the passed in sentence graph # TODO: make this comment more descriptive
def sentence_graph_draw(
        sentence_graph, 
        sentence,
        output_folder_name="sentence-graphs-visualization",
        output_file_name="sentence-graph-debug",
        file_extension=".png",
        kcore=None,
        base_vertex_size=25,
        base_vertex_font_size=25):
    #base_vertex_font_size = 20#128
    #base_vertex_size = 100#200
    if len(sentence_graph.get_vertices()) == 0:
        print("Empty sentence graph received, cannot draw, returning....")
        return
    """
    # Out_degree counts all edges when a graph is undirected
    max_out_degree = max(map(lambda v: v.out_degree(), sentence_graph.get_vertices()))
    font_size_func =\
        lambda out_degree: 5 * min(128, max(32, (out_degree / max(1, max_out_degree))))

    vertex_font_size_property_map = sentence_graph.get_degree_properties("out")
    for key in sentence_graph.get_vertices():
        vertex_font_size_property_map[key] =\
            font_size_func(vertex_font_size_property_map[key])
    vertex_size_property_map = sentence_graph.get_degree_properties("out")
    for key in sentence_graph.get_vertices():
        vertex_size_property_map[key] =\
            base_vertex_size *\
                (vertex_size_property_map[key] / max(1, max_out_degree))
    """

    output_file_name = output_file_name.replace("/", "-slash-")
    output_file_path = os.path.join(output_folder_name, output_file_name)
    shortened_output_file_path = output_file_path[:252]

    graph_draw(
        sentence_graph.get_graph(), 
        output_size=(20000, 20000), 
        output=shortened_output_file_path + file_extension,
        vertex_text=sentence_graph.get_word_vertex_properties(), 
        vertex_size=base_vertex_size,
        vertex_font_size=base_vertex_font_size,#vertex_font_size_property_map,
        vertex_fill_color=sentence_graph.get_color_vertex_properties(),
        edge_color=sentence_graph.get_color_edge_properties())
    
def sentence_graph_file_path_from_sentence(
    sentence, 
    sentence_graphs_folder="sentence-graphs-storage",
    file_extension=".gt"):
    sentence = sentence.replace(" ", "-")
    sentence = sentence.replace("/", "-slash-")
    file_path = os.path.join(sentence_graphs_folder, sentence)
    shortened_file_path = file_path[:252]
    return shortened_file_path + file_extension

def save_sentence_graph_to_file(sentence_graph, output_file_path, file_format="gt"):
    sentence_graph.get_graph().save(output_file_path, fmt=file_format)

def load_sentence_graph_from_file(input_file_path, sentence, file_format="gt"):
    try:
        loaded_graph = load_graph(input_file_path, fmt=file_format)
        print("Loaded graph: |%s|" % loaded_graph)
        if loaded_graph is not None and loaded_graph.num_vertices() != 0:
            return SentenceGraph(sentence=sentence, graph=loaded_graph)
        else:
            print("ERROR: Sentence graph loaded is: %s and is either None or has 0 vertices!"
                % load_graph)
    except Exception, e:
        print("ERROR: Cannot load sentence graph in file format: %s from file path: %s,"
            " due to exception:\n%s\nThis is normal if caching is being relied on." 
            % (file_format, input_file_path, e))
    return None
