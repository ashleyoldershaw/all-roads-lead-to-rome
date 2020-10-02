from all_roads_lead_to_rome import generate_database, sort_and_refresh_database, load_database, \
    breadth_first_search_through_dict
from scraper import scrape_website, get_seed_files


def run_client(base_url):
    index = {}

    print("There's an old saying that all roads lead to Rome. I wanted to know how long those roads are on Wikipedia.")
    graph = {}

    while True:
        string = input("Input command: ")

        if not string:
            continue

        # process the input
        args = [a.strip() for a in string.split()]
        command = args[0]

        if command == "scrape":
            if len(args) == 2 and args[1] == "force":
                force_download = True
                print("Forcing download")
            else:
                force_download = False

            seed_urls = get_seed_files()
            scrape_website(seed_urls, "https://en.wikipedia.org", force_download=force_download)

        elif command == "build":
            generate_database()
            sort_and_refresh_database()

        elif command == "load":
            graph = load_database()

        elif command == "find":
            if graph == {}:
                print("Load the graph with the \"load\" command first!")
                continue
            if len(args) > 1:
                print(breadth_first_search_through_dict(graph, string[5:]))
            else:
                print("Must type in a term to search!")

        elif command == "quit":
            break

        elif command == "help":
            print("Read the README.md file!")

        else:
            print("Bad input: try again")


if __name__ == '__main__':
    website = "http://example.webscraping.com"

    run_client(website)
