import sys
import requests
import hashlib
import json
import re
import matplotlib.pyplot as mpl
from time import sleep
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}

HTML_TAGS_REGEX = r"/<\/?[^>]+(>|$)/gm"
HTML_CONTENT_REGEX = r"/<[^>]+>/gm"


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
        tokens = url.split("?")
        baseUrl = tokens[0]
        params = {}

        tokens = tokens[1].split("&")
        for token in tokens:
            key, value = token.split("=")
            params[key] = value

        print(params)
        response = requests.get(baseUrl, headers=HEADERS, params=params)
        print(toString(response))
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


def replace_html(text):
    """
     Description:
          Returns the text with HTML tags removed.

     Parameters:
          text (str): The text to remove HTML tags from.
     """
    return re.sub(HTML_TAGS_REGEX, '', re.sub(HTML_CONTENT_REGEX, '', text))


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


def graph(text):
    tokens = text.count("0")
    tags = text.count("1")
    N = tokens + tags

    plt.plot([token_count], [tag_count])
    plt.title('Content Block')
    plt.xlabel('Token count')
    plt.ylabel('Tag count')
    plt.show()

"""
x
"""
def generate_heatmap(bits):
    max_tags = 0
    heatmap = np.zeros((len(bits), len(bits)))
    for i in range(len(bits)):
        for j in range(i, len(bits)):
            tags_before = sum(bits[:i])
            tags_after = sum(bits[j:])
            # non_tags_between = j - i - sum(bits[i:j])

            # middle part of the summation in the slides
            f = 0
            for b in bits[i:j]:
                f += (1 - b)

            total_tags = tags_before + f + tags_after
            heatmap[i, j] = total_tags

            # X.append(i)
            # Y.append(j)
            # Z.append(total_tags)

    plt.imshow(heatmap, cmap='hot', interpolation='nearest', origin='lower')
    plt.show()

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
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iter / float(total)))
    filled_len = int(length * iter // total)
    bar = fill * filled_len + '-' * (length - filled_len)

    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')

    if iter == total:
        print()


def main():
     """
     Description:
          Main function.

     Usage:
          python webcrawler2.py <url>
     """
     try:
          url = sys.argv[1]
     except:
          print("Error. No URL argument provided.")

     print_giraffe()
     print_loading()
     content = get_content(parse_url(url)).prettify()

     if content:
          write_raw_data(content, url)
     else:
          print("Error. Unable to retrieve this flaming heap of garbage.")


if __name__ == "__main__":
    main()
