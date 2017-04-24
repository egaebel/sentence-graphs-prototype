from pylocker import Locker

import scrapy

import json
import time
import types
import uuid

# The part of speech is the only string argument to this query
WIKTIONARY_XPATH_QUERY_H3 =\
"""//span[@class="mw-headline"][@id="English"]/../following-sibling::h3/span[@class="mw-headline"][@id="%s"]/../following-sibling::ol[1]/li[1]/node()[not(self::ul)][not(self::dl)]//self::text()[normalize-space()]"""
WIKTIONARY_XPATH_QUERY_H4 =\
"""//span[@class="mw-headline"][@id="English"]/../following-sibling::h4/span[@class="mw-headline"][@id="%s"]/../following-sibling::ol[1]/li[1]/node()[not(self::ul)][not(self::dl)]//self::text()[normalize-space()]"""
SHORT_WIKTIONARY_XPATH_QUERY_H3 =\
"""//span[@class="mw-headline"][@id="English"]/../following-sibling::h3/span[@class="mw-headline"][@id="%s"]"""
SHORT_WIKTIONARY_XPATH_QUERY_H4 =\
"""//span[@class="mw-headline"][@id="English"]/../following-sibling::h4/span[@class="mw-headline"][@id="%s"]"""

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
        self.root_url = kwargs.get('root_url')
        self.urls = kwargs.get('urls')
        self.word = kwargs.get('word')
        self.part_of_speech = kwargs.get('part_of_speech')
        self.output_file_path = kwargs.get('output_file_path')
        if not isinstance(self.urls, types.ListType):
            self.urls = [self.urls]
        
        # We don't want any strange characters like quotes
        self.word = filter(self._character_filter, self.word.lower())

        # Wiktionary has all part of speech headings with the first letter 
        # captialized and the other letters lowercase
        self.part_of_speech =\
            self.part_of_speech[:1].upper() + self.part_of_speech[1:].lower()
        # Wiktionary has underscores instead of spaces in multi-word part of speech ids 
        self.part_of_speech = self.part_of_speech.replace(" ", "_")

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
                errback=self.error_callback)

    def error_callback(self, x):
        self.log("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$Error callback reached")
        self.log("Other argument is: %s" % x)
        # If the word is a noun, try retrying with the noun capitalized
        if self.part_of_speech.lower() == 'noun':
            upper_cased_word = self.word[:1].upper() + self.word[1:].lower()
            url = "%s/%s" % (root_url, upper_cased_word) 
            yield scrapy.Request(
                url=url, 
                callback=self.wiktionary_parse,
                errback=lambda: None)
        yield None

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
                    .xpath(SHORT_WIKTIONARY_XPATH_QUERY_H4 
                        % self.part_of_speech)
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

        output_dict = {
            'word': self.word,
            'part_of_speech': self.part_of_speech,
            'definition': definition,
        }

        self._write_definition_json_to_file(output_dict, self.output_file_path)

        return output_dict

    def _write_definition_json_to_file(self, output_dict, output_file_path):
        max_file_lock_iterations = 1000
        print("Writing: %s to file" % output_dict)
        written = False
        file_lock_iteration = 0
        while not written:
            # Create file lock
            lock_pass = str(uuid.uuid1())
            file_lock = Locker(filePath=output_file_path, lockPass=lock_pass, mode='w')
            with file_lock as lock:
                was_acquired, code, fd = lock
                # If lock was acquired
                if fd is not None:
                    fd.write(json.dumps([output_dict]))
                    written = True
                else:
                    time.sleep(1)
            file_lock_iteration += 1
            if file_lock_iteration >= max_file_lock_iterations:
                print("ERROR: File lock acquisition in wiktionary_spider timed out at %d "
                    + "attempts to acquire file lock on file: %s" % (file_lock_iteration, output_file_path))

    def _character_filter(self, x):
        return ord('a') <= ord(x) <= ord('z')\
            or ord(x) == ord(' ')\
            or ord(x) == ord('<')\
            or ord(x) == ord('=')\
            or ord(x) == ord('>')\
            or ord(x) == ord('.')\
            or ord(x) == ord(',')
