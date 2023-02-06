import sys
import requests
import hashlib
import json
from time import sleep
from bs4 import BeautifulSoup

HEADERS = {
     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}

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

def get_page(url):
     """
     Description:
          Returns the HTML of the page at the given URL.

     Parameters:
          url (str): The URL of the page to retrieve.
     """
     try:
          response = requests.get(url, headers=HEADERS)
          if response.status_code == 200:
               return response
          else:
               print(response.status_code)
               return None
     except:
          return None


def get_content(url):
     """
     Description:
          Returns the text content of the page at the given URL.

     Parameters:
          url (str): The URL of the page to retrieve.
     """
     page = get_page(url)
     if page:
          soup = BeautifulSoup(page.content, 'html.parser')
          return soup


def write_raw_data(content, url):
     """
     Description:
          Writes the content to a file with hashed name.

     Parameters:
          content (str): The content to write to the file.
          url (str): The URL of the page to retrieve.
     """
     filename = 'data/' + hash_url(url) + '.txt'
     with open(filename, 'w') as f:
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
     items = list(range(0, 50))
     l = len(items)

     loading(0, l, prefix='Progress:', suffix='Complete', length=l)
     for i, item in enumerate(items):
          sleep(0.09)
          loading(i + 1, l, prefix='Progress:', suffix='Complete', length=l)


def loading(iter, total, prefix='', suffix='', decimals=1, length=100, fill='>'):
     """
     Description:
          A loading bar for the command line. Yes, I have time on my hands.

     Parameters:
          iter (int): The current iteration.
          total (int): The total number of iterations.
          prefix (str): The prefix to display before the loading bar.
          suffix (str): The suffix to display after the loading bar.
          decimals (int): The number of decimals to display.
          length (int): The length of the loading bar.
          fill (str): The character to use to fill the loading bar.
     """
     percent = ("{0:." + str(decimals) + "f}").format(100 * (iter / float(total)))
     filled_len = int(length * iter // total)
     bar = fill * filled_len + '-' * (length - filled_len)

     print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = '\r')

     if iter == total:
          print()
