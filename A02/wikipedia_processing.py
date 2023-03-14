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
TOKENIZED_FILE_NAME = "wikipedia.token"
STOPWORD_FILE_NAME = "wikipedia.token.stop"
STEMMED_FILE_NAME = "wikipedia.token.stemm"
INVERTED_INDEX_FILE_NAME = "wikipedia.index"

JSON_FILE_NAMES = [os.path.join(DATA_DIRECTORY, fileName) for fileName in os.listdir(DATA_DIRECTORY)]
JSON_FILE_NAMES = [fileName for fileName in JSON_FILE_NAMES if os.path.isfile(fileName)]

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
    for fileName in JSON_FILE_NAMES:
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


def zipf_law(tokens: List[str]):
    """
    Description:
        Performs Zipf's law on the text.

    Parameters:
        tokens (List[str]): The list of tokens to perform Zipf's law on.
    """
    print("Performing Zipf's law...")
    frequencies = nltk.FreqDist(tokens)
    frequencies.plot(50, cumulative=False)

    print("Done!")
    return


def tokenize(tokens: List[str]):
    """
    Description:
        Tokenizes the text and saves the result to a 'wikipedia.token' file.

    Parameters:
        tokens (List[str]): The list of tokens to tokenize.
    """
    print("Tokenizing...")
    with open(TOKENIZED_FILE_NAME, "w", encoding=DATA_FILE_ENCODING) as file:
        file.write("\n".join(tokens))

    print("Done!")
    return


def _remove_stopwords(tokens: List[str]):
    """
    Description:
        Removes stopwords from the text.

    Parameters:
        tokens (List[str]): The list of tokens to remove stopwords from.

    Returns:
        (List[str]): The list of tokens without stopwords.
    """
    stopwords = nltk.corpus.stopwords.words("english")
    result = [word for word in tokens if word not in stopwords]
    return result


def remove_stopwords(tokens: List[str]):
    """
    Description:
        Removes stopwords from the text and saves the result to a
        'wikipedia.token.stop' file.

    Parameters:
        tokens (List[str]): The list of tokens to remove stopwords from.
    """
    print("Removing stopwords...")
    result = _remove_stopwords(tokens)
    with open(STOPWORD_FILE_NAME, "w", encoding=DATA_FILE_ENCODING) as file:
        file.write("\n".join(result))

    print("Done!")
    return


def _porter_stemming(tokens: List[str]):
    """
    Description:
        Performs Porter stemming on the text.

    Parameters:
        tokens (List[str]): The list of tokens to perform Porter stemming on.

    Returns:
        (List[str]): The list of stemmed tokens.
    """
    stemmer = nltk.stem.PorterStemmer()
    result = [stemmer.stem(word) for word in tokens]
    return result


def porter_stemming(tokens: List[str]):
    """
    Description:
        Performs Porter stemming on the text and saves the result to
        a 'wikipedia.token.stemm' file.

    Parameters:
        tokens (List[str]): The list of tokens to perform Porter stemming on.
    """
    print("Performing Porter stemming...")
    result = _porter_stemming(tokens)
    with open(STEMMED_FILE_NAME, "w", encoding=DATA_FILE_ENCODING) as file:
        file.write("\n".join(result))

    print("Done!")
    return


def inverted_index():
    """
    Description:
        Creates an inverted index for the text and saves the result to
        a 'wikipedia.token.index' file.

    Parameters:
        corpus (str): The text to create an inverted index for.

        {word: {id: count, id2: count2},}}
    Returns:
        (Dict[str, List[int]]): The inverted index.
    """
    print("Creating inverted index...")
    index = {}
    for fileName in JSON_FILE_NAMES:
        file = open(fileName, "r", encoding=DATA_FILE_ENCODING)
        data = json.load(file) #[ {id, text, title} ]
        for entry in data:
            articleId = entry["id"]
            text = entry["text"].lower()
            tokenizedText = nltk.word_tokenize(text)
            tokenizedText = _remove_stopwords(tokenizedText)
            tokenizedText = _porter_stemming(tokenizedText)

            for word in tokenizedText:
                if (word not in index):
                    index[word] = {articleId: 1}

                elif (articleId not in index[word]):
                    index[word][articleId] = 1

                else:
                    index[word][articleId] += 1

    with open(INVERTED_INDEX_FILE_NAME, "w", encoding=DATA_FILE_ENCODING) as file:
        file.write(json.dumps(index))

    print("Done!")
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

    if (args.zipf):
        zipf_law(tokens)

    if (args.tokenize):
        tokenize(tokens)

    if (args.stopword):
        remove_stopwords(tokens)

    if (args.stemming):
        porter_stemming(tokens)

    if (args.invertedindex):
        print(inverted_index())

    return


if (__name__ == "__main__"):
    main()
