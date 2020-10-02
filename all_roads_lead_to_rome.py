import csv
import difflib
import os

import more_itertools
from progress.bar import IncrementalBar

from scraper import get_links_from_wiki
from utils import get_nice_name, get_filename


def generate_database():
    explored_pages = set()
    relations = set()
    base_dir = os.path.join('..', 'pages', 'en.wikipedia.org', 'wiki')
    base_url = 'https://en.wikipedia.org'

    files = [os.path.join(base_dir, file) for file in os.listdir(base_dir) if
             os.path.isfile(os.path.join(base_dir, file))]

    bar = IncrementalBar(max=len(files))

    # caching functions as they're being called a lot
    nice_name = get_nice_name
    get_wiki_links = get_links_from_wiki
    filename = get_filename
    for page in files:
        bar.next()
        if nice_name(page) in explored_pages:
            continue
        with open(page, 'r') as f:
            links = get_wiki_links(f.read())

        for link in links:
            new_url = os.path.join(base_url + link)

            file_location = filename(new_url)

            if os.path.isfile(file_location) and os.path.dirname(file_location) == base_dir:
                relations.add((nice_name(page), nice_name(link)))
    bar.finish()

    with open('links.csv', 'w') as f:
        writer = csv.writer(f)
        for relation in relations:
            writer.writerow(relation)


def sort_and_refresh_database():
    with open('links.csv', 'r') as f:
        lines = sorted(list(set(f.readlines())))
    with open('links.csv', 'w') as f:
        for line in lines:
            f.write(line)


def load_database(filename='links.csv'):
    count = len(open(filename, 'r').readlines())
    print(f"Loading up {count} relations")
    with open(filename, 'r') as f:
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
            print(f"No match for {start} found")
            return []

    queue = [[start_node]]

    goal = "Rome"
    explored = []

    if start == goal:
        return [goal]

    while queue:
        # the breadth first search bit:
        # get the latest node and look for the goal, if it's not there add the nodes we can see to the queue
        path = queue.pop(0)
        node = path[-1]

        if node not in explored:
            try:
                neighbours = wiki_graph[node]
            except KeyError:
                # sometimes a node doesn't point to any other nodes in the set
                continue
            for neighbour in neighbours:
                # build a new path out for each neighbour and add it to the queue
                # if we reach the goal, return what we have
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)

                if neighbour == goal:
                    return new_path

            # mark node as explored
            explored.append(node)

    # in case there's no path between the 2 nodes
    print(f"A connecting path from {start_node} to {goal} not exist, try building the network up more or adding the "
          f"URL of the page you want to link to the seeds.txt")
    return []


def generate_routes_to_rome(wiki_graph):
    # this function goes through the whole graph and generates the path to Rome for each node, i.e. choosing all the
    # links from links.txt which direct us to Rome.
    links = set()
    counter = 0
    bar = IncrementalBar(max=len(wiki_graph))
    for node in wiki_graph:
        link = breadth_first_search_through_dict(wiki_graph, node)
        paths = more_itertools.pairwise(link)
        for path in paths:
            links.add(path)
        bar.next()
    bar.finish()

    with open("links_to_rome.csv", 'w') as f:
        writer = csv.writer(f)
        for link in links:
            writer.writerow([link[0], link[1]])


def get_longest_paths():
    graph = load_database('links_to_rome.csv')
    paths = set()
    for node in graph:
        paths.add(tuple(breadth_first_search_through_dict(graph, node)))
    max_path = len(max(paths, key=lambda x: len(x)))
    print(max_path)
    long_paths = {x for x in paths if len(x) == max_path}
    for path in long_paths:
        print(path)
    return long_paths


if __name__ == '__main__':
    get_longest_paths()
