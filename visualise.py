import csv

from all_roads_lead_to_rome import load_database


def generate_gephi_files():
    graph = load_database('links_to_rome.csv')
    nodes = {}
    counter = 0

    nodes['Rome'] = 0
    for node in graph:
        if node not in nodes:
            counter += 1
            nodes[node] = counter

    with open('nodes.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Label'])
        for node in nodes:
            writer.writerow([nodes[node], node])

    with open('edges.csv', 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['Source', 'Target'])
        for source in graph:
            for target in graph[source]:
                try:
                    writer.writerow([nodes[source], nodes[target]])
                except KeyError:
                    pass


if __name__ == '__main__':
    generate_gephi_files()
