from multiprocessing import Manager
import json
import os
import os.path
import subprocess
import time
import types

WIKTIONARY_WEB_ROOT_URL = "https://en.wiktionary.org/wiki"
WIKTIONARY_LOCAL_ROOT_URL = ""

MAX_WAIT_ITERATIONS = 60

class WiktionaryClient:
    def __init__(self, parse_wiktionary_lock=None, spider_file="wiktionary_spider.py"):
        self.parse_wiktionary_lock = parse_wiktionary_lock
        self.spider_file = spider_file

    # Hit wiktionary, scrape definition using word and POS
    #
    # Return a sentence graph of the definition
    def lookup_definition(
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
        self.parse_wiktionary_lock.acquire()
        print("parse_wiktionary_lock: acquired")
        file_path = os.path.join(folder_name, file_name)
        file_path = file_path[:255]
        if os.path.exists(file_path):
            print("file lock acquisition: failed for: %s" % file_path)
            self.parse_wiktionary_lock.release()
            return False
        print("file lock acquisition: attempted for: %s" % file_path)
        os.mknod(file_path)
        print("file lock acquisition: acquired for: %s" % file_path)
        self.parse_wiktionary_lock.release()
        print("parse_wiktionary_lock: released")
        return True

    def _release_file_lock(self, folder_name, file_name):
        self.parse_wiktionary_lock.acquire()
        print("parse_wiktionary_lock: acquired")
        os.remove(os.path.join(folder_name, file_name))
        print("file lock acquisition: released for: %s" % file_name)
        self.parse_wiktionary_lock.release()
        print("parse_wiktionary_lock: released")

    # Use scrapy to parse the wiktionary url (TODO MAKE THIS COMMENT MORE COMPLETE)
    def _parse_wiktionary(
            self, 
            wiktionary_root_url, 
            wiktionary_url, 
            word, 
            part_of_speech, 
            use_cache=False):
        output_file_name = "scrapy-scrape-test--%s-%s.json" % (word, part_of_speech)
        output_file_name = output_file_name.replace("/", "-slash-")
        output_file_path = "definition-cache/%s" % output_file_name
        if not use_cache or not os.path.exists(output_file_path):
            lock_folder_name = "wiktionary-locks"
            lock_file_name = "%s-%s" % (word, part_of_speech)
            lock_file_name = lock_file_name.replace("/", "-slash-")
            if self.parse_wiktionary_lock is not None:
                lock_acquired = self._try_acquire_file_lock(lock_folder_name, lock_file_name)
            if lock_acquired or self.parse_wiktionary_lock is None:
                print("file lock acquired, running scrapyd.....")
                self._run_scrapyd_spider(
                    wiktionary_root_url, 
                    wiktionary_url, 
                    word, 
                    part_of_speech, 
                    output_file_path)
                if self.parse_wiktionary_lock is not None:
                    self._release_file_lock(lock_folder_name, lock_file_name)
            else:
                wait_iteration = 0
                while not os.path.exists(output_file_path):
                    time.sleep(1)
                    wait_iteration += 1
                    if wait_iteration >= MAX_WAIT_ITERATIONS:
                        print("ERROR: Timed out waiting for output_file_path: %s" % output_file_path)
                        break

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
        scrapy_command = [
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
            "output_file_path=%s" % output_file_path
        ]
        print(
            "Running scrapyd spider with command: %s" % ' '.join(scrapy_command))
        #subprocess.check_call(scrapy_command)
        process = subprocess.Popen(scrapy_command)
        print("Polling process..... for word, part of speech, has pid: %s: %s, %s" % (word, part_of_speech, process.pid))
        while process.returncode is None:
            process.poll()
            if process.returncode is not None:
                print("returncode: %s" % process.returncode)

def clear_wiktionary_file_locks(lock_folder="wiktionary-locks"):
    for file in os.listdir(lock_folder):
        os.remove(os.path.join(lock_folder, file))