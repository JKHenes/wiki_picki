import sys, http.client, urllib.request, urllib.parse, urllib.error, json, re, random

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

def get_random_chara(): #THIS IS SPECIFIC TO THE SONIC WEBSITE
    id = [149610, 171415,20601,84540,172886,174980,146592,145006,3177,175147,3689,36402,175143,13739,148487] 
    return random.choice(id)

def sonic_name_matcher(result): # ALSO SPECIFIC TO SONIC
    name_rx = "\\w+ [tT]he \\w+"
    matcher = None
    for items in result.get("items"):
        matcher = re.match(name_rx,str(items.get("title")))
        if matcher:
            result = items
            break

    # if you cant find a match get a random article
    if matcher is not None:
        article_id = result.get("id")
    else:
        article_id = get_random_chara()

    return result, article_id

# Searches a website, and tries to find the title, url, and content of the first article it finds. 
def get_info(query,website):

    # Make sure that the query can actually parsed by the get request
    query = urllib.parse.quote_plus(query)

    # Gets the first search result from a query
    search_data = do_search(query, website)

    if website == "sonicfanchara.fandom.com": # Specific Sonic character parsing
        search_data,article_id = sonic_name_matcher(search_data)
    else:                                     # Generic approach: will just select the first article 
        search_data = search_data.get("items")[0]
        article_id = search_data.get("id")
    
    # Shouuuuld be fine? if there was no data it would've exited out before.
    # Gets the specific article from an article
    article_data = get_url(website, '/api/v1/Articles/AsSimpleJson?id=' + str(article_id))
    article_data = article_data.decode("utf-8")
    article_data = json.loads(article_data)

    title = article_data.get("sections")[0].get("title")
    url = "https://"+ website + "/" + title.replace(" ", "_")

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
