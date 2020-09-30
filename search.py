def get_index_for_word(word, index):
    # returns the index entry for a certain word, if it exists

    if index.get(word):
        return {i[1]: i[0] for i in index.get(word)}
    else:
        return


def print_index_for_word(word, index):
    # gets the index entry for the word if it exists, and prints the output in a pretty way

    result = get_index_for_word(word, index)
    if result:
        base = "{:>5} | {}"
        print()
        print(base.format("Count", "Address"))
        print("-" * 80)
        for page in result:
            print(base.format(result[page], page))
        print()
    else:
        print("No results found in index for {}".format(word))
    return


def search(search_index, terms):
    # searches the index for pages containing all the search terms, rank by count on page

    index_terms = [get_index_for_word(term, search_index) for term in terms]
    search_results = []

    # seeing as we want an intersection, if any of them are empty return no results
    for term in index_terms:
        if term is None:
            return

    # multiply counts together to get index value, if it's not there multiply by 0 to remove the url
    for url in index_terms[0]:
        multiplier = index_terms[0][url]
        for term in index_terms[1:]:
            multiplier *= term.get(url, 0)

        if multiplier:
            search_results.append([url, multiplier])

    # if there's no intersection return nothing
    if not search_results:
        return

    # sort descending by index number and return
    search_results.sort(key=lambda x: x[1], reverse=True)

    return search_results


def print_search_results(index, terms):
    # get search results and print out the urls

    results = search(index, terms)

    if results:
        print("\nSearch results:")
        for result in results:
            print("{}".format(result[0]))
        print("")
    else:
        print("No results for search")
