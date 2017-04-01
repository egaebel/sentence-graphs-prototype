from multiprocessing import Manager
import json
import os
import os.path
import subprocess
import time
import types

WIKTIONARY_WEB_ROOT_URL = "https://en.wiktionary.org/wiki"
WIKTIONARY_LOCAL_ROOT_URL = ""

################################################################################
##########################-----Wiktionary Functions-----########################
################################################################################

class WiktionaryClient:

    def __init__(self, parse_wiktionary_lock, spider_file="wiktionary_spider.py"):
        self.parse_wiktionary_lock = parse_wiktionary_lock
        self.spider_file = spider_file

    # Hit wiktionary, scrape definition using word and POS
    #
    # Return a sentence graph of the definition
    def lookup_definition_on_wiktionary(
            self,
            word, 
            part_of_speech, 
            wiktionary_root_url=WIKTIONARY_WEB_ROOT_URL,
            use_cache=True):
        if part_of_speech.lower() == 'proper noun':
            word = word[:1].upper() + word[1:].lower()

        print("Looking up %s %s on wiktionary......" % (word, part_of_speech))
        definition_text = self._parse_wiktionary(
            wiktionary_root_url,
            "%s/%s" % (wiktionary_root_url, word), 
            word, 
            part_of_speech, 
            use_cache=use_cache)
        return definition_text

    def _try_acquire_file_lock(self, folder_name, file_name):
        file_path = os.path.join(folder_name, file_name)
        file_path = file_path[:255]
        if os.path.exists(file_path):
            print("file lock acquisition: failed for: %s" % file_path)
            return False
        print("file lock acquisition: attempted for: %s" % file_path)
        os.mknod(file_path)
        print("file lock acquisition: acquired for: %s" % file_path)
        return True

    # Use scrapy to parse the wiktionary url (TODO MAKE THIS COMMENT MORE COMPLETE)
    def _parse_wiktionary(
            self, 
            wiktionary_root_url, 
            wiktionary_url, 
            word, 
            part_of_speech, 
            use_cache=False):
        output_file_path = "definition-cache/scrapy-scrape-test--%s-%s.json"\
            % (word, part_of_speech)
        if not use_cache or not os.path.exists(output_file_path):
            lock_folder_name = "wiktionary-locks"
            lock_file_name = "%s-%s" % (word, part_of_speech)
            lock_file_name = lock_file_name.replace("/", "-slash-")
            self.parse_wiktionary_lock.acquire()
            print("parse_wiktionary_lock: acquired")
            lock_acquired = self._try_acquire_file_lock(lock_folder_name, lock_file_name)
            self.parse_wiktionary_lock.release()
            print("parse_wiktionary_lock: released")
            if lock_acquired:
                print("file lock acquired, running scrapyd.....")
                self._run_scrapyd_spider(
                    wiktionary_root_url, 
                    wiktionary_url, 
                    word, 
                    part_of_speech, 
                    output_file_path)
                self.parse_wiktionary_lock.acquire()
                print("parse_wiktionary_lock: acquired")
                os.remove(os.path.join(lock_folder_name, lock_file_name))
                print("file lock acquisition: released for: %s" % lock_file_name)
                self.parse_wiktionary_lock.release()
                print("parse_wiktionary_lock: released")
            else:
                while not os.path.exists(output_file_path):
                    time.sleep(1)

        print("\n\n\n")
        if not os.path.exists(output_file_path):
            return ""
        with open(output_file_path, 'r') as json_definition_data:
            try:
                definition_data = json.load(json_definition_data)
                print("definition_data: %s" % definition_data)
            except:
                print("ERROR: Could not find definition file at path: %s" 
                    % output_file_path)
                return ""
        return definition_data[0]['definition']

    def _run_scrapyd_spider(self, 
            wiktionary_root_url, 
            urls, 
            word, 
            part_of_speech, 
            output_file_path):
        if not isinstance(urls, types.ListType):
            urls = [urls]
        print(
            "Running scrapyd spider with word: %s part of speech: %s and urls: %s" 
                % (word, part_of_speech, urls))
        subprocess.check_call([
            "scrapy", 
            "runspider", 
            self.spider_file, 
            "-a",
            "root_url=%s" % wiktionary_root_url,
            "-a",
            "urls=%s" % ",".join(urls),
            "-a",
            "word=%s" % word,
            "-a",
            "part_of_speech=%s" % part_of_speech,
            "-a",
            "output_file_path=%s" % output_file_path])

def clear_wiktionary_file_locks(lock_folder="wiktionary-locks"):
    for file in os.listdir(lock_folder):
        os.remove(os.path.join(lock_folder, file))