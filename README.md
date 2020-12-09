# All roads lead to Rome!

There's an old saying that all roads lead to Rome. There's also a concept that every actor has a "Bacon Number" where 
you see how many degrees of separation an actor is from Kevin Bacon.

Seeing as Wikipedia is the largest encyclopedia in the world, I thought I'd apply both ideas to Wikipedia, and come up
with how long it takes to get to Rome from whatever page you like on Wikipedia.

This was done for a bit of fun, and adapted from a uni coursework. I've been out of work and wanted to play with some
new concepts and tools and I've learned a bit from this which has been useful. This has its limitations but it's just a
bit of fun. I'll get to that later in this README.

## Setting up

How to use the system.

1. Set up seed URLs (should be Wikipedia pages otherwise it's not going to work)
    1. Open `seeds.txt`
    1. Type in seed urls - examples are given of `https://en.wikipedia.org/wiki/Rome` for obvious reasons and a few
    others because they'll mix things up a bit

1. Run the client

    ```bash
    python client.py
    ```
    
1. If you have already run this command, you can skip this step.
   
   Run the scrape function (force option included to force re-downloading the files (not recommended))

    ```
    scrape [force]
    ```
    
    Wikipedia doesn't seem to mind if there is no wait period so we should get files quite quickly. After the first time
    it's been run it will only download the files it doesn't have unless you choose the force option. If Wikipedia does
    send a 429 Too Many Requests message we stop immediately.
    
1. Run the build function to build the graph

    ```
    build
    ```
    
There will be a progress bar that will let you know how far through you are. When you have built the graph, you can load
it up.

## Using the search engine:

To begin you must load up the search engine by using the `load` command:
```bash
load
```

To use the search engine use the `find` command:

```
find <page name>
```

Type in words to find the link to that page and Rome - if it's not there it'll try and find the closest name there.

## Notes

Scraping might not be the best option for Wikipedia in general, as data dumps of Wikipedia are available. This is true
but we can transfer this to other websites for similar purposes if you want which is the reason I kept the scraper
rather than building a new thing from scratch

There are areas for improvement that I will acknowledge:

- The building of the model with the `build` command is time consuming and requires a lot of resources
- Finding the most relevant word isn't always the best, for example 'Rome' and 'rome' seem like an obvious match, but
the difflib library thinks that 'Jerome' is closer because it contains all the same letters
