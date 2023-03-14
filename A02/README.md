
<div align="center">



# Assignment 2 Report



#### Monday 13th March 2023



</div>



## Group Members

*  **Aidan Traboulay** 200115590 - trab5590@mylaurier.ca

*  **Mobina Tooranisama** 200296720 - toor6720@mylaurier.ca

*  **Nausher Rao** 190906250 - raox6250@mylaurier.ca



## Contributions
 #### **Aidan Traboulay** 200115590
 - I worked on the `page_rank.py` file, which utilized the page rank algorithm to determine the page rank of pages in a given data set. 

####  **Mobina Tooranisama** 200296720
- I worked on the `noisy_channel.py` file, which uses the noisy channel model to spell check and corrects misspelled words and calculates probabilities of words in a given dataset.

####  **Nausher Rao** 190906250
- I worked on the `elias_coding.py` file, writing all the functions for encoding and decoding. This file extensively used the built-in `math` module.
- I worked on the `wikipeda_processing.py` file, writing all the functions for processing the wikipedia data. This file extensively used the built-in `json`, `os`, `string`, and `sys` modules, as well as the Natural Language Toolkit (`nltk`) - specifically the `corpus`, `stem`, and `tokenize` submodules.


## Explanations
All three programs used quite different modules, but were all written using `Python 3.10`.

### Wikipedia Processing (`wikipedia_processing.py`)
The main function calls different functions depending on the arguments passed to the program.
- The Zipf's Law functions graphs the top 50 most frequent words.
- The tokenize function tokenizes the text and returns a list of tokens printed to a file.
- The tokenize argument stems the tokens using Porter Stemming and returns a list of stems printed to a file.
- The stopword argument removes all the stopwords from a list of tokens, printing the result to a file.
- The inverted index argument creates an inverted index of the tokens (stemmed and stopwords removed), printing the result to a file, and printed to the standard out.


### Elias Coding (`elias_coding.py`)
The main function calls different functions depending on the arguments passed to the program. The program can be run in two modes with two different algorithms: encoding and decoding with the Elias Gamma and Elias Delta algorithms. Each number is iterated over and passed to the specific function.


#### Elias Delta Coding
The `encode_elias_delta` function takes a number as input and returns the result. The function first calculates the log_2 of the given number and adds 1. This number is then converted to binary and the first bit is removed. The remaining bits are then concatenated with the original number in unary. The simplified version of this formula can be seen below:
$$ n = 1 + \lfloor log_{2}(x) \rfloor \newline result = n_{binary} + x_{unary}$$


#### Elias Gamma Coding
The `encode_elias_gamma` function takes a number as input and returns the result. The function first calculates the log_2 of the given number and adds 1. After this, variables `n` and `b` are calculated using the following simplified formula:
$$ n = 1 + log_{2}(x) \newline b = (x - 2)^{log_{2}(x)} \newline result = n_{unary} + b_{binary}$$


#### Elias Delta Decoding
The `decode_elias_delta` function takes a string as input and returns the result as an integer. The code does the reverse of the encoding function, and then verifies the calculated kdd, kdr, and kdd_binary values against the values calculated from the input string. If the values do not match, the function returns an error message.


#### Elias Gamma Decoding
The `decode_elias_gamma` function takes a string as input and returns the result as an integer. The code does the reverse of the encoding function, and then verifies the calculated value against the basic rules for Elias Coding.


### Page Rank (`page_rank.py`)
The purpose of the program was to utilize the page rank algorithm which took the arguments of `max iteration`, `lambda`, `threshold` and a list of `nodes`. The basic idea was to parse through a large data set (`web-Stanford.txt`) which provided **2,312,502** node connections, the page rank algorithm is then applied to find specified nodes and determine the page rank of those nodes, in order of highest priority. When developing this program, the biggest issue I faced was that of the large data set. My first few iterations of the program worked extremely quickly on a smaller data set which I extracted. Finally, I was able to implement an efficent program, while it is not instanenous it is significantly faster. It avoids recomputing the reciprocal of the number of outbound edges for each node at each iteration by precomputing it once before the iterations begin. It also calculates the number of outbound edges for each node in a more efficient way by iterating over the edges only once, which reduces the number of iterations required to converge. A selection sort is then applied to then display the results to the user. 

#### Program Breakdown

The function `load_data()` loads the data set and splits the lines, seperating the **from_nodes** and **in_nodes** and applies them to a simple graph, which is just a Python dictionary. It returns the graph of the nodes and the number of outbound links given in each node.

The function `page_rank()` aplies the page rank algorithm to each node in the graph. It uses an iterative approach and returns the current pagerank values.

The function `page_rank_handler()` applies the user's arguments to the page rank algorithm (`page_rank()`) and prints the page ID and the rank of that page.

The function `arg_handler()` handles all the user arguments and returns them.

The function `main()` runs the program, by applying the arguments to the `page_rank_handler()`.

#### Usage
```sh
python3 page_rank.py --maxiteration 20 --lambda .25 --thr .01 --nodes 5 87524 632
```

- Note: The user passes in the node list as individual values, space seperated.

### Noisy Channel (`noisy_channel.py`)
The `noisy_channel.py` module defines the functions required for implementing the Noisy Channel Model, including the `noisy_channel_model`, `generate_candidates`, and `channel_model` functions. 

The `nltk` module is used for tokenization and stopword removal. The `Counter` class from the `collections` module is used to count the occurrences of each word in the dataset. The `math` module is used for exponentiation.

The script also includes a workaround for SSL certificate verification, in case SSL verification fails.

The `noisy_channel_model` function generates a set of candidate words for the misspelled word and returns a dictionary of candidate words with their respective probabilities. 

The `generate_candidates` function generates a set of candidate words by performing operations such as deleting, transposing, replacing, and inserting characters. 

The `channel_model` function calculates the probability of a word being a candidate by calculating the cost of transforming one word into another using edit distance.

The `main` function  uses argparse to parse command-line arguments. The `--correct` option takes a list of misspelled words and returns the most probable correction for each misspelled word. The `--proba` option takes a list of words and returns their respective probabilities in the dataset.

The script is callable form the command line as below:

```python noisy_channel.py [options] [values]```

[Options] are as below:
1. `--correct`: that gets a list of words in an array and for each prints best word to replace.
2. `--proba`: that gets a list of words in an array and for each item prints P(w)

#### Usage
```sh
python noisy_channel.py --correct [advertice, univercity, university , iimprove]
python noisy_channel.py --proba [advertise, computer, algorithm, medicine874r]
```