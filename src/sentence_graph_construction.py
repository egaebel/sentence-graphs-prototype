from graph_tool.all import Graph
from graph_tool.all import graph_draw
from graph_tool.all import load_graph

from sentence_graph_io import sentence_graph_draw
from wiktionary_utilities import lookup_definition_on_wiktionary

from multiprocessing import Manager
import sys

# Use functions from parsey-mcparseface-service
sys.path.insert(1, "../../parsey-mcparseface-service/src/")
from run_parsey import run_parsey
from parse_tree_parser import parse_ascii_tree

PARSEY_PART_OF_SPEECH_TO_WIKTIONARY_MAP = {
    'CC': 'Conjunction',
    'CD': 'Cardinal number',
    'DT': 'Determiner',
    'EX': 'Existential there',
    'IN': 'Preposition',
    'JJ': 'Adjective',
    'JJR': 'Adjective',
    'JJS': 'Adjective',
    'LS': 'List item marker',
    'MD': 'Modal',
    'NN': 'Noun',
    'NNS': 'Noun',
    'NNP': 'Proper noun',
    'NNPS': 'Proper noun',
    'PDT': 'Predeterminer',
    'POS': 'Possessive ending',
    'PRP': 'Pronoun',
    'PRP$': 'Pronoun',
    'RB': 'Adverb',
    'RBR': 'Adverb',
    'RBS': 'Adverb',
    'RP': 'Particle',
    'SYM': 'Symbol',
    'TO': 'To',
    'UH': 'Interjection',
    'VB': 'Verb',
    'VBD': 'Verb',
    'VBG': 'Verb',
    'VBN': 'Verb',
    'VBP': 'Verb',
    'VBZ': 'Verb',
    'WDT': 'Determiner',
    'WP': 'Pronoun',
    'WP$': 'Pronoun',
    'WRB': 'Adverb',
}

################################################################################
####################-----Sentence Graph Building Functions-----#################
################################################################################

# Takes some body of text, splits it into sentences, constructs sentence
# graphs for every sentence, and returns a list of all the sentence graphs.
def get_text_sentence_graphs(text, wiktionary_client, directed=False):
    sentence_graphs = []
    for sentence in text.split("."):
        if sentence.strip() == "":
            continue
        sentence_graphs.append(build_deep_sentence_graph(sentence, wiktionary_client))
    return sentence_graphs

def create_sentence_graph():
    pass

# Take a string sentence and recursively build a sentence graph by looking up 
# the definition of each word and adding an edge from each word to the graph of 
# the sentence defining the word. Perform this process recursively and if a word
# that already exists in the graph is encountered then add an edge to that 
# pre-existing word instead of diving deep again.
#
# Eventually this process should stop....
# If it proves unreasonably long-running, then set a depth limit or something 
# similar
#
# Return the deep sentence graph
def build_deep_sentence_graph(
        sentence,
        wiktionary_client, 
        directed=False,
        depth=2):
    sentence_graph = Graph(directed=directed)
    
    # Vertex properties
    word_property = sentence_graph.new_vertex_property("string")
    part_of_speech_property = sentence_graph.new_vertex_property("string")
    word_pos_tuple_property = sentence_graph.new_vertex_property("object")
    vertex_color_property = sentence_graph.new_vertex_property("vector<double>")
    sentence_graph.vertex_properties["word"] = word_property
    sentence_graph.vertex_properties["part_of_speech"] = part_of_speech_property
    sentence_graph.vertex_properties["vertex_color"] = vertex_color_property

    # Edge properties
    sentence_edge_property = sentence_graph.new_edge_property("string")
    definition_edge_property = sentence_graph.new_edge_property("string")
    sentence_graph.edge_properties["sentence_edge"] = sentence_edge_property
    sentence_graph.edge_properties["definition_edge"] = definition_edge_property

    word_pos_to_vertex_index_mapping = dict()

    first_sentence_vertices = _build_deep_sentence_graph_helper(
        sentence, 
        sentence_graph, 
        word_pos_to_vertex_index_mapping,
        wiktionary_client,
        directed,
        depth)

    print("Setting base sentence coloring.....")
    for word_vertex in first_sentence_vertices:
        print("Processing word_vertex: %s" % 
            sentence_graph.vertex_properties["word"][word_vertex])
        sentence_graph.vertex_properties["vertex_color"][word_vertex] =\
            [1, 0, 0, 1]

    return sentence_graph

def _build_deep_sentence_graph_helper(
        sentence,
        sentence_graph,
        word_pos_to_vertex_index_mapping,
        wiktionary_client, 
        directed,
        depth):
    if depth is not None:
        if depth == 0:
            return []
        depth -= 1

    print("DEBUG*****: Building deep sentence graph on sentence: %s" % sentence)
    sentence = sentence.replace(".", "").lower().strip()
    sentence_vertices = []
    # Parse with ParseyMcParseface to obtain parts of speech tagging
    sentence_parse_tree = parse_ascii_tree(run_parsey(sentence))
    if sentence_parse_tree is None:
        print(
            "\n\nERROR: sentence_parse_tree from parse_ascii_tree is None for"
            " sentence:\n %s\n\n" % sentence)
        return []

    prev_word_vertex = None
    for parse_node in sentence_parse_tree.to_sentence_order():

        word = parse_node.word
        try:
            part_of_speech =\
                PARSEY_PART_OF_SPEECH_TO_WIKTIONARY_MAP[parse_node.part_of_speech]
        except:
            continue

        word_pos_tuple = (word, part_of_speech)
        if word_pos_tuple in word_pos_to_vertex_index_mapping:
            # Set word_vertex to the previously found vertex
            word_vertex_index = word_pos_to_vertex_index_mapping[word_pos_tuple]
            word_vertex = sentence_graph.vertex(word_vertex_index)
        else:
            # Create vertex, set properties
            word_vertex = sentence_graph.add_vertex()
            sentence_graph.vertex_properties["word"][word_vertex] = word
            sentence_graph.vertex_properties["part_of_speech"][word_vertex] =\
                part_of_speech
            sentence_graph.vertex_properties["vertex_color"][word_vertex] =\
                [0, 0, 1, 1]
            word_pos_to_vertex_index_mapping[word_pos_tuple] =\
                sentence_graph.vertex_index[word_vertex]

            if depth != 0:
                # Get definition, add pointer from word to all words in definition
                definition = wiktionary_client.lookup_definition_on_wiktionary(word, part_of_speech)

                if definition.strip() != '':
                    # Get definition of definitions
                    definition_word_vertices = _build_deep_sentence_graph_helper(
                        definition,
                        sentence_graph, 
                        word_pos_to_vertex_index_mapping,
                        wiktionary_client, 
                        directed,
                        depth)

                    # Add edges from the word_vertex to all definition vertices and set 
                    # the definition edge property on each edge
                    for definition_word_vertex in definition_word_vertices:
                        definition_edge = sentence_graph.add_edge(
                            word_vertex, definition_word_vertex)
                        sentence_graph.edge_properties["definition_edge"][definition_edge] =\
                            definition_edge
                else:
                    print("\n\nERROR: definition not found for:\nword: %s\n"
                        "part of speech:%s\n\n\n" % (word, part_of_speech))
                    failure_file = open("failed-definition-lookups/%s-%s" % (word, part_of_speech), 'w')
                    failure_file.write("word: %s\npart of speech:%s\n" % (word, part_of_speech))
                    failure_file.close()

        sentence_vertices.append(word_vertex)

        # Add sentence edge and set sentence edge property on edge
        if prev_word_vertex is not None:
            sentence_edge = sentence_graph.add_edge(
                prev_word_vertex, word_vertex)
            sentence_graph.edge_properties["sentence_edge"][sentence_edge] =\
                sentence_edge
        prev_word_vertex = word_vertex

    return sentence_vertices

# Take a sentence in some form and generate a graph
# edges are built up using word order
#
# Return graph of sentence
def generate_linear_sentence_graph(sentence, directed=False):
    words = sentence.split(" ")
    
    sentence_graph = Graph(directed=directed)
    word_vertices = sentence_graph.add_vertex(len(words))
    word_property = sentence_graph.new_vertex_property("string")
    sentence_graph.vertex_properties["word"] = word_property
    for word_vertex, word in zip(word_vertices, words):
        word_property[word_vertex] = word
    sentence_graph.add_edge_list([(i - 1, i) for i in range(1, len(words))])

    # DEBUG
    sentence_graph_draw(
        sentence_graph, sentence, "linear-sentence-graph-debug.png")


################################################################################
####################-------------------Tests-------------------#################
################################################################################

def tests():
    pass

if __name__ == '__main__':
    tests()