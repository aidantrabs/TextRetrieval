import sys
import os
import requests
import hashlib
import json
from time import sleep
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}

PROXIES = {'http': os.getenv('HTTP_PROXY')}


def session_handler():
    """
    Description:
        Returns a session object and sets the user agent.

    Parameters:
        None
    """
    session = requests.session()
    session.headers.update(HEADERS)
    return session


def get_content(url):
    """
    Description:
        Returns the text content of the page at the given URL.

    Parameters:
        url (str): The URL of the page to retrieve.
    """
    base_url, params = parse_url(url)
    page = get_page(base_url, params)
    if page:
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup


def parse_url(url):
    """
    Description:
        Returns the base URL and parameters of the given URL.

    Parameters:
        url (str): The URL to parse.
    """
    tokens = url.split("?")
    base_url = tokens[0]
    params = {}

    tokens = tokens[1].split("&") if len(tokens) > 1 else []
    for token in tokens:
        key, value = token.split("=")
        params[key] = value

    return base_url, params


def get_page(base_url, params):
    """
    Description:
        Returns the HTML of the page at the given URL.

    Parameters:
        url (str): The URL of the page to retrieve.
    """
    try:
        response = requests.get(base_url, headers=HEADERS,
                                params=params, proxies=PROXIES)
        if (response.ok == 200):
            return response
        else:
            print(response.status_code)

    except:
        return None


def write_raw_data(content, url):
    """
    Description:
        Writes the content to a file with hashed name.

    Parameters:
        content (str): The content to write to the file.
        url (str): The URL of the page to retrieve.
    """
    os.mkdir("data") if not os.path.exists("data") else None
    filename = os.path.join("data", hash_url(url) + ".txt")
    with open(filename, 'w+') as f:
        f.write(content)


def hash_url(url):
    """
    Description:
        Returns the SHA256 hash of the given URL.

    Parameters:
        url (str): The URL to hash.
    """
    return hashlib.sha256(url.encode()).hexdigest()


def print_giraffe():
    """
    Description:
        Prints a giraffe to the command line.

    Parameters:
        None
    """
    print(r"""

                                        ._ o o
                                        \_`-)|_
                                   ,""       \
                                   ,"  ## |   ಠ ಠ.
                              ," ##   ,-\__    `.
                              ,"       /     `--._;)
                         ,"     ## /
                         ,"   ##    /
          """)


def print_loading():
    """
    Description:
        Prints a fully-animated loading bar to the command line.

    Parameters:
        None
    """
    items = list(range(0, 50))
    l = len(items)

    loading(0, l, prefix='Progress:', suffix='Complete', length=l)
    for i, item in enumerate(items):
        sleep(0.09)
        loading(i + 1, l, prefix='Progress:', suffix='Complete', length=l)


def loading(iter, total, prefix='', suffix='', decimals=1, length=100, fill='>'):
    """
    Description:
        A frame of a loading bar for the command line. Yes, I have time on my hands.

    Parameters:
        iter (int): The current iteration.
        total (int): The total number of iterations.
        prefix (str): The prefix to display before the loading bar.
        suffix (str): The suffix to display after the loading bar.
        decimals (int): The number of decimals to display.
        length (int): The length of the loading bar.
        fill (str): The character to use to fill the loading bar.
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iter / float(total)))
    filled_len = int(length * iter // total)
    bar = fill * filled_len + '-' * (length - filled_len)

    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')

    if iter == total:
        print()
