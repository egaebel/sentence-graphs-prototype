from graph_tool.all import Graph

WORD_KEY = "word"
PART_OF_SPEECH_KEY = "part_of_speech"
VERTEX_COLOR_KEY = "vertex_color"
SENTENCE_EDGE_KEY = "sentence_edge"
DEFINITION_EDGE_KEY = "definition_edge"

class SentenceGraph():
    def __init__(self, directed=False):
        self.sentence_graph = Graph(directed=directed)
    
        # Vertex properties
        word_property = self.sentence_graph.new_vertex_property("string")
        part_of_speech_property = self.sentence_graph.new_vertex_property("string")
        vertex_color_property = self.sentence_graph.new_vertex_property("vector<double>")
        self.sentence_graph.vertex_properties[WORD_KEY] = word_property
        self.sentence_graph.vertex_properties[PART_OF_SPEECH_KEY] = part_of_speech_property
        self.sentence_graph.vertex_properties[VERTEX_COLOR_KEY] = vertex_color_property

        # Edge properties
        sentence_edge_property = self.sentence_graph.new_edge_property("string")
        definition_edge_property = self.sentence_graph.new_edge_property("string")
        self.sentence_graph.edge_properties[SENTENCE_EDGE_KEY] = sentence_edge_property
        self.sentence_graph.edge_properties[DEFINITION_EDGE_KEY] = definition_edge_property

    def add_vertex(self, word, pos):
        word_pos_tuple = (word, pos)

        # Create vertex, set properties
        word_vertex = self.sentence_graph.add_vertex()

        self.sentence_graph.vertex_properties[WORD_KEY][word_vertex] = word
        self.sentence_graph.vertex_properties[PART_OF_SPEECH_KEY][word_vertex] = pos
        self.sentence_graph.vertex_properties[VERTEX_COLOR_KEY][word_vertex] = [0, 0, 1, 1]

        return word_vertex

    def add_sentence_edge_from_words(self, word1, pos1, word2, pos2):
        return self.add_sentence_edge(self.get_vertex(word1, pos1), self.get_vertex(word2, pos2))

    def add_sentence_edge(self, word_vertex1, word_vertex2):
        sentence_edge = self.sentence_graph.add_edge(word_vertex1, word_vertex2)
        self.sentence_graph.edge_properties[SENTENCE_EDGE_KEY][sentence_edge] = sentence_edge
        return sentence_edge

    def add_definition_edge_from_words(self, word, pos, definition_word, definition_pos):
        return self.add_definition_edge(
            self.get_vertex(word, pos),
            self.get_vertex(definition_word, definition_pos))

    def add_definition_edge(self, word_vertex, definition_word_vertex):
        definition_edge = self.sentence_graph.add_edge(word_vertex, definition_word_vertex)
        self.sentence_graph.edge_properties[DEFINITION_EDGE_KEY][definition_edge] = definition_edge
        return definition_edge

    def add_definition_edges(self, word_vertex, definition_word_vertices):
        # Add edges from the word_vertex to all definition vertices and set 
        # the definition edge property on each edge
        for definition_word_vertex in definition_word_vertices:
            self.add_definition_edge(word_vertex, definition_word_vertices)
        return self

    def remove_vertex_by_word(self, word, pos):
        self.remove_vertex(self.get_vertex(word, pos))

    def remove_vertex(self, vertex):
        word = self.sentence_graph.vertex_properties[WORD_KEY][vertex]
        pos = self.sentence_graph.vertex_properties[PART_OF_SPEECH_KEY][vertex]
        self.sentence_graph.remove_vertex(vertex)

    def remove_edge(self, word1, pos1, word2, pos2):
        self.sentence_graph.remove_edge(self.get_edge(word1, pos1, word2, pos2))
                         
    def contains(self, word, pos):
        return self.get_vertex(word, pos) is not None

    def get_vertex(self, word, pos):
        for vertex in self.sentence_graph.vertices():
            try:
                vertex_word = self.sentence_graph.vertex_properties[WORD_KEY][vertex]
                vertex_pos = self.sentence_graph.vertex_properties[PART_OF_SPEECH_KEY][vertex]
                if vertex_word == word and vertex_pos == pos:
                    return vertex
            except:
                pass
        return None

    def get_vertex_by_index(self, index):
        return self.sentence_graph.vertex(index)

    def get_vertices_iterator(self):
        return self.sentence_graph.vertices()

    def get_vertices(self):
        return [x for x in self.sentence_graph.vertices()]

    def get_edge(self, word1, pos1, word2, pos2):
        vertex_1 = self.get_vertex(word1, pos1)
        vertex_2 = self.get_vertex(word2, pos2)
        return None\
            if vertex_1 is None or vertex_2 is None\
            else self.sentence_graph.edge(vertex_1, vertex_2)

    def get_edges_iterator(self):
        return self.sentence_graph.edges()

    def get_edges(self):
        return [x for x in self.sentence_graph.edges()]

    def get_word_vertex_properties(self):
        return self.sentence_graph.vertex_properties[WORD_KEY]

    def get_pos_vertex_properties(self):
        return self.sentence_graph.vertex_properties[PART_OF_SPEECH_KEY]

    def get_vertex_color_properties(self):
        return self.sentence_graph.vertex_properties[VERTEX_COLOR_KEY]

    def get_sentence_edge_properties(self):
        return self.sentence_graph.edge_properties[SENTENCE_EDGE_KEY]

    def get_definition_edge_properties(self):
        return self.sentence_graph.edge_properties[DEFINITION_EDGE_KEY]

    def get_graph(self):
        return self.sentence_graph