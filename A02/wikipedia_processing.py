import json
import os
import sys

DATA_DIRECTORY = "./data_wikipedia"

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


def process_files(params: Parameters):
    """
    Description:
        Processes all files in the data directory.

    Parameters:
        params (Parameters): The parameters for the script.
    """
    for fileName in os.listdir(DATA_DIRECTORY):
        properFileName = os.path.join(DATA_DIRECTORY, fileName)
        if(not os.path.isfile(properFileName)):
            continue

        process_file(properFileName, params)

    return


def process_file(fileName: str, params: Parameters):
    """
    Description:
        Processes a file.

    Parameters:
        fileName (str): The name of the file to process.
        params (Parameters): The parameters for the script.
    """
    file = open(fileName, "r")
    data = json.load(file) #[ {id, text, title} ]
    mergedText = ""

    for entry in data:
        id = entry["id"]
        text = entry["text"]
        title = entry["title"]
        mergedText += text

    return


def main():
    """
    Description:
        Main function for the wikipedia processing script.
    """
    params = Parameters()
    params.zipf = "--zipf" in sys.argv
    params.tokenize = "--tokenize" in sys.argv
    params.stopword = "--stopword" in sys.argv
    params.stemming = "--stemming" in sys.argv
    params.invertedIndex = "--invertedindex" in sys.argv

    process_files(params)
    return


if (__name__ == "__main__"):
    main()
