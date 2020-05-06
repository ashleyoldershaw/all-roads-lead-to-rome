import json
from collections import Counter
from string import ascii_letters

from bs4 import BeautifulSoup, Comment

from utils import get_filename


def tag_visible(element):
    # returns true if the text is visible, false if not

    invisible_tags = 'style', 'script', 'head', 'title', 'meta', '[document]'
    if element.parent.name in invisible_tags:
        return False
    if isinstance(element, Comment):
        return False
    return True


def get_all_words(text):
    # get all the visible words in the text, ignoring all numbers etc

    # set of allowed characters
    allowed = set(ascii_letters + " ")

    soup = BeautifulSoup(text, 'html.parser')
    texts = soup.findAll(text=True)

    # filter out all the non-visible text
    visible_text = filter(tag_visible, texts)

    # very pythonic, get all strings out of the list, just using the allowed characters
    strings = [''.join(l for l in v if l in allowed).strip() for v in visible_text if v.strip()]

    # stick all the strings together and then separate out by whitespace giving a 1d list of all the words
    return [string for string in " ".join(t.strip() for t in strings).split(" ") if string]


def get_page_index(url):
    # group all the words in the list to a dictionary, have the value the count of the occurrences of each word

    with open(get_filename(url)) as f:
        contents = f.read()

    words = get_all_words(contents)

    grouping = dict(Counter(words))

    return grouping


def add_word_to_index(entry, word, url, full_index):
    # add the word from a page to the reverse index, putting together the count and the url into the words value
    # in the dictionary

    if not full_index.get(word):
        full_index[word] = [(entry[word], url)]
    else:
        full_index[word].append((entry[word], url))


def add_page_to_index(url, index):
    # get the page of the url, add them up and put them in the index

    # ignore pages with certain url patterns
    non_indexed_pages = ["iso", "index"]
    for page in non_indexed_pages:
        if url.split("/")[-2] == page or url.split("/")[-1] == page:
            return

    entry = get_page_index(url)

    for word in entry:
        add_word_to_index(entry, word, url, index)


def sort_and_store_index(index, base_url):
    # sorts the index entries from highest to lowest and writes it to the index file

    for item in index:
        index[item].sort(key=lambda x: x[0], reverse=True)

    with open(get_filename(base_url + "/indices.json"), "w") as f:
        f.write(json.dumps(index))


def fully_index_from_scraped_files(base_url):
    # for testing, looks in the scraped pages list and creates a reverse index

    full_index = {}

    with open(get_filename(base_url + "/scraped_pages.txt"), "r") as f:
        pages = f.read().splitlines()

    for page in pages:
        add_page_to_index(page, full_index)

    sort_and_store_index(full_index, base_url)

    return full_index
