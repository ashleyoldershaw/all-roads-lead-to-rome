import csv
import difflib
import os

from progress.bar import IncrementalBar

from scraper import get_links_from_wiki
from utils import get_nice_name, get_filename


def generate_database():
    explored_pages = set()
    base_dir = os.path.join('pages', 'en.wikipedia.org', 'wiki')
    base_url = 'https://en.wikipedia.org'

    files = [os.path.join(base_dir, file) for file in os.listdir(base_dir) if
             os.path.isfile(os.path.join(base_dir, file))]

    bar = IncrementalBar(max=len(files) / 100)
    counter = 0

    if os.path.exists('links.csv'):
        with open('links.csv', 'r') as f:
            for i in f.readlines():
                from_page = i.split(',')[0]
                explored_pages.add(from_page)
    for page in files:
        counter += 1
        if counter % 100 == 0:
            bar.next()
        if get_nice_name(page) in explored_pages:
            continue
        with open(page, 'r') as f:
            links = get_links_from_wiki(f.read())

        for link in links:
            new_url = os.path.join(base_url + link)

            file_location = get_filename(new_url)

            if os.path.isfile(file_location) and os.path.dirname(file_location) == base_dir:
                with open('links.csv', 'a+') as f:
                    f.write(f"\"{get_nice_name(page)}\",\"{get_nice_name(link)}\"\n")
    bar.finish()


def sort_and_refresh_database():
    with open('links.csv', 'r') as f:
        lines = sorted(list(set(f.readlines())))
    with open('links.csv', 'w') as f:
        for line in lines:
            f.write(line)


def load_database():
    with open('links.csv', 'r') as f:
        graph = {}
        reader = csv.reader(f)
        for line in reader:
            origin = line[0]
            destination = line[1]
            if origin not in graph:
                graph[line[0]] = set()
            graph[origin].add(destination)
    return graph


def breadth_first_search_through_dict(wiki_graph, start):
    # finds shortest path between 2 nodes of a graph using BFS
    # adapted from an example found online

    if start in wiki_graph:
        start_node = start
    else:
        matches = difflib.get_close_matches(start, wiki_graph.keys())
        if matches:
            print(f"Not found - using closest match ({matches[0]})")
            start_node = matches[0]
        else:
            return f"No match for {start} found"

    queue = [[start_node]]

    goal = "Rome"
    explored = []

    # return path if start is goal
    if start == goal:
        return [goal]

    # keeps looping until all possible paths have been checked
    while queue:
        # pop the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        if node not in explored:
            try:
                neighbours = wiki_graph[node]
            except:
                continue
            # go through all neighbour nodes, construct a new path and
            # push it into the queue
            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)
                # return path if neighbour is goal
                if neighbour == goal:
                    return new_path

            # mark node as explored
            explored.append(node)

    # in case there's no path between the 2 nodes
    return "A connecting path does not exist, try building the network up more or adding the URL " \
           "of the page you want to link to the seeds.txt"
