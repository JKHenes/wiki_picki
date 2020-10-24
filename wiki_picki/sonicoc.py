import sys, http.client, urllib.request, urllib.parse, urllib.error, json

from pprint import pprint

def get_url(domain, url):
    headers = {}
    try:
        conn = http.client.HTTPSConnection(domain)
        conn.request("GET", url, "", headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        return data
    except Exception as e:
        # These are standard elements in every error.
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    # Failed to get data!
    return None

def do_search(query, website):

    search_result = get_url(website, 'api/v1/Search/List?query=' + query)
    if search_result is None:
        #print("No data :(")
        return None

    search_result = search_result.decode("utf-8")
    search_result = json.loads(search_result)
    if not search_result.get("items"):
        #print("No data :(")
        return None

    return search_result

# Searches a website, and tries to find the title, url, and content of the first article it finds. 
def get_info(query,website):


    # Make sure that the query can actually parsed by the get request
    query = urllib.parse.quote_plus(query)

    # Gets the first search result from a query
    search_data = do_search(query, website)

    if search_data is None:
        search_data = do_search(query[0:3], website)
        if search_data is None:
            print("No data for you wahh") # replace this with a random article?
            sys.exit()

    search_data = search_data.get("items")[0]

    article_id = search_data.get("id")
    title = search_data.get("title")
    url = search_data.get("url")

    # Shouuuuld be fine? if there was no data it would've exited out before.
    # Gets the specific article from an article
    article_data = get_url(website, '/api/v1/Articles/AsSimpleJson?id=' + str(article_id))
    article_data = article_data.decode("utf-8")
    article_data = json.loads(article_data)

    text = ""
    # Print out text content of wiki, goes through each 'section'
    for sections in article_data.get("sections"):
        try:
            fragment = sections.get("content")[0].get("text")
            if fragment is not None:
                text += fragment + "\n"
        except IndexError as e:
            pass

    # Debug prints
    #print(title)
    #print(url)
    #print(text[:-1])

    return (title, url, text[:-1])
