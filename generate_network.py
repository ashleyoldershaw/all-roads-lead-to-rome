from all_roads_lead_to_rome import sort_and_refresh_database, load_database, generate_routes_to_rome
from visualise import generate_gephi_files

if __name__ == '__main__':
    # sort_and_refresh_database()
    graph = load_database()
    generate_routes_to_rome(graph)
    generate_gephi_files()
