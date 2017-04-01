from graph_tool.all import Graph

from multiprocessing import Lock
from multiprocessing import Manager
import os
import unittest

import sentence_graph_test_utilities

# Need to add to python path to access src folder
import sys
sys.path.insert(1, "../src")
from sentence_graph_construction import build_deep_sentence_graph
from sentence_graph_reduction import reduce_sentence_graphs
from sentence_graph_io import load_sentence_graph_from_file
from sentence_graph_io import save_sentence_graph_to_file
from sentence_graph_io import sentence_graph_draw
from sentence_graph_io import sentence_graph_file_path_from_sentence
from wiktionary_client import clear_wiktionary_file_locks
from wiktionary_client import WiktionaryClient

WIKTIONARY_SPIDER_FILE_PATH = "../src/wiktionary_spider.py"

SENTENCE_1 = "I attend a wonderful college."
SENTENCE_2 = "I attend a great university."

sentences = [
        "Austin is the capitol of Texas.",
        "The United States was founded in 1776.",
        "California is currently in a terrible drought.",
        "Oregon is a very green state.",
        "Virginia is located on the east coast.",
        "Massachussets is a very liberal state.",
        "Florida is going to be under water in 200 years.",
        "Wyoming skiing is absolutely amazing.",
        "There have been many presidents from Illinois.",
        "Chicago was home to many gangsters in the early 1900s.",
        "Oklahoma is having big issues with fracking.",
        "Nevada has an amazing solar tower.",
        "Colorado made a great decision in legalizing marijuana.",
        "Kansas is known for tornados.",
        "Nebraska is known for its corn.",
        "Idaho is known for its potatoes.",
        "Arizona does not observe daylight savings time.",
        "Louisiana is also going to be under water.",
        "Alabama almost got screwed over by Coke.",
        "Maryland is North of Virginia.",
    ]

class TestSentenceGraphReduction(unittest.TestCase):
    def large_tests(self, clear_cached=False):
        clear_wiktionary_file_locks()
        sentence_graphs_cache_folder = "sentence-graphs-storage/sentence-graph-reduction-test-graphs"
        if clear_cached:
            _clear_cached_sentence_graph_files(sentence_graphs_cache_folder)

        wiktionary_client = WiktionaryClient(Manager().Lock(), WIKTIONARY_SPIDER_FILE_PATH)

        sentence_graphs = []
        for sentence in sentences:
            sentence_graph_file_path = sentence_graph_file_path_from_sentence(
                sentence, sentence_graphs_cache_folder)
            sentence_graph = load_sentence_graph_from_file(sentence_graph_file_path)
            if sentence_graph is None:
                sentence_graph = build_deep_sentence_graph(
                    sentence, wiktionary_client, depth=2)
                sentence_graph_draw(
                    sentence_graph, 
                    sentence,
                    output_folder_name="sentence-graphs-visualization",
                    output_file_name="reduction-tests--%s" % sentence,
                    file_extension=".png")
                save_sentence_graph_to_file(sentence_graph, sentence_graph_file_path)

            sentence_graphs.append(sentence_graph)

        print("\n\nReducing sentence graphs")
        reduced_sentence_graphs = reduce_sentence_graphs(sentence_graphs)
        for sentence, reduced_sentence_graph in zip(sentences, reduced_sentence_graphs):
            sentence_graph_draw(
                reduced_sentence_graph, 
                sentence,
                output_folder_name="sentence-graphs-visualization",
                output_file_name="reduction-tests--REDUCED--%s" % sentence,
                file_extension=".png")

    def test_two_sentence_depth_1_reduction(self):
        expected_reduced_sentence_graph_1 = Graph(directed=False)
        wonderful_vertex = expected_reduced_sentence_graph_1.add_vertex()
        college_vertex = expected_reduced_sentence_graph_1.add_vertex()
        expected_reduced_sentence_graph_1.add_edge(wonderful_vertex, college_vertex)

        expected_reduced_sentence_graph_2 = Graph(directed=False)
        great_vertex = expected_reduced_sentence_graph_2.add_vertex()
        university_vertex = expected_reduced_sentence_graph_2.add_vertex()
        expected_reduced_sentence_graph_2.add_edge(great_vertex, university_vertex)

        sentence_graphs, reduced_sentence_graphs = _two_sentence_depth_reduction(
            SENTENCE_1, SENTENCE_2, depth=1)

        self.assertEqual(expected_reduced_sentence_graph_1, reduced_sentence_graphs[0])
        self.assertEqual(expected_reduced_sentence_graph_2, reduced_sentence_graphs[1])

    """
    def test_two_sentence_depth_2_reduction(self):
        sentence_graphs, reduced_sentence_graphs = _two_sentence_depth_reduction(
            SENTENCE_1, SENTENCE_2, depth=2)
    """

    """
    def small_tests():
        test_two_sentence_depth_0_reduction()


    def tests():
        small_tests()
        #large_tests()
    """

def _two_sentence_depth_reduction(sentence_1, sentence_2, depth):
    wiktionary_client = WiktionaryClient(Manager().Lock(), WIKTIONARY_SPIDER_FILE_PATH)

    sentence_graph_1 = build_deep_sentence_graph(
        sentence_1, wiktionary_client, depth=depth)
    sentence_graph_2 = build_deep_sentence_graph(
        sentence_2, wiktionary_client, depth=depth)
    sentence_graphs = [sentence_graph_1, sentence_graph_2]

    return sentence_graphs, reduce_sentence_graphs(sentence_graphs)

def _clear_cached_sentence_graph_files(sentence_graphs_folder):
    for file_name in os.listdir(sentence_graphs_folder):
        os.remove(os.paths.join(sentence_graphs_folder, file_name))

if __name__ == '__main__':
    clear_wiktionary_file_locks()
    unittest.main()