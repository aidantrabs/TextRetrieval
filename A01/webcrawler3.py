import sys
import requests
import hashlib
import json
import re
import matplotlib.pyplot as mpl
from time import sleep
from bs4 import BeautifulSoup
from common import *

HTML_TAGS_REGEX = r"/<\/?[^>]+(>|$)/gm"
HTML_CONTENT_REGEX = r"/<[^>]+>/gm"

def replace_html(text):
    """
     Description:
          Returns the text with HTML tags removed.

     Parameters:
          text (str): The text to remove HTML tags from.
     """
    return re.sub(HTML_TAGS_REGEX, '', re.sub(HTML_CONTENT_REGEX, '', text))


def graph(text):
    """
    x
    """
    tokens = text.count("0")
    tags = text.count("1")
    N = tokens + tags

    plt.plot([token_count], [tag_count])
    plt.title('Content Block')
    plt.xlabel('Token count')
    plt.ylabel('Tag count')
    plt.show()


def generate_heatmap(bits):
    """
    x
    """
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
     content = get_content(url).prettify()

     if content:
          write_raw_data(content, url)
     else:
          print("Error. Unable to retrieve this flaming heap of garbage.")


if __name__ == "__main__":
    main()
