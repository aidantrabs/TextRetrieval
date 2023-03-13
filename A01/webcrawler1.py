import argparse
import datetime as dt
from bs4 import BeautifulSoup
from utils import *


def get_dt():
    """
    Description:
        Returns the current date and time.
    """
    return dt.datetime.now()


def crawl_urls(url: str, max_depth: int, rewrite: bool = False, verbose: bool = False, depth:int = 0):
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
    if (not http_resp):
        print("Error. Could not retrieve page.")
        return

    soup = BeautifulSoup(http_resp.text, "html.parser")
    hashed = hash_url(url)
    datetime = get_dt()

    hyperlinks = soup.find_all("a")
    links = [link.get("href") for link in hyperlinks]

    filename = "{}.txt".format(hashed)
    if (not rewrite and os.path.isfile(filename) and verbose):
        print("{},{}".format(url, depth))

    write_raw_data(soup.prettify(), filename)
    with open("crawler1.log", "a") as logs:
        logs.write(f"{hashed}, {url}, {datetime}, {http_resp}\n")

    if (max_depth == 0 and verbose):
        print(f"{url},{depth}")

    for link in links:
        crawl_urls(link, max_depth - 1, rewrite, verbose, depth + 1)

    return


def main():
    """
    Description:
        Main function.

    Usage:
        python webcrawler1.py [options] <initialURL>
    """
    global max_depth

    parser = argparse.ArgumentParser(prog="Web Crawler #1", description="Depth & Logger Crawler.")
    parser.add_argument("max_depth", help="The maximum depth to crawl.", type=int)
    parser.add_argument("--rewrite", help="Rewrite the files.", action="store_true")
    parser.add_argument("--verbose", help="Print the URLs as they are crawled.", action="store_true")
    parser.add_argument("url", help="The URL to crawl.", type=str)
    args = parser.parse_args()

    if (not args.max_depth):
        print("Error. No max depth argument provided.")
        return

    elif (args.max_depth < 0):
        print("Error. Max depth must be greater than or equal to 0.")
        return

    if (not args.url):
        print("Error. No URL argument provided.")
        return

    session_handler()
    print_giraffe()
    print_loading()

    crawl_urls(args.url, args.max_depth, args.rewrite, args.verbose)
    return


if (__name__ == "__main__"):
    main()
