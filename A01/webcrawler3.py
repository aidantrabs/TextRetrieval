import argparse
import matplotlib.pyplot as mpl
import numpy as np
import re
from utils import *

# Matches all content in an HTML doc that isn't an HTML tag.
HTML_CONTENT_REGEX = r"\b\w+\b(?![^<]*>)"

# Matches all HTML tags in a document.
HTML_TAGS_REGEX = r"<[^<]+?>"

# Matches all non-binary characters.
NON_ZERO_ONE_REGEX = r"[^01]+"

def replace_html(text: str):
    """
    Description:
        Returns the text with HTML tags removed.

    Parameters:
        text (str): The text to remove HTML tags from.
    """
    a = re.sub(HTML_CONTENT_REGEX, "0", text)
    b = re.sub(HTML_TAGS_REGEX, "1", a)
    c = re.sub(NON_ZERO_ONE_REGEX, "", b)
    
    return c

def optimise_webpage(bits: list):
    """
    Description:
        Returns the optimal range of content to display on a webpage.

    Parameters:
        bits (list): A list of 0s and 1s representing the content of a document.
    """
    n = len(bits)
    max_tags, i_prime, j_prime = 0, 0, 0
    for i in range(n):
        for j in range(i, n):
            a = sum(bits[:i])
            b = sum(bits[j:])
            f = 0
            for bit in bits[i:j]:
                f += (1 - bit)

            total = a + f + b
            if (total > max_tags):
                max_tags = total
                i_prime = i
                j_prime = j

    return i_prime, j_prime

def generate_heatmap(bits: list):
    """
    Description:
        Generates a heatmap of the number of tags in a document.

    Parameters:
        bits (list): A list of 0s and 1s representing the content of a document.
    """
    b = len(bits)
    heatmap = np.zeros((b, b))

    for i in range(b):
        for j in range(i, b):
            a = sum(bits[:i])
            b = sum(bits[j:])
            f = 0
            for bit in bits[i:j]:
                f += (1 - bit)

            heatmap[i, j] = a + f + b

    mpl.imshow(heatmap, cmap='hot', interpolation='nearest', origin='lower')
    mpl.show()

    return

def get_optimised_content(content: str, i: int, j: int):
    """
    Description:
        Returns the content of a document between the given indices.

    Parameters:
        content (str): The content of the document.
        i (int): The starting index.
        j (int): The ending index.

    Returns:
        str: The content of the document between the given indices.
    """
    split_content = re.split(HTML_TAGS_REGEX, content)

    return " ".join(split_content[i:j])

def main():
    """
    Description:
        Main function.

    Usage:
        python3 webcrawler3.py <url>
    """
    parser = argparse.ArgumentParser(prog="Web Crawler #3", description="Tag & Graph Crawler.")
    parser.add_argument("url", help="The URL of the webpage to crawl.")
    args = parser.parse_args()

    if (not args.url):
        print("Error. No URL argument provided.")
        return

    session_handler()
    print_giraffe()
    print_loading()

    url = args.url
    raw_content = str(get_content(url))
    content = replace_html(raw_content)

    if (content):
        bits = [int(x) for x in content]
        i, j = optimise_webpage(bits)
        print("D")
        print("Optimal range (i^*, j^*): {} to {}".format(i, j))

        optimised_content = get_optimised_content(raw_content, i, j)
        write_raw_data(optimised_content, url)
        generate_heatmap(bits)
    else:
        print("Error. Unable to retrieve this flaming heap of garbage.")

    return

if (__name__ == "__main__"):
    main()