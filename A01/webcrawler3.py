import sys
import regex as re
import numpy as np
import matplotlib.pyplot as mpl
from utils import *

# Matches all content in an HTML doc that isn't an HTML tag.
HTML_CONTENT_REGEX = r"\b\w+\b(?![^<]*>)"

# Matches all HTML tags in a document.
HTML_TAGS_REGEX = r"<[^<]+?>"

# Matches all non-binary characters.
ZERO_ONE_REGEX = r"[^01]+"


def replace_html(text):
    """
    Description:
        Returns the text with HTML tags removed.

    Parameters:
        text (str): The text to remove HTML tags from.
     """
    return re.sub(ZERO_ONE_REGEX, "",
                  re.sub(HTML_TAGS_REGEX, "1",
                         re.sub(HTML_CONTENT_REGEX, "0", text)))


def graph(text):
    """
    x
    """
    tokens = text.count("0")
    tags = text.count("1")
    N = tokens + tags

    mpl.plot([tokens], [tags])
    mpl.title('Content Block')
    mpl.xlabel('Token count')
    mpl.ylabel('Tag count')
    mpl.show()


# def generate_heatmap(bits):
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

    mpl.imshow(heatmap, cmap='hot', interpolation='nearest', origin='lower')
    mpl.show()


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

    mpl.imshow(heatmap, cmap='hot', interpolation='nearest', origin='lower')
    mpl.show()


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

    # session_handler()
    # print_giraffe()
    # print_loading()
    content = replace_html(get_content(url))
    generate_heatmap([int(x) for x in content])
    if content:
        write_raw_data(content, url)
    else:
        print("Error. Unable to retrieve this flaming heap of garbage.")


if __name__ == "__main__":
    main()
