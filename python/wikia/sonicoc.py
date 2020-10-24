import sys, http.client, urllib.request, urllib.parse, urllib.error, json

from pprint import pprint


def get_url(domain, url):


  # If you know something might fail - ALWAYS place it in a try ... except
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

if __name__ == '__main__':

    query = "Jake"
    website ='dailylifewithamonstergirl.fandom.com'

    # Make sure that the query can actually parsed by the get request
    query = urllib.parse.quote_plus(query)
    headers = {}
    search_data = get_url(website, 'api/v1/Search/List?query=' + query)
    if search_data is None:
        print("No data :(")
        sys.exit

    search_data = search_data.decode("utf-8")
    search_data = json.loads(search_data)

    final_search = search_data.get("items")[0]

    article_id = final_search.get("id")
    title = final_search.get("title")
    url = final_search.get("url")
    

    # Shouuuuld be fine? if there was no data it would've exited out before.
    article_data = get_url(website, '/api/v1/Articles/AsSimpleJson?id=' + str(article_id))
    article_data = article_data.decode("utf-8")
    article_data = json.loads(article_data)

    text = article_data.get("sections")[1].get("content")[0].get("text")
    print(title)
    print(url)
    print(text)

    #pprint(article_data)
