import os
import re
import time

import requests
import xmltodict
from bs4 import BeautifulSoup

from indexer import add_page_to_index, sort_and_store_index
from utils import get_filename


def maybe_save_url(url, force_download = False):
    # check if we have the page before downloading it
    if force_download or not os.path.exists(get_filename(url)):
        return save_url(url)
    else:
        return get_filename(url)


def save_url(url):
    # download the contents of a URL to a file with the same path structure
    print("Downloading: {}".format(url))
    response = requests.get(url)

    filename = get_filename(url)

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        f.write(response.text)

    time.sleep(5)

    return filename


def get_sitemap_urls(url):
    # this scrapes the sitemap for the website urls stored inside it

    contents = requests.get(url + "/sitemap.xml")
    urls = xmltodict.parse(contents.text)

    website_queue = []

    for r in urls["urlset"]["url"]:
        page_url = r["loc"]
        website_queue.append(page_url)

    return website_queue


def get_links_from_text(html_page):
    # extract all the links from the text, barring some that we don't want

    banned_starters = ["/places/default/edit/", "/places/default/user/",
                       "/places/default/search"]

    soup = BeautifulSoup(html_page, features="html.parser")
    page_links = set()
    for link in soup.findAll('a', attrs={'href': re.compile("^/")}):
        address = link.get('href')
        allowed = True
        for starter in banned_starters:
            if address.startswith(starter):
                allowed = False
        if allowed:
            page_links.add(address.rstrip("/"))

    return page_links


def get_links_from_url(url, force_download = False):
    # extract all the links from this url page

    page = get_filename(url)
    with open(page) as f:
        html_page = f.read()
    return get_links_from_text(html_page)


def scrape_website(seeds, base_url, force_download = False):
    # keep scraping and indexing until we run out of links to find

    # to keep track of what we need to find and where we're going
    links_to_follow = set(["/" + "/".join(seed.split("/")[3:]) for seed in seeds])
    visited_links = set()
    index = {}

    # repeat until we run out of links
    while links_to_follow:
        print("Number of pages in queue: {}".format(len(links_to_follow)))
        new_url = links_to_follow.pop()
        visited_links.add(new_url)

        maybe_save_url(base_url + new_url, force_download=force_download)

        links_to_follow = (links_to_follow | get_links_from_url(base_url + new_url, force_download = force_download)) - visited_links
        add_page_to_index(base_url + new_url, index)

    # save the list of pages we've got
    with open(get_filename(base_url + "/scraped_pages.txt"), "w") as f:
        f.write(base_url + "\n{}".format(base_url).join(sorted(visited_links)))

    sort_and_store_index(index, base_url)
