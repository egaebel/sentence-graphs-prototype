from graph_tool import topology

from fake_definition_client import FakeDefinitionClient
from fake_sentence_parser import FakeSentenceParser
import unittest

# Need to add to python path to access src folder
import sys
sys.path.insert(1, "../src")
from sentence_graph import SentenceGraph
from sentence_graph_io import sentence_graph_draw
from sentence_graph_construction import build_deep_sentence_graph

# Need to add to python path to access parsey-mcparseface-service src folder
sys.path.insert(1, "../../parsey-mcparseface-service/src/")
from parse_tree_parser import ParseNode

PARAGRAPH = "The history of the universe is brief on the cosmic scale."\
    + "Many think this brevity to not be so, but on the cosmic calendar this becomes apparent."\
    + "The idea of the cosmic calendar was first conceived by Carl Sagan, I think so anyway."\
    + "The cosmic calendar was reused by Neil de Grasse Tyson in his remake of the Cosmos series."\
    + "Usually the cosmic calendar is featured as a huge 12 month calendar that the host is standing on, "\
        + "with all manner of cosmic phenomena printed on the calendar."

def create_simple_sentence_parse_tree(last_word):
    """
    Input: The word sentence
    Parse:
    word NN ROOT @2
     +-- The DT det @1
     +-- sentence NN dep @3

    """
    #ParseNode("sentence", "Noun", "root", 3, None, 0)
    root_node = ParseNode("word", "NN", "ROOT", 1, None, 0)
    root_node.add_child(ParseNode("the", "DT", "det", 0, root_node, 1))
    root_node .add_child(ParseNode(last_word, "NN", "dep", 2, root_node, 1))
    return root_node

SENTENCE_1 = "This is the first sentence."
"""
Input: This is the first sentence .
Parse:
sentence NN ROOT @5
 +-- This DT nsubj @1
 +-- is VBZ cop @2
 +-- the DT det @3
 +-- first JJ amod @4
 +-- . . punct @6

"""
SENTENCE_1_PARSE_TREE = ParseNode("sentence", "NN", "ROOT", 4, None, 0)
SENTENCE_1_PARSE_TREE\
        .add_child(ParseNode("This", "DT", "nsubj", 0, SENTENCE_1_PARSE_TREE, 1))\
        .add_child(ParseNode("is", "VBZ", "cop", 1, SENTENCE_1_PARSE_TREE, 1))\
        .add_child(ParseNode("the", "DT", "det", 2, SENTENCE_1_PARSE_TREE, 1))\
        .add_child(ParseNode("first", "JJ", "amod", 3, SENTENCE_1_PARSE_TREE, 1))
SENTENCE_1_DEFINITION_1 = "The word this."
SENTENCE_1_DEFINITION_2 = "The word is."
SENTENCE_1_DEFINITION_3 = "The word the."
SENTENCE_1_DEFINITION_4 = "The word first."
SENTENCE_1_DEFINITION_5 = "The word sentence."

fake_definition_client = FakeDefinitionClient()
# Sentence 1
fake_definition_client.set_definition("this", "Determiner", SENTENCE_1_DEFINITION_1)
fake_definition_client.set_definition("is", "Verb", SENTENCE_1_DEFINITION_2)
fake_definition_client.set_definition("the", "Determiner", SENTENCE_1_DEFINITION_3)
fake_definition_client.set_definition("first", "Adjective", SENTENCE_1_DEFINITION_4)
fake_definition_client.set_definition("sentence", "Noun", SENTENCE_1_DEFINITION_5)
# Sentence 2

fake_sentence_parser = FakeSentenceParser()
fake_sentence_parser.set_parse_tree(SENTENCE_1, SENTENCE_1_PARSE_TREE)
fake_sentence_parser.set_parse_tree(SENTENCE_1_DEFINITION_1, create_simple_sentence_parse_tree("this"))
fake_sentence_parser.set_parse_tree(SENTENCE_1_DEFINITION_2, create_simple_sentence_parse_tree("is"))
fake_sentence_parser.set_parse_tree(SENTENCE_1_DEFINITION_3, create_simple_sentence_parse_tree("the"))
fake_sentence_parser.set_parse_tree(SENTENCE_1_DEFINITION_4, create_simple_sentence_parse_tree("first"))
fake_sentence_parser.set_parse_tree(SENTENCE_1_DEFINITION_5, create_simple_sentence_parse_tree("sentence"))

class TestSentenceGraphConstruction(unittest.TestCase):
    def test_build_deep_sentence_graph(self):
        expected_sentence_graph = SentenceGraph(directed=False)
        this_vertex = expected_sentence_graph.add_vertex("this", "Determiner")
        is_vertex = expected_sentence_graph.add_vertex("is", "Verb")
        the_vertex = expected_sentence_graph.add_vertex("the", "Determiner")
        first_vertex = expected_sentence_graph.add_vertex("first", "Adjective")
        sentence_vertex = expected_sentence_graph.add_vertex("sentence", "Noun")
        sentence_vertices = [this_vertex, is_vertex, the_vertex, first_vertex, sentence_vertex]
        expected_sentence_graph.set_vertices_color(sentence_vertices)

        def_this_vertex = expected_sentence_graph.add_vertex("this", "Noun")
        def_is_vertex = expected_sentence_graph.add_vertex("is", "Noun")
        def_first_vertex = expected_sentence_graph.add_vertex("first", "Noun")
        def_word_vertex = expected_sentence_graph.add_vertex("word", "Noun")

        expected_sentence_graph.add_sentence_edges(sentence_vertices)
        expected_sentence_graph.add_sentence_edges([the_vertex, def_word_vertex, def_this_vertex])
        expected_sentence_graph.add_sentence_edges([def_word_vertex, def_is_vertex])
        expected_sentence_graph.add_sentence_edges([the_vertex, def_word_vertex, the_vertex])
        expected_sentence_graph.add_sentence_edges([def_word_vertex, def_first_vertex])
        expected_sentence_graph.add_sentence_edges([def_word_vertex, sentence_vertex])

        expected_sentence_graph.add_definition_edges(this_vertex, [the_vertex, def_word_vertex, def_this_vertex])
        expected_sentence_graph.add_definition_edges(is_vertex, [the_vertex, def_word_vertex, def_is_vertex])
        expected_sentence_graph.add_definition_edges(the_vertex, [def_word_vertex])
        expected_sentence_graph.add_definition_edges(first_vertex, [the_vertex, def_word_vertex, def_first_vertex])
        expected_sentence_graph.add_definition_edges(sentence_vertex, [the_vertex, def_word_vertex])

        sentence_graph = build_deep_sentence_graph(
            SENTENCE_1, 
            fake_definition_client, 
            fake_sentence_parser.fake_parse_sentence, 
            directed=False, 
            depth=2)

        """
        # Debugging help
        sentence_graph_draw(
            sentence_graph, SENTENCE_1, output_folder_name="debug-viz", output_file_name="actual-sentence-graph")
        sentence_graph_draw(
            expected_sentence_graph, SENTENCE_1, output_folder_name="debug-viz", output_file_name="expected-sentence-graph")
        """

        self.assertTrue(topology.isomorphism(sentence_graph.get_graph(), expected_sentence_graph.get_graph()))

if __name__ == '__main__':
    unittest.main()