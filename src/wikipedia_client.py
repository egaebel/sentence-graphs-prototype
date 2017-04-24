from aylienapiclient import textapi

import random
import re

AYLIEN_APP_ID = "7fe8de1d"
AYLIEN_APP_KEY = "ef49f063d5cb17a97f158e43de5f7747"

WIKIPEDIA_ARTICLE_LIST_FILE_PATH = "data/enwiki-latest-all-titles-in-ns0"
WIKIPEDIA_WEB_ROOT_URL = "https://en.wikipedia.org/wiki"
WIKIPEDIA_LOCAL_ROOT_URL = ""

# Scrape all of wikipedia starting at a random page and going up to page_limit
# pages before stopping. If page_limit==0 then all of wikipedia will be scraped.
def scrape_wikipedia(
        wikipedia_root_url=WIKIPEDIA_WEB_ROOT_URL, 
        article_titles_file=WIKIPEDIA_ARTICLE_LIST_FILE_PATH, 
        page_limit=5,
        randomize=False):
    print("Retrieving wikipedia urls....")
    wikipedia_urls_generator = get_all_wikipedia_urls(\
        wikipedia_root_url,
        article_titles_file)

    if randomize:
        print("Randomly selecting wikipedia urls......")
        wikipedia_urls_generator = filter(lambda x: _has_no_strange_characters(x) and random.randint(0, 1000) == 7, wikipedia_urls_generator)

    wikipedia_articles = []
    url_count = 0
    skip_count = 0
    client = _get_aylien_client()
    for url in wikipedia_urls_generator:
        if skip_count < 10000:
            print("Skipping wikipedia url: %s" % url)
            skip_count += 1
            continue
        print("\n\n\n")
        wikipedia_article_body = _strip_wikipedia_citations(\
            get_article_text(client, url))
        print("Scraped article body: %s" % wikipedia_article_body[:100])
        print("\n")
        wikipedia_article_dict = {
            'url': url, 
            'body': wikipedia_article_body, 
            'sentence_graphs': list(),
        }
        wikipedia_articles.append(wikipedia_article_dict)

        url_count += 1
        if page_limit > 0 and url_count >= page_limit:
            break

    return wikipedia_articles

def _has_no_strange_characters(url):
    return url.find("\"") == -1 and url.find("'") == -1 and url.find("$") == -1

# Return a generator that generates all wikipedia article URLs starting from the
# passed URL (for handling local copies of wikipedia or other mirrors) drawing 
# from the passed in article_titles_file to obtain a listing of page titles.
def get_all_wikipedia_urls(wikipedia_root_url, article_titles_file):
    with open(article_titles_file, 'r') as titles_file:
        for line in titles_file:
            yield "%s/%s" % (wikipedia_root_url, line.strip())

# Use Aylien API to get text from URL or full text
#
# Return string with article text
def get_article_text(client, url):
    print("Scraping wikipedia url: ||%s||" % url)
    extracted_results = client.Extract(url)
    print("Extracted results: %s" % extracted_results)
    return extracted_results["article"]

def _get_aylien_client(
        aylien_app_id=AYLIEN_APP_ID, aylien_app_key=AYLIEN_APP_KEY):
    return textapi.Client(aylien_app_id, aylien_app_key)

# Strip Wikipedia citations from the passed in text
# e.g. [27], [309]
def _strip_wikipedia_citations(text):
    return re.sub("\[[0-9]*\]", "", text)

if __name__ == '__main__':
    client = _get_aylien_client()
    print("Article Text: %s" % get_article_text(client, "https://en.wikipedia.org/wiki/Scottish_Hard_Court_Championships"))