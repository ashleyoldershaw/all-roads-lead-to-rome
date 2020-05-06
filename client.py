from scraper import scrape_website, get_sitemap_urls
from search import print_index_for_word, print_search_results
from utils import load_model


def run_client(base_url):
    index = {}

    while True:
        string = input("Global searcher: ")

        if not string:
            continue

        # process the input
        args = [a.strip() for a in string.split()]
        command = args[0]

        if command == "build":
            if len(args) == 2 and args[1] == "force":
                force_download = True
                print("Forcing download")
            else:
                force_download = False

            scrape_website(get_sitemap_urls(base_url), base_url, force_download=force_download)
        elif command == "load":
            index = load_model(base_url)
        elif command == "print":
            if len(args) == 2:
                if index:
                    print_index_for_word(args[1], index)
                else:
                    print("Index is empty")
            else:
                print("Number of words to print must be 1")

        elif command == "find":
            if len(args) > 1:
                print_search_results(index, args[1:])
            else:
                print("Must type in at least one word to search")
        elif command == "quit":
            break
        else:
            print("Bad input: try again")


if __name__ == '__main__':
    website = "http://example.webscraping.com"

    run_client(website)
