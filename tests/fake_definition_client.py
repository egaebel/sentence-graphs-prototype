class FakeDefinitionClient():
    def __init__(self):
        self.definition_dict = dict()

    def set_definition(self, word, part_of_speech, definition):
        self.definition_dict[(word.lower(), part_of_speech.lower())] = definition.lower()

    def lookup_definition(self, word, part_of_speech):
        return self.definition_dict[(word.lower(), part_of_speech.lower())]
