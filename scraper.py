import os
import random
import re

import requests
from bs4 import BeautifulSoup
from progress.bar import IncrementalBar

from utils import get_filename


def maybe_save_url(url, force_download=False):
    # check if we have the page before downloading it
    if force_download or not os.path.exists(get_filename(url)):
        return save_url(url)
    else:
        return get_filename(url)


def save_url(url):
    # download the contents of a URL to a file with the same path structure
    # print("Downloading: {}".format(url), end='\r')
    response = requests.get(url)

    if response.status_code == 404:
        return
    elif response.status_code != 200:
        print(response.text)
        print(response.status_code)
        print(url)
        raise RuntimeError(response.status_code)

    filename = get_filename(url)

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        f.write(response.text)

    # time.sleep(0.5)

    return filename


def get_links_from_text(html_page):
    # extract all the links from the text, barring some that we don't want

    banned_starters = ["/places/default/edit/", "/places/default/user/",
                       "/places/default/search"]

    soup = BeautifulSoup(html_page, features="html.parser")
    page_links = set()
    for link in soup.findAll('a', attrs={'href': re.compile("^/")}):
        address = link.get('href')
        allowed = not any(address.startswith(starter) for starter in banned_starters)
        if allowed:
            page_links.add(address.rstrip("/"))

    return page_links


def get_links_from_wiki(html_page):
    page_links = set()

    soup = BeautifulSoup(html_page, features="html.parser")

    main = soup.find("div", {"id": "bodyContent"})

    for link in main.findAll('a', attrs={'href': re.compile("^/")}):
        address = link.get('href')
        if ":" not in address:
            page_links.add(address.split("?")[0].split("#")[0].rstrip("/"))
    return page_links


def get_links_from_url(url):
    # extract all the links from this url page

    page = get_filename(url)
    with open(page) as f:
        html_page = f.read()
    return get_links_from_wiki(html_page)


def scrape_page(base_url, new_url, links_to_follow, visited_links, force_download=False):
    filename = maybe_save_url(base_url + new_url, force_download=force_download)

    if filename:
        # if we don't limit this it balloons to huge numbers as Wikipedia has millions of pages!
        if len(links_to_follow) < 20000:
            links_to_follow = (links_to_follow | get_links_from_url(base_url + new_url)) - visited_links
        visited_links.add(new_url)
    return links_to_follow, visited_links


def get_number_of_pages():
    base_dir = os.path.join('..', 'pages', 'en.wikipedia.org', 'wiki')

    return sum(1 for file in os.listdir(base_dir) if
               os.path.isfile(os.path.join(base_dir, file)))


def scrape_website(seeds, base_url, force_download=False):
    # keep scraping and indexing until we run out of links to find
    visited_links = set()
    links_to_follow = set()

    seeds = {"/" + "/".join(seed.split("/")[3:]) for seed in seeds}

    num_pages = get_number_of_pages()
    print(f"{num_pages} pages exist - scraping more!")

    print(f"Going through {len(seeds)} seed urls:")
    bar = IncrementalBar(max=len(seeds))
    for seed in seeds:
        links_to_follow, visited_links = scrape_page(base_url, seed, links_to_follow, visited_links, force_download)
        bar.next()
    bar.finish()

    # repeat until we run out of links (which would mean we've trawled Wikipedia completely!)
    while links_to_follow:
        print(F"Number of pages in queue: {len(links_to_follow): <10}", end='\r')
        new_url = random.sample(links_to_follow, 1)[0]
        links_to_follow.remove(new_url)
        links_to_follow, visited_links = scrape_page(base_url, new_url, links_to_follow, visited_links, force_download)


def get_seed_files():
    with open("seeds.txt", "r") as f:
        seeds = {seed.strip() for seed in f.readlines()}
    return seeds


if __name__ == '__main__':
    seed_urls = get_seed_files()
    scrape_website(seed_urls, "https://en.wikipedia.org")
