from graph_tool.all import Graph

import unittest

# Need to add to python path to access src folder
import sys
sys.path.insert(1, "../src")
from sentence_graph import SentenceGraph

WORD_1 = "word-1"
POS_1 = "pos-1"
WORD_2 = "word-2"
POS_2 = "pos-2"
WORD_3 = "word-3"
POS_3 = "pos-3"
WORD_4 = "word-4"
POS_4 = "pos-4"
WORD_5 = "word-5"
POS_5 = "pos-5"
WORD_6 = "word-6"
POS_6 = "pos-6"

class TestSentenceGraph(unittest.TestCase):
    def test_add_vertex(self):
        sentence_graph = SentenceGraph()
        vertex_1 = sentence_graph.add_vertex(WORD_1, POS_1)
        vertex_2 = sentence_graph.add_vertex(WORD_2, POS_2)
        vertex_3 = sentence_graph.add_vertex(WORD_3, POS_3)
        vertex_4 = sentence_graph.add_vertex(WORD_4, POS_4)

        self.assertEqual(sentence_graph.get_vertex(WORD_1, POS_1), vertex_1)
        self.assertEqual(sentence_graph.get_vertex(WORD_2, POS_2), vertex_2)
        self.assertEqual(sentence_graph.get_vertex(WORD_3, POS_3), vertex_3)
        self.assertEqual(sentence_graph.get_vertex(WORD_4, POS_4), vertex_4)

        self.assertTrue(len(sentence_graph.get_vertices()) == 4)

    def test_add_sentence_edge_from_words(self):
        sentence_graph = SentenceGraph()
        vertex_1 = sentence_graph.add_vertex(WORD_1, POS_1)
        vertex_2 = sentence_graph.add_vertex(WORD_2, POS_2)
        vertex_3 = sentence_graph.add_vertex(WORD_3, POS_3)
        vertex_4 = sentence_graph.add_vertex(WORD_4, POS_4)

        edge_1 = sentence_graph.add_sentence_edge_from_words(
            WORD_1, POS_1, WORD_2, POS_2)
        edge_2 = sentence_graph.add_sentence_edge_from_words(
            WORD_3, POS_3, WORD_2, POS_2)
        edge_3 = sentence_graph.add_sentence_edge_from_words(
            WORD_3, POS_3, WORD_4, POS_4)

        self.assertEqual(sentence_graph.get_edge(WORD_1, POS_1, WORD_2, POS_2), edge_1)
        self.assertEqual(sentence_graph.get_edge(WORD_3, POS_3, WORD_2, POS_2), edge_2)
        self.assertEqual(sentence_graph.get_edge(WORD_3, POS_3, WORD_4, POS_4), edge_3)

        self.assertEqual(sentence_graph.get_sentence_edge_properties()[edge_1], '(0, 1)')
        self.assertEqual(sentence_graph.get_sentence_edge_properties()[edge_2], '(2, 1)')
        self.assertEqual(sentence_graph.get_sentence_edge_properties()[edge_3], '(2, 3)')

        self.assertTrue(len(sentence_graph.get_edges()) == 3)

    def test_add_definition_edge_from_words(self):
        sentence_graph = SentenceGraph()
        vertex_1 = sentence_graph.add_vertex(WORD_1, POS_1)
        vertex_2 = sentence_graph.add_vertex(WORD_2, POS_2)
        vertex_3 = sentence_graph.add_vertex(WORD_3, POS_3)
        vertex_4 = sentence_graph.add_vertex(WORD_4, POS_4)

        edge_1 = sentence_graph.add_definition_edge_from_words(
            WORD_1, POS_1, WORD_2, POS_2)
        edge_2 = sentence_graph.add_definition_edge_from_words(
            WORD_3, POS_3, WORD_2, POS_2)
        edge_3 = sentence_graph.add_definition_edge_from_words(
            WORD_3, POS_3, WORD_4, POS_4)

        self.assertEqual(sentence_graph.get_edge(WORD_1, POS_1, WORD_2, POS_2), edge_1)
        self.assertEqual(sentence_graph.get_edge(WORD_3, POS_3, WORD_2, POS_2), edge_2)
        self.assertEqual(sentence_graph.get_edge(WORD_3, POS_3, WORD_4, POS_4), edge_3)

        self.assertEqual(sentence_graph.get_definition_edge_properties()[edge_1], '(0, 1)')
        self.assertEqual(sentence_graph.get_definition_edge_properties()[edge_2], '(2, 1)')
        self.assertEqual(sentence_graph.get_definition_edge_properties()[edge_3], '(2, 3)')

        self.assertTrue(len(sentence_graph.get_edges()) == 3)

    def test_remove_vertex(self):
        sentence_graph = SentenceGraph()
        sentence_graph.add_vertex(WORD_1, POS_1)
        sentence_graph.add_vertex(WORD_2, POS_2)
        sentence_graph.add_vertex(WORD_3, POS_3)
        sentence_graph.add_vertex(WORD_4, POS_4)
        sentence_graph.add_vertex(WORD_5, POS_5)
        sentence_graph.add_vertex(WORD_6, POS_6)        

        sentence_graph.remove_vertex(sentence_graph.get_vertex(WORD_1, POS_1))
        self.assertIsNone(sentence_graph.get_vertex(WORD_1, POS_1))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_2, POS_2))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_3, POS_3))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_4, POS_4))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_5, POS_5))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_6, POS_6))

        sentence_graph.remove_vertex(sentence_graph.get_vertex(WORD_4, POS_4))
        self.assertIsNone(sentence_graph.get_vertex(WORD_1, POS_1))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_2, POS_2))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_3, POS_3))
        self.assertIsNone(sentence_graph.get_vertex(WORD_4, POS_4))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_5, POS_5))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_6, POS_6))

        sentence_graph.remove_vertex(sentence_graph.get_vertex(WORD_5, POS_5))
        self.assertIsNone(sentence_graph.get_vertex(WORD_1, POS_1))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_2, POS_2))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_3, POS_3))
        self.assertIsNone(sentence_graph.get_vertex(WORD_4, POS_4))
        self.assertIsNone(sentence_graph.get_vertex(WORD_5, POS_5))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_6, POS_6))

        sentence_graph.remove_vertex(sentence_graph.get_vertex(WORD_2, POS_2))
        self.assertIsNone(sentence_graph.get_vertex(WORD_1, POS_1))
        self.assertIsNone(sentence_graph.get_vertex(WORD_2, POS_2))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_3, POS_3))
        self.assertIsNone(sentence_graph.get_vertex(WORD_4, POS_4))
        self.assertIsNone(sentence_graph.get_vertex(WORD_5, POS_5))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_6, POS_6))

        sentence_graph.remove_vertex(sentence_graph.get_vertex(WORD_3, POS_3))
        self.assertIsNone(sentence_graph.get_vertex(WORD_1, POS_1))
        self.assertIsNone(sentence_graph.get_vertex(WORD_2, POS_2))
        self.assertIsNone(sentence_graph.get_vertex(WORD_3, POS_3))
        self.assertIsNone(sentence_graph.get_vertex(WORD_4, POS_4))
        self.assertIsNone(sentence_graph.get_vertex(WORD_5, POS_5))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_6, POS_6))

        sentence_graph.remove_vertex(sentence_graph.get_vertex(WORD_6, POS_6))
        self.assertIsNone(sentence_graph.get_vertex(WORD_1, POS_1))
        self.assertIsNone(sentence_graph.get_vertex(WORD_2, POS_2))
        self.assertIsNone(sentence_graph.get_vertex(WORD_3, POS_3))
        self.assertIsNone(sentence_graph.get_vertex(WORD_4, POS_4))
        self.assertIsNone(sentence_graph.get_vertex(WORD_5, POS_5))
        self.assertIsNone(sentence_graph.get_vertex(WORD_6, POS_6))

        self.assertTrue(len(sentence_graph.get_vertices()) == 0)

    def test_remove_vertex_from_words(self):
        sentence_graph = SentenceGraph()
        sentence_graph.add_vertex(WORD_1, POS_1)
        sentence_graph.add_vertex(WORD_2, POS_2)
        sentence_graph.add_vertex(WORD_3, POS_3)
        sentence_graph.add_vertex(WORD_4, POS_4)
        sentence_graph.add_vertex(WORD_5, POS_5)
        sentence_graph.add_vertex(WORD_6, POS_6)

        sentence_graph.remove_vertex_by_word(WORD_1, POS_1)
        self.assertIsNone(sentence_graph.get_vertex(WORD_1, POS_1))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_2, POS_2))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_3, POS_3))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_4, POS_4))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_5, POS_5))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_6, POS_6))

        sentence_graph.remove_vertex_by_word(WORD_4, POS_4)
        self.assertIsNone(sentence_graph.get_vertex(WORD_1, POS_1))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_2, POS_2))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_3, POS_3))
        self.assertIsNone(sentence_graph.get_vertex(WORD_4, POS_4))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_5, POS_5))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_6, POS_6))

        sentence_graph.remove_vertex_by_word(WORD_5, POS_5)
        self.assertIsNone(sentence_graph.get_vertex(WORD_1, POS_1))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_2, POS_2))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_3, POS_3))
        self.assertIsNone(sentence_graph.get_vertex(WORD_4, POS_4))
        self.assertIsNone(sentence_graph.get_vertex(WORD_5, POS_5))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_6, POS_6))

        sentence_graph.remove_vertex_by_word(WORD_2, POS_2)
        self.assertIsNone(sentence_graph.get_vertex(WORD_1, POS_1))
        self.assertIsNone(sentence_graph.get_vertex(WORD_2, POS_2))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_3, POS_3))
        self.assertIsNone(sentence_graph.get_vertex(WORD_4, POS_4))
        self.assertIsNone(sentence_graph.get_vertex(WORD_5, POS_5))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_6, POS_6))

        sentence_graph.remove_vertex_by_word(WORD_6, POS_6)
        self.assertIsNone(sentence_graph.get_vertex(WORD_1, POS_1))
        self.assertIsNone(sentence_graph.get_vertex(WORD_2, POS_2))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_3, POS_3))
        self.assertIsNone(sentence_graph.get_vertex(WORD_4, POS_4))
        self.assertIsNone(sentence_graph.get_vertex(WORD_5, POS_5))
        self.assertIsNone(sentence_graph.get_vertex(WORD_6, POS_6))

        sentence_graph.remove_vertex_by_word(WORD_3, POS_3)
        self.assertIsNone(sentence_graph.get_vertex(WORD_1, POS_1))
        self.assertIsNone(sentence_graph.get_vertex(WORD_2, POS_2))
        self.assertIsNone(sentence_graph.get_vertex(WORD_3, POS_3))
        self.assertIsNone(sentence_graph.get_vertex(WORD_4, POS_4))
        self.assertIsNone(sentence_graph.get_vertex(WORD_5, POS_5))
        self.assertIsNone(sentence_graph.get_vertex(WORD_6, POS_6))

        self.assertTrue(len(sentence_graph.get_vertices()) == 0)

    def test_remove_vertex_by_word_with_edges_present(self):
        sentence_graph = SentenceGraph()
        vertex_1 = sentence_graph.add_vertex(WORD_1, POS_1)
        vertex_2 = sentence_graph.add_vertex(WORD_2, POS_2)
        vertex_3 = sentence_graph.add_vertex(WORD_3, POS_3)
        vertex_4 = sentence_graph.add_vertex(WORD_4, POS_4)
        vertex_5 = sentence_graph.add_vertex(WORD_5, POS_5)
        vertex_6 = sentence_graph.add_vertex(WORD_6, POS_6)

        sentence_graph.add_sentence_edge(vertex_1, vertex_6)
        sentence_graph.add_sentence_edge(vertex_4, vertex_5)
        sentence_graph.add_sentence_edge(vertex_2, vertex_1)
        sentence_graph.add_sentence_edge(vertex_2, vertex_6)
        sentence_graph.add_sentence_edge(vertex_2, vertex_5)
        sentence_graph.add_sentence_edge(vertex_3, vertex_5)
        sentence_graph.add_sentence_edge(vertex_3, vertex_6)
        sentence_graph.add_sentence_edge(vertex_3, vertex_1)

        sentence_graph.remove_vertex_by_word(WORD_1, POS_1)
        self.assertIsNone(sentence_graph.get_vertex(WORD_1, POS_1))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_2, POS_2))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_3, POS_3))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_4, POS_4))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_5, POS_5))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_6, POS_6))

        self.assertIsNone(sentence_graph.get_edge(WORD_1, POS_1, WORD_6, POS_6))
        self.assertIsNone(sentence_graph.get_edge(WORD_2, POS_2, WORD_1, POS_1))
        self.assertIsNone(sentence_graph.get_edge(WORD_3, POS_3, WORD_1, POS_1))


        sentence_graph.remove_vertex_by_word(WORD_4, POS_4)
        self.assertIsNone(sentence_graph.get_vertex(WORD_1, POS_1))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_2, POS_2))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_3, POS_3))
        self.assertIsNone(sentence_graph.get_vertex(WORD_4, POS_4))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_5, POS_5))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_6, POS_6))

        self.assertIsNone(sentence_graph.get_edge(WORD_4, POS_4, WORD_5, POS_5))

        sentence_graph.remove_vertex_by_word(WORD_5, POS_5)
        self.assertIsNone(sentence_graph.get_vertex(WORD_1, POS_1))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_2, POS_2))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_3, POS_3))
        self.assertIsNone(sentence_graph.get_vertex(WORD_4, POS_4))
        self.assertIsNone(sentence_graph.get_vertex(WORD_5, POS_5))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_6, POS_6))

        self.assertIsNone(sentence_graph.get_edge(WORD_2, POS_2, WORD_5, POS_5))
        self.assertIsNone(sentence_graph.get_edge(WORD_3, POS_3, WORD_5, POS_5))

        sentence_graph.remove_vertex_by_word(WORD_2, POS_2)
        self.assertIsNone(sentence_graph.get_vertex(WORD_1, POS_1))
        self.assertIsNone(sentence_graph.get_vertex(WORD_2, POS_2))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_3, POS_3))
        self.assertIsNone(sentence_graph.get_vertex(WORD_4, POS_4))
        self.assertIsNone(sentence_graph.get_vertex(WORD_5, POS_5))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_6, POS_6))

        self.assertIsNone(sentence_graph.get_edge(WORD_2, POS_2, WORD_6, POS_6))

        sentence_graph.remove_vertex_by_word(WORD_6, POS_6)
        self.assertIsNone(sentence_graph.get_vertex(WORD_1, POS_1))
        self.assertIsNone(sentence_graph.get_vertex(WORD_2, POS_2))
        self.assertIsNotNone(sentence_graph.get_vertex(WORD_3, POS_3))
        self.assertIsNone(sentence_graph.get_vertex(WORD_4, POS_4))
        self.assertIsNone(sentence_graph.get_vertex(WORD_5, POS_5))
        self.assertIsNone(sentence_graph.get_vertex(WORD_6, POS_6))

        self.assertIsNone(sentence_graph.get_edge(WORD_3, POS_3, WORD_6, POS_6))

        sentence_graph.remove_vertex_by_word(WORD_3, POS_3)
        self.assertIsNone(sentence_graph.get_vertex(WORD_1, POS_1))
        self.assertIsNone(sentence_graph.get_vertex(WORD_2, POS_2))
        self.assertIsNone(sentence_graph.get_vertex(WORD_3, POS_3))
        self.assertIsNone(sentence_graph.get_vertex(WORD_4, POS_4))
        self.assertIsNone(sentence_graph.get_vertex(WORD_5, POS_5))
        self.assertIsNone(sentence_graph.get_vertex(WORD_6, POS_6))        

        self.assertTrue(len(sentence_graph.get_vertices()) == 0)
        self.assertTrue(len(sentence_graph.get_edges()) == 0)

if __name__ == '__main__':
    unittest.main()