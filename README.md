# Country search engine

This code is for a Web Services and Web Data coursework.

##Setting up

How to use the system.

1. Run the client

    ```bash
    python client.py
    ```
    
2. If you have already run this command, you can skip this step.
   
   Run the build function (force option included to force re-downloading the files)

    ```
    build [force]
    ```
    
    This command should take a while the first time as we are observing a politeness window of 5 seconds between each request. After the first time it's been run it will only download the files it doesn't have unless you choose the force option.
    
3. Run the load function to load in the index

    ```
    load
    ```
    
Now you have built the index and loaded it up, you can now use the search engine.

##Using the search engine:

To use the search engine use these commands:

####Searching the page
```
find <words>
```

Type in words to show all the pages containing all of the words you list. There is no upper bound to the number of words you can use but you may find that there are 0 pages with all of them in.

####Printing the index for a word

```
print <word>
```

Lists all the pages containing that word and how many times it appears in that page.