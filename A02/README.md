
<div align="center">



# Assignment 2 Report



#### Monday 6th March 2023



</div>



## Group Members

*  **Aidan Traboulay** 200115590 - trab5590@mylaurier.ca

*  **Mobina Tooranisama** 200296720 - toor6720@mylaurier.ca

*  **Nausher Rao** 190906250 - raox6250@mylaurier.ca



## Contributions
 #### **Aidan Traboulay** 200115590
 -

####  **Mobina Tooranisama** 200296720
-

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


### Noisy Channel (`noisy_channel.py`)
