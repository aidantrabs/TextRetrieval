import sys
import requests
from bs4 import BeautifulSoup
from utils import *
import datetime as dt

def get_dt():
    """
    Description: 
        get the download datetimes for each URL in the given page.

    Usage:
        dt = get_dt()
    """
    return dt.datetime.now()

def crawl_urls(url, max_depth=0, rewrite=False, verbose=False, depth=0):
    """
    Description:
        Extracts all URLs from the given page.
    
    Usage:
        extract_urls(url)
    """
    soup = get_content(url)
    hashed = hash_url(url)
    dt = get_dt()
    http_resp = get_page(url)
    
    hyperlinks = soup.find_all('a', href=True)
    links = []
    for link in hyperlinks:
        links.append(link)

    filename = f"{hashed}.txt"
    if not rewrite and os.path.isfile(filename):
        if verbose:
            print(f"{url},{depth}")
        return

    with open('crawler1.log', 'a') as logs:
        logs.write(f"{hashed}, {url}, {dt}, {http_resp}\n")

    if max_depth == 0:
        if verbose:
            print(f"{url},{depth}")
        return
    for link in links:
        crawl_urls(link, max_depth-1, rewrite, verbose, depth+1)
    
    return   

def main():
    """
    Description:
        Main function.

    Usage:
        python webcrawler1.py [options] <initialURL>
    """
    try:
          url = sys.argv[1]
    except:
          print("Error. No URL argument provided.")
     
    session_handler()
    print_giraffe()
    print_loading()
    content = get_content(url).prettify()

    if content:
        write_raw_data(content, url)
    else:
        print("Error. Unable to retrieve this flaming heap of garbage.")
    
    crawl_urls(url)

if __name__ == "__main__":
     main()