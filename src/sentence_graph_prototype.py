from aylienapiclient import textapi

from graph_tool.all import Graph
from graph_tool.all import graph_draw
from graph_tool.all import load_graph
from graph_tool import topology

import scrapy

import itertools
import json
import os
import os.path
import re
import subprocess
import sys
import types

# Use functions from parsey-mcparseface-service
sys.path.insert(1, "../../parsey-mcparseface-service/src/")
from run_parsey import run_parsey
from parse_tree_parser import parse_ascii_tree

################################################################################
###########################-----Global Variables-----###########################
################################################################################

WIKIPEDIA_ARTICLE_LIST_FILE_PATH = "data/enwiki-latest-all-titles-in-ns0"
WIKIPEDIA_WEB_ROOT_URL = "https://en.wikipedia.org/wiki"
WIKIPEDIA_LOCAL_ROOT_URL = ""

WIKTIONARY_WEB_ROOT_URL = "https://en.wiktionary.org/wiki"
WIKTIONARY_LOCAL_ROOT_URL = ""
# The part of speech is the only string argument to this query
WIKTIONARY_XPATH_QUERY_H3 =\
"""//span[@class="mw-headline"][@id="English"]/../following-sibling::h3/span[@class="mw-headline"][@id="%s"]/../following-sibling::ol[1]/li[1]/node()[not(self::ul)][not(self::dl)]//self::text()[normalize-space()]"""
WIKTIONARY_XPATH_QUERY_H4 =\
"""//span[@class="mw-headline"][@id="English"]/../following-sibling::h4/span[@class="mw-headline"][@id="%s"]/../following-sibling::ol[1]/li[1]/node()[not(self::ul)][not(self::dl)]//self::text()[normalize-space()]"""
SHORT_WIKTIONARY_XPATH_QUERY_H3 =\
"""//span[@class="mw-headline"][@id="English"]/../following-sibling::h3/span[@class="mw-headline"][@id="%s"]"""
SHORT_WIKTIONARY_XPATH_QUERY_H4 =\
"""//span[@class="mw-headline"][@id="English"]/../following-sibling::h4/span[@class="mw-headline"][@id="%s"]"""

AYLIEN_APP_ID = "7fe8de1d"
AYLIEN_APP_KEY = "ef49f063d5cb17a97f158e43de5f7747"

PARSEY_PART_OF_SPEECH_TO_WIKTIONARY_MAP = {
    'CC': 'Coordinating conjunction',
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
###########################-----Scrapy Spider(s)-----###########################
################################################################################

# A scrapy spider for scraping a definition of a word from Wiktionary
# The definition is specified by the word and the part of speech, for now the
# language is assumed to be English.
# The definition is returned as a dict to go through scrapy's usual processing
# pipeline.
# To write the definition to file as JSON, set the following project settings 
# before initiating a crawl
# 
# settings = {
#        'FEED_FORMAT': 'json',
#        'FEED_URI': output_file_path,
#        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
# }
#
# NOTE: USER_AGENT is obviously unrelated to scrapy output, but it's included to
#       have all default settings in one place.
class WiktionarySpider(scrapy.Spider):
    name = "wiktionary-web"

    def __init__(self, *args, **kwargs):
        super(WiktionarySpider, self).__init__(*args, **kwargs)
        self.urls = kwargs.get('urls')
        self.word = kwargs.get('word')
        self.part_of_speech = kwargs.get('part_of_speech')
        if not isinstance(self.urls, types.ListType):
            self.urls = [self.urls]
        
        # Wiktionary has all part of speech headings with the first letter 
        # captialized and the other letters lowercase
        self.part_of_speech =\
            self.part_of_speech[:1].upper() + self.part_of_speech[1:].lower()

        self.log("\n\n")
        self.log("urls: %s" % self.urls)
        self.log("word: %s" % self.word)
        self.log("part_of_speech: %s" % self.part_of_speech)
        self.log("\n\n")

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(
                url=url, 
                callback=self.wiktionary_parse,
                errback=lambda x: None)

    def wiktionary_parse(self, response):
        self.log("\n\n")
        self.log("Word: %s" % self.word)
        self.log("Part of Speech: %s\n" % self.part_of_speech)

        self.log("short wiktionary xpath result (h3): %s" %
            response
                .xpath(SHORT_WIKTIONARY_XPATH_QUERY_H3 % self.part_of_speech)
                .extract())

        xpath_parse = response\
            .xpath(WIKTIONARY_XPATH_QUERY_H3 % self.part_of_speech)\
            .extract()
        if len(xpath_parse) == 0:
            self.log("short wiktionary xpath result (h4): %s" %
                response
                    .xpath(SHORT_WIKTIONARY_XPATH_QUERY_H4 % self.part_of_speech)
                    .extract())
            xpath_parse = response\
            .xpath(WIKTIONARY_XPATH_QUERY_H4 % self.part_of_speech)\
            .extract()
        definition = ' '\
            .join([x.strip() for x in xpath_parse])\
            .replace('.', '')\
            .strip()

        definition = filter(self._character_filter, definition.lower())

        self.log("Fully Parsed Definition: %s\n\n\n" % definition)

        return {
            'word': self.word,
            'part_of_speech': self.part_of_speech,
            'definition': definition,
        }

    def _character_filter(self, x):
        return ord('a') <= ord(x) <= ord('z')\
            or ord(x) == ord(' ')\
            or ord(x) == ord('<')\
            or ord(x) == ord('=')\
            or ord(x) == ord('>')\
            or ord(x) == ord('.')\
            or ord(x) == ord(',')

################################################################################
###########################-----Wikpedia Functions-----#########################
################################################################################

# Scrape all of wikipedia starting at a random page and going up to page_limit
# pages before stopping. If page_limit==0 then all of wikipedia will be scraped.
def scrape_wikipedia(
        wikipedia_root_url=WIKIPEDIA_WEB_ROOT_URL, 
        article_titles_file=WIKIPEDIA_ARTICLE_LIST_FILE_PATH, 
        page_limit=5):
    wikipedia_urls_generator = get_all_wikipedia_urls(\
        wikipedia_root_url,
        article_titles_file)

    wikipedia_articles = []
    url_count = 0
    for url in wikipedia_urls_generator:
        wikipedia_article_body = _strip_wikipedia_citations(\
            get_article_text(url))
        wikipedia_article_dict = {
            'url': url, 
            'body': wikipedia_article_body, 
            'sentence_graphs': list(),
        }
        wikipedia_articles.append(wikipedia_article_dict)

        url_count += 1
        if page_limit > 0 and url_count > page_limit:
            break

    return wikipedia_articles

# Return a generator that generates all wikipedia article URLs starting from the
# passed URL (for handling local copies of wikipedia or other mirrors) drawing 
# from the passed in article_titles_file to obtain a listing of page titles.
def get_all_wikipedia_urls(wikipedia_root_url, article_titles_file):
    with open(article_titles_file, 'r') as titles_file:
        for line in titles_file:
            yield "%s/%s" % (wikipedia_root_url, line)

# Use Aylien API to get text from URL or full text
#
# Return string with article text
def get_article_text(url):
    client = _get_aylien_client()
    return client.Extract(url)["article"]

def _get_aylien_client(
        aylien_app_id=AYLIEN_APP_ID, aylien_app_key=AYLIEN_APP_KEY):
    return textapi.Client(aylien_app_id, aylien_app_key)

# Strip Wikipedia citations from the passed in text
# e.g. [27], [309]
def _strip_wikipedia_citations(text):
    return re.sub("\[[0-9]*\]", "", text)

################################################################################
##########################-----Wiktionary Functions-----########################
################################################################################

# Hit wiktionary, scrape definition using word and POS
#
# Return a sentence graph of the definition
def lookup_definition_on_wiktionary(
        word, 
        part_of_speech, 
        wiktionary_root_url=WIKTIONARY_WEB_ROOT_URL,
        use_cache=True):
    print("Looking up %s %s on wiktionary......" % (word, part_of_speech))
    definition_text = _parse_wiktionary(
        "%s/%s" % (wiktionary_root_url, word), 
        word, 
        part_of_speech, 
        use_cache=use_cache)
    return definition_text

# Use scrapy to parse the wiktionary url (TODO MAKE THIS COMMENT MORE COMPLETE)
def _parse_wiktionary(wiktionary_url, word, part_of_speech, use_cache=False):
    output_file_path = "definition-cache/scrapy-scrape-test--%s-%s.json"\
        % (word, part_of_speech)
    if not use_cache or not os.path.exists(output_file_path):
        _run_scrapyd_spider(
            wiktionary_url, word, part_of_speech, output_file_path)

    print("\n\n\n")
    with open(output_file_path, 'r') as json_definition_data:
        try:
            definition_data = json.load(json_definition_data)
            print("definition_data: %s" % definition_data)
        except:
            print("ERROR: Could not find definition file at path: %s" 
                % output_file_path)
            return ""
    return definition_data[0]['definition']

def _run_scrapyd_spider(urls, word, part_of_speech, output_file_path):
    spider_file = "sentence_graph_prototype.py"
    if not isinstance(urls, types.ListType):
        urls = [urls]
    subprocess.check_call([
        "scrapy", 
        "runspider", 
        spider_file, 
        "-a",
        "urls=%s" % ",".join(urls),
        "-a",
        "word=%s" % word,
        "-a",
        "part_of_speech=%s" % part_of_speech,
        "-o",
        "%s" % output_file_path])

################################################################################
###################-----Sentence Graph Building Functions-----##################
################################################################################

# Takes some body of text, splits it into sentences, constructs sentence
# graphs for every sentence, and returns a list of all the sentence graphs.
def get_text_sentence_graphs(text, directed=False):
    sentence_graphs = []
    for sentence in text.split("."):
        sentence_graphs.append(build_deep_sentence_graph(sentence))
    return sentence_graphs


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
        definition_provider=lookup_definition_on_wiktionary, 
        directed=False,
        depth=10):
    sentence_graph = Graph(directed=directed)
    
    # Vertex properties
    word_property = sentence_graph.new_vertex_property("string")
    part_of_speech_property = sentence_graph.new_vertex_property("string")
    word_pos_tuple_property = sentence_graph.new_vertex_property("object")
    vertex_color_property = sentence_graph.new_vertex_property("vector<double>")
    sentence_graph.vertex_properties["word"] = word_property
    sentence_graph.vertex_properties["part_of_speech"] = part_of_speech_property
    sentence_graph.vertex_properties["word_pos_tuple"] = word_pos_tuple_property
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
        definition_provider,
        directed,
        depth=depth)

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
        definition_provider, 
        directed,
        depth=None):
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
            sentence_graph.vertex_properties["word_pos_tuple"][word_vertex] =\
                word_pos_tuple
            sentence_graph.vertex_properties["vertex_color"][word_vertex] =\
                [0, 0, 1, 1]
            word_pos_to_vertex_index_mapping[word_pos_tuple] =\
                sentence_graph.vertex_index[word_vertex]

            # Get definition, add pointer from word to all words in definition
            definition = definition_provider(word, part_of_speech)

            if definition.strip() != '':
                # Get definition of definitions
                definition_word_vertices = _build_deep_sentence_graph_helper(
                    definition,
                    sentence_graph, 
                    word_pos_to_vertex_index_mapping,
                    definition_provider=definition_provider, 
                    directed=directed,
                    depth=depth)

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

    sentence_graph_draw(
        sentence_graph, sentence, "linear-sentence-graph-debug.png")

def sentence_graph_draw(
        sentence_graph, 
        sentence,
        output_folder_name="sentence-graphs-visualization",
        output_file_name="sentence-graph-debug.png"):
    base_vertex_font_size = 128
    base_vertex_size = 200
    max_in_degree = max(sentence_graph.vertices(), key=lambda x: x.in_degree()).in_degree()
    print("Max in degree in sentence graph is: %s" % str(max_in_degree))
    font_size_func =\
        lambda in_degree: min(128, max(32, (in_degree / max_in_degree)))

    vertex_font_size_property_map = sentence_graph.degree_property_map("in")
    for key in sentence_graph.vertices():
        vertex_font_size_property_map[key] =\
            font_size_func(vertex_font_size_property_map[key])
    vertex_size_property_map = sentence_graph.degree_property_map("in")
    for key in sentence_graph.vertices():
        vertex_size_property_map[key] =\
            base_vertex_size * (vertex_size_property_map[key] / max_in_degree)

    output_file_path = os.path.join(output_folder_name, output_file_name)

    graph_draw(
        sentence_graph, 
        vertex_text=sentence_graph.vertex_properties["word"], 
        vertex_font_size=vertex_font_size_property_map,
        #vertex_size=vertex_size_property_map,
        vertex_fill_color=sentence_graph.vertex_properties["vertex_color"],
        output_size=(20000, 20000), 
        output=output_file_path)
    
def sentence_graph_file_path_from_sentence(
    sentence, 
    sentence_graphs_folder="sentence-graphs-storage",
    file_extension=".gt"):
    return os.path.join(
        sentence_graphs_folder, sentence.replace(" ", "-") + file_extension)

def save_sentence_graph_to_file(
        sentence_graph, output_file_path, file_format="gt"):
    sentence_graph.save(
        output_file_path,
        fmt=file_format)

def load_sentence_graph_from_file(input_file_path, file_format="gt"):
    return load_graph(input_file_path, fmt=file_format)


################################################################################
##################-----Sentence Graph Operation Functions-----##################
################################################################################

# Compute a similarity score between 0.0-1.0 between two passed in graphs
def compute_graph_similarity_score(graph1, graph2):
    pass

################################################################################
##############################-----Test & Main-----#############################
################################################################################

def sentence_graph_test(sentence, graphic_output_file_name, depth=2):
    print("Testing build_deep_sentence_graph with sentence_graph_draw....")
    sentence_graph = build_deep_sentence_graph(
        sentence, directed=True, depth=depth)
    sentence_graph_draw(
        sentence_graph,
        sentence,
        output_file_name=graphic_output_file_name)
    save_sentence_graph_to_file(
        sentence_graph, sentence_graph_file_path_from_sentence(sentence))
    loaded_sentence_graph = load_sentence_graph_from_file(
        sentence_graph_file_path_from_sentence(sentence))
    if topology.isomorphism(sentence_graph, loaded_sentence_graph):
        print("Sentence graph successfully loaded from file!!!!")
    else:
        print("Sentence graph saved and loaded from file was corrupted!")

    return sentence_graph

def test():
    """
    print("Grabbing article text for Graph-Tool......\n")
    print(\
        _strip_wikipedia_citations(\
            get_article_text(\
                "https://en.wikipedia.org/wiki/Graph-tool")))

    print("\n\n\n")

    print("Printing 500 wikipedia article URLs.......\n")
    print("".join([x for x in itertools.islice(get_all_wikipedia_urls(\
        WIKIPEDIA_WEB_ROOT_URL, WIKIPEDIA_ARTICLE_LIST_FILE_PATH), 500)]))

    print("\n\n\n")

    print("Scraping 5 wikipedia pages.......\n")
    for wikipedia_scrape in scrape_wikipedia():
        print("\n\n\n\n")
        print("Wikipedia Scrape:")
        print(wikipedia_scrape)
    
    print("\n\n\n")

    print("Scraping wiktionary pages.......\n")
    print("lookup_definition_on_wiktionary(police, noun): %s" 
        % lookup_definition_on_wiktionary("police", "noun"))
    print("\n")
    
    print("\n\n\n")

    generate_linear_sentence_graph("This is a sentence and it is great")
    
    print("\n\n\n")

    print("Testing run_parsey....")
    print("run_parsey(): ||%s||" % run_parsey("this here is a sentence, it is nice."))
    """

    """
    print("\n\n\n")

    print("Testing scrapyd spider")
    print("Output: %s" % _run_scrapyd_spider(
        "https://en.wiktionary.org/wiki/dogs",
        "dogs",
        "noun",
        "~/tester.json"))

    print("\n\n\n")    
    """

    depth = 4
    sentence_graph_1 = sentence_graph_test(
        "Donald Trump is a tyrannical ruler", 
        "donald-trump-1--synonym-sentence-graphs-debug--depth-%s.png" % depth,
        depth=depth)
    sentence_graph_2 = sentence_graph_test(
        "Donald Trump is a despotic ruler", 
        "donald-trump-2--synonym-sentence-graphs-debug--depth-%s.png" % depth,
        depth=depth)
    if topology.isomorphism(sentence_graph_1, sentence_graph_2):
        print("That was easy, those sentence graphs are the same!")
    else:
        print("As expected, it isn't that easy, the sentence graphs differ.")

if __name__ == '__main__':
    test()