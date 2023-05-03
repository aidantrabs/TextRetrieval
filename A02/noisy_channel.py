import argparse
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import math
import ssl

# Get past SSL certificate verification
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('stopwords')
nltk.download('punkt')

stop_words = set(stopwords.words('english'))

try:
    with open('data_wikipedia/00c2bfc7-57db-496e-9d5c-d62f8d8119e3.json', 'r') as file:
        text = file.read()
except (FileNotFoundError, PermissionError) as e:
    print(f"Error: {e}")
    exit()

text = text.translate(str.maketrans('', '', string.punctuation))
text = text.lower()
tokens = word_tokenize(text)
words = []
for word in tokens:
    if word.isalpha() and word not in stop_words:
        words.append(word)

# Creating a language model for calculating probabilities of words in the dataset
word_counts = Counter(words)
total_words = sum(word_counts.values())

# Calculating probabilities of words in the dataset
word_probs = {}
for word, count in word_counts.items():
    word_probs[word] = count / total_words

def noisy_channel_model(word: str, vocab: dict, del_cost=1, ins_cost=1, sub_cost=1):
    """
    Description:
        Returns a dictionary of candidate words and their probabilities.

    Parameters:
        word (str): The word to generate candidates for.
        vocab (dict): A dictionary of words and their probabilities.
        del_cost (int): The cost of deleting a character.
        ins_cost (int): The cost of inserting a character.
        sub_cost (int): The cost of substituting a character.

    Returns:
        probs (dict): A dictionary of candidate words and their probabilities.
    """
    candidates = generate_candidates(word)
    probs = {}
    for candidate in candidates:
        if candidate in vocab:
            prob = channel_model(word, candidate, del_cost, ins_cost, sub_cost) * vocab[candidate]
            probs[candidate] = prob
    return probs

def generate_candidates(word: str):
    """
    Description:
        Returns a set of candidate words.

    Parameters:
        word (str): The word to generate candidates for.

    Returns:
        candidates (set): A set of candidate words.
    """
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = {a + b[1:] for a, b in splits if b}
    transposes = {a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1}
    replaces = {a + c + b[1:] for a, b in splits for c in alphabet if b}
    inserts = {a + c + b for a, b in splits for c in alphabet}
    return deletes | transposes | replaces | inserts

def channel_model(x: str, y: str, del_cost: int, ins_cost: int, sub_cost: int):
    """
    Description:
        Returns the probability of transforming x into y.

    Parameters:
        x (str): The word to transform.
        y (str): The word to transform into.
        del_cost (int): The cost of deleting a character.
        ins_cost (int): The cost of inserting a character.
        sub_cost (int): The cost of substituting a character.

    Returns:
        prob (float): The probability of transforming x into y.
    """
    if x == y:
        return 1
    if len(x) > len(y):
        x, y = y, x
    if len(y) - len(x) > 1:
        return 0
    prev_row = list(range(len(y) + 1))
    for i, c1 in enumerate(x):
        curr_row = [i + 1]
        for j, c2 in enumerate(y):
            del_cost_ = prev_row[j + 1] + del_cost
            ins_cost_ = curr_row[j] + ins_cost
            sub_cost_ = prev_row[j] + sub_cost * (c1 != c2)
            curr_row.append(min(del_cost_, ins_cost_, sub_cost_))
        prev_row = curr_row
    return math.exp(-prev_row[-1])

def main():
    """
    Description:
        Main function of the program.

    Parameters:
        None

    Returns:
        None
    """
    parser = argparse.ArgumentParser(description='Noisy Channel Model Spell Checker')
    parser.add_argument('--correct', nargs='+', help='list of misspelled words to correct')
    parser.add_argument('--proba', nargs='+', help='list of words to calculate probabilities for')
    args = parser.parse_args()

    if args.correct:
        words = []
        for arg in args.correct:
            for word in arg.strip('[]').split(','):
                if word.isalpha():
                    words.append(word.strip(string.punctuation))
        for word in words:
            candidates = noisy_channel_model(word, word_probs)
            best_word = max(candidates, key=candidates.get)
            print(f"{word} -> {best_word}")

    if args.proba:
        words = []
        for arg in args.proba:
            for word in arg.strip('[]').split(','):
                if word.isalpha():
                    words.append(word.strip(string.punctuation))
                    
        for word in words:
            prob = word_probs.get(word, 0)
            print(f"P({word}) = {prob}")

if __name__ == '__main__':
    main()
