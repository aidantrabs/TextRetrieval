import sys
from bs4 import BeautifulSoup
from utils import *
import datetime as dt

def get_dt():
    """
    Description:
        Returns the current date and time.
    """
    return dt.datetime.now()

def crawl_urls(url, max_depth, rewrite=False, verbose=False, depth=0):
    """
    Description:
        Crawls the given URL and all of its hyperlinks.

    Parameters:
        url (str): The URL to crawl.
        max_depth (int): The maximum depth to crawl.
        rewrite (bool): Whether to rewrite the files.
        verbose (bool): Whether to print the URLs as they are crawled.
        depth (int): The current depth of the crawler.
    """
    http_resp = get_page(url, {})
    
    if not http_resp:
        return

    soup = BeautifulSoup(http_resp.text, 'html.parser')
    hashed = hash_url(url)
    datetime = get_dt()
    
    hyperlinks = soup.find_all('a')
    links = [link.get('href') for link in hyperlinks]

    filename = "{}.txt".format(hashed)
    if not rewrite and os.path.isfile(filename):
        if verbose:
            print("{},{}".format(url, depth))
    
    write_raw_data(soup.prettify(), filename)

    with open('crawler1.log', 'a') as logs:
        logs.write(f"{hashed}, {url}, {datetime}, {http_resp}\n")

    if max_depth == 0:
        if verbose:
            print(f"{url},{depth}")

    for link in links:
        crawl_urls(link, max_depth - 1, rewrite, verbose, depth + 1)

def main():
    """
    Description:
        Main function.

    Usage:
        python webcrawler1.py [options] <initialURL>
    """
    global max_depth

    try:
        url = sys.argv[-1]
    except:
        print("Error. No URL argument provided.")
        
    try:
        max_depth = int(sys.argv[1])
    except:
        print("Error. Need to provide a max depth.")

    rewrite = '--rewrite' in sys.argv
    verbose = '--verbose' in sys.argv

    session_handler()
    print_giraffe()
    print_loading()

    crawl_urls(url, max_depth, rewrite, verbose)

if __name__ == "__main__":
     main()