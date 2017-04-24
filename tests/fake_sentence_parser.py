class FakeSentenceParser():
    def __init__(self):
        self.sentence_to_parse_tree_dict = dict()

    def set_parse_tree(self, sentence, parse_node):
        self.sentence_to_parse_tree_dict[sentence.replace(".", "").lower()] = parse_node

    def fake_parse_sentence(self, sentence):
        return self.sentence_to_parse_tree_dict[sentence.replace(".", "").lower()]
