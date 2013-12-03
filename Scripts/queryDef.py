def bQuery(search_word, search_query):

    # bind the search variable to the query
    search_query.bind("$word", search_word)

    # print the results of the query
    print(search_query.execute())

    # close the query/session
    search_query.close()
