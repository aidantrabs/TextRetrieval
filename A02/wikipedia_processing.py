import argparse
import json
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os
import string
import scipy.interpolate
import sys
from typing import List, Tuple

DATA_DIRECTORY = "./data_wikipedia"
DATA_FILE_ENCODING = "utf-8"


class Parameters:
    """
    Description:
        A class to hold the parameters for the wikipedia processing script.

    Attributes:
        zipf: Whether or not to perform Zipf's law.
        tokenize: Whether or not to perform tokenization.
        stopword: Whether or not to perform stopword removal.
        stemming: Whether or not to perform stemming.
        invertedIndex: Whether or not to perform inverted index creation.
    """
    zipf: bool
    tokenize: bool
    stopword: bool
    stemming: bool
    invertedIndex: bool

    def __init__(self, zipf: bool, tokenize: bool, stopword: bool, stemming: bool, invertedIndex: bool):
        self.zipf = zipf
        self.tokenize = tokenize
        self.stopword = stopword
        self.stemming = stemming
        self.invertedIndex = invertedIndex
        return


def get_full_merged_string(params: Parameters):
    """
    Description:
        Processes all files in the data directory, and compiles all the
        "text" attributes of the JSON objects in the files into a single
        cleaned string.

    Parameters:
        params (Parameters): The parameters for the script.

    Returns:
        (str): The merged lower-case string with punctuation removed.
    """
    text = ""
    for fileName in os.listdir(DATA_DIRECTORY):
        properFileName = os.path.join(DATA_DIRECTORY, fileName)
        if(not os.path.isfile(properFileName)):
            continue

        text += get_file_merged_string(properFileName)

    return text.lower().translate(str.maketrans('', '', string.punctuation))


def get_file_merged_string(fileName: str):
    """
    Description:
        Compiles all the "text" attributes of the JSON objects in the file
        and combines them into a single string.

    Parameters:
        fileName (str): The name of the file to process.

    Returns:
        (str): The merged string.
    """
    file = open(fileName, "r", encoding=DATA_FILE_ENCODING)
    data = json.load(file) #[ {id, text, title} ]
    text = ""

    for entry in data:
        text += entry["text"]

    return text


def get_word_counts(text: str):
    """
    Description:
        Creates an tuple array of word counts from the text, where the key
        is the word and the value is the count.

    Parameters:
        text (str): The text to get the word counts from.

    Returns:
        (dict): The dictionary of word counts, sorted ascendingly by count.
    """
    counts = {}
    for word in text.split(" "):
        if(word not in counts):
            counts[word] = 1

        else:
            counts[word] += 1

    return counts





def zipf_law(wordCounts: List[Tuple[str, int]]):
    """
    Description:
        Performs Zipf's law on the text.

    Parameters:
        text (str): The text to perform Zipf's law on.
    """
    depth = 10
    counts = dict(sorted(wordCounts.items(), key=lambda x: x[1], reverse=True)[0:depth])

    def percentify(value, max):
        return round(value / max * 100)

    def smoothify(yInput):
        x = np.array(range(0, depth))
        y = np.array(yInput)
        # define x as 600 equally spaced values between the min and max of original x
        x_smooth = np.linspace(x.min(), x.max(), 600)
        # define spline with degree k=3, which determines the amount of wiggle
        spl = scipy.interpolate.make_interp_spline(x, y, k=3)
        y_smooth = spl(x_smooth)
        # Return the x and y axis
        return x_smooth, y_smooth


    ziffianCurveValues = [100/i for i in range(1, depth+1)]
    x, y = smoothify(ziffianCurveValues)
    plt.plot(x, y, label='Ziffian Curve', ls=':', color='grey')


def main():
    """
    Description:
        Main function for the wikipedia processing script.
    """
    parser = argparse.ArgumentParser(prog="Wikipedia Processing", description="Process Wikipedia JSON data.")
    parser.add_argument("--zipf", help="Perform Zipf's law.", action="store_true")
    parser.add_argument("--tokenize", help="Perform tokenization.", action="store_true")
    parser.add_argument("--stopword", help="Perform stopword removal.", action="store_true")
    parser.add_argument("--stemming", help="Perform stemming.", action="store_true")
    parser.add_argument("--invertedindex", help="Perform inverted index creation.", action="store_true")

    args = parser.parse_args()
    params = Parameters(args.zipf, args.tokenize, args.stopword, args.stemming, args.invertedindex)

    text = get_full_merged_string(params)
    counts = get_word_counts(text)
    zipf_law(counts)

    print(f"Length of fully merged text is {len(text)} characters.")
    print(f"Memory of fully merged text is {sys.getsizeof(text) / 1000000} MB.")


    return


if (__name__ == "__main__"):
    main()
