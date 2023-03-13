import argparse
import json
import nltk
import nltk.corpus
import nltk.stem
import nltk.tokenize
import os
import string
import sys
from typing import List

DATA_DIRECTORY = "./data_wikipedia"
DATA_FILE_ENCODING = "utf-8"

def generate_corpus():
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
    fileNames = [os.path.join(DATA_DIRECTORY, fileName) for fileName in os.listdir(DATA_DIRECTORY)]
    fileNames = [fileName for fileName in fileNames if os.path.isfile(fileName)]

    for fileName in fileNames:
        file = open(fileName, "r", encoding=DATA_FILE_ENCODING)
        data = json.load(file) #[ {id, text, title} ]
        for entry in data:
            text += entry["text"]

    return text.lower().translate(str.maketrans("", "", string.punctuation))


def get_tokenized_corpus(corpus: str):
    """
    Description:
        Tokenizes the text and saves the result to a 'wikipedia.token' file.

    Parameters:
        corpus (str): The text to tokenize.

    Returns:
        (List[str]): The list of tokens.
    """
    return nltk.word_tokenize(corpus)


# def zipf_law(wordCounts: List[Tuple[str, int]]):
def zipf_law(tokens: List[str]):
    """
    Description:
        Performs Zipf's law on the text.

    Parameters:
        text (str): The text to perform Zipf's law on.
    """
    frequencies = nltk.FreqDist(tokens)
    frequencies.plot(50, cumulative=False)

    # depth = 100
    # counts = dict(sorted(wordCounts.items(), key=lambda x: x[1], reverse=True)[0:depth])
    # for idx, (words, frequency) in enumerate(counts.items()):
    #     if idx == 0:
    #         top_count = frequency
    #     print(words, frequency, round(top_count/frequency, 2))

    # def percentify(value, max):
    #     return round(value / max * 100)

    # def smoothify(yInput):
    #     x = np.array(range(0, depth))
    #     y = np.array(yInput)
    #     # define x as 600 equally spaced values between the min and max of original x
    #     x_smooth = np.linspace(x.min(), x.max(), 600)
    #     # define spline with degree k=3, which determines the amount of wiggle
    #     spl = scipy.interpolate.make_interp_spline(x, y, k=3)
    #     y_smooth = spl(x_smooth)
    #     # Return the x and y axis
    #     return x_smooth, y_smooth


    # ziffianCurveValues = [100/i for i in range(1, depth+1)]
    # x, y = smoothify(ziffianCurveValues)
    # plt.plot(x, y, label="Ziffian Curve", ls=":", color="grey")


def tokenize(tokens: List[str]):
    """
    Description:
        Tokenizes the text and saves the result to a 'wikipedia.token' file.

    Parameters:
        text (str): The text to tokenize.
    """
    with open("wikipedia.token", "w", encoding=DATA_FILE_ENCODING) as file:
        file.write("\n".join(tokens))

    return


def remove_stopwords(tokens: List[str]):
    """
    Description:
        Removes stopwords from the text and saves the result to a
        'wikipedia.token.stop' file.

    Parameters:
        text (str): The text to remove stopwords from.
    """
    stopwords = nltk.corpus.stopwords.words("english")
    result = [word for word in tokens if word not in stopwords]
    with open("wikipedia.token.stop", "w", encoding=DATA_FILE_ENCODING) as file:
        file.write("\n".join(result))

    return

def porter_stemming(tokens: List[str]):
    """
    Description:
        Performs Porter stemming on the text and saves the result to
        a 'wikipedia.token.stemm' file.

    Parameters:
        text (str): The text to perform Porter stemming on.
    """
    stemmer = nltk.stem.PorterStemmer()
    result = [stemmer.stem(word) for word in tokens]
    with open("wikipedia.token.stemm", "w", encoding=DATA_FILE_ENCODING) as file:
        file.write("\n".join(result))

    return


def inverted_index(tokens: List[str]):
    """
    Description:
        Creates an inverted index for the text and saves the result to
        a 'wikipedia.token.index' file.

    Parameters:
        text (str): The text to create an inverted index for.
    """
    index = {}
    for index, word in enumerate(tokens):
        if(word not in index):
            index[word] = [index]
        else:
            index[word].append(index)

    with open("wikipedia.token.index", "w", encoding=DATA_FILE_ENCODING) as file:
        for word, positions in index.items():
            file.write(f"{word} {positions}")

    return index


def main():
    """
    Description:
        Main function for the wikipedia processing script.
    """
    nltk.download("stopwords")
    nltk.download("punkt")

    parser = argparse.ArgumentParser(prog="Wikipedia Processing", description="Process Wikipedia JSON data.")
    parser.add_argument("--zipf", help="Perform Zipf's law.", action="store_true")
    parser.add_argument("--tokenize", help="Perform tokenization.", action="store_true")
    parser.add_argument("--stopword", help="Perform stopword removal.", action="store_true")
    parser.add_argument("--stemming", help="Perform stemming.", action="store_true")
    parser.add_argument("--invertedindex", help="Perform inverted index creation.", action="store_true")
    args = parser.parse_args()

    corpus = generate_corpus()
    tokens = get_tokenized_corpus(corpus)
    print(f"Length of fully merged text is {len(corpus)} characters.")
    print(f"Memory of fully merged text is {sys.getsizeof(corpus) / 1000000} MB.")

    if(args.zipf):
        zipf_law(tokens)

    if(args.tokenize):
        tokenize(tokens)

    if(args.stopword):
        remove_stopwords(tokens)

    if(args.stemming):
        porter_stemming(tokens)

    if(args.invertedindex):
        inverted_index(tokens)

    return


if (__name__ == "__main__"):
    main()
