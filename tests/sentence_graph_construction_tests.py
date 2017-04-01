import unittest

# Need to add to python path to access src folder
import sys
sys.path.insert(1, "../src")
from sentence_graph_construction import build_deep_sentence_graph

PARAGRAPH = "The history of the universe is brief on the cosmic scale."
    + "Many think this brevity to not be so, but on the cosmic calendar this becomes apparent."
    + "The idea of the cosmic calendar was first conceived by Carl Sagan, I think so anyway."
    + "The cosmic calendar was reused by Neil de Grasse Tyson in his remake of the Cosmos series."
    + "Usually the cosmic calendar is featured as a huge 12 month calendar that the host is standing on, "
        + "with all manner of cosmic phenomena printed on the calendar."

SENTENCE_1 = "This is the first sentence."
SENTENCE_2 = "This is the second sentence."

class TestSentenceGraphConstruction(unittest.TestCase):
    def test_(self):
        pass

if __name__ == '__main__':
    unittest.main()