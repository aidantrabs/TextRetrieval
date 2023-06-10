<div align="center">
  
# _Text Retrieval & Search Engine_ :globe_with_meridians:

A collection of multiple command-line programs that utilize various topics involved with text retrieval and search engines.

</div>

## Breakdown :pushpin: 

<div align="center"> 
  
###  -- A01 --

### <code> webcrawler1.py </code>
  
<hr>

</div>

- Downloads content of <code>initialURL</code> 
- Writes downloaded content in <code>H.txt</code>, where H is the calculated hash value of <code>initialURL</code>, using <code>hashlib</code>
- Extracts all hyperlinks of the downloaded content 
- Apennds a line at the end of file <code>crawler1.log</code> that includes <code>&lt;H, URL, Download DateTime, HTTP Response Code&gt;</code>

<br>

> Usage: 

```php
$ python3 webcrawler1.py [options] initialURL
```

> Options: 

<code>--maxdepth</code>: Maximum number of depths to crawl from initialURL <br>
<code>--rewrite</code>: If value is TRUE and H.txt exists for current URL, it re-extracts and re-writes URL. Default is FALSE. <br>
<code>--verbose</code>: If TRUE, prints &lt;URL, depth&gt;. Default is FALSE.


<div align="center"> 
  
### <code> webcrawler2.py </code>

<hr>
  
</div>

- Downloads content of <code>researcherURL</code> 
- Writes downloaded content in <code>H.txt</code>, where H is the calculated hash value of <code>researcherURL</code>, using <code>hashlib</code>
- Extracts all information from the pages in a JSON format, and saves it to <code>H.json</code>
- Is able to parse past the limited number of publications by sending a POST request to the URL dynamically


> Usage: 

```php
$ python3 webcrawler2.py researcherURL
```   

<div align="center"> 
  
### <code> webcrawler3.py </code>

<hr>
  
</div>

- Downloads content of <code>initialURL</code> 
- Writes downloaded content in <code>H.html</code>, where H is the calculated hash value of <code>initialURL</code>, using <code>hashlib</code>
- Replaces all HTML tags with 1, assuming that a HTML tag is <code>&lt;?????&gt;</code>, where <code>?????</code> is a combination of any characters having any length. This is done using REGEX to simplify HTML tags' identification and replacement process 
- Replaces tokens (words) with 0 </code> 
- $\forall 0 \leq j \leq N-1$ calculates $f(i,j)$ and prints $(i*,j*)$ which is the best combination of $i,j$ that maximizes $f(i,j)$
- Writes the identified main content of downloaded page (which is located between $i*$ and $j*$) in H.txt.
- For all calculated values of $i$, $j$ plot function $f(i,j)$ similar to one of the following plots. The x-axis and y-axis are for $i$ and $j$, respectively. The color of the histogram for 2D or z-axis for 3D represents $f(i,j)$ 

$$f(i,j) = \sum_{n=0}^{i - 1}{b_n} + \sum_{n=i}^{j}{(1-b_n)} + \sum_{n=j}^{N-1}{b_n}$$
   
> Usage: 

```php
$ python3 webcrawler3.py initialURL
```   

<!-- -->

<div align="center"> 
  
### -- A02 --

### <code> wikipedia_processing.py </code>
  
<hr>

</div>

The main function calls different functions depending on the arguments passed to the program.
- The Zipf's Law functions graphs the top 50 most frequent words.
- The tokenize function tokenizes the text and returns a list of tokens printed to a file.
- The tokenize argument stems the tokens using Porter Stemming and returns a list of stems printed to a file.
- The stopword argument removes all the stopwords from a list of tokens, printing the result to a file.
- The inverted index argument creates an inverted index of the tokens (stemmed and stopwords removed), printing the result to a file, and printed to the standard out.


<br>

> Usage: 

```php
$ python3 wikipedia_processing.py [options]
```

> Options: 

<code>--zipf</code>: Perform Zipf's law. <br>
<code>--tokenize</code>: Perform tokenization. <br>
<code>--stopword</code>: Perform stopword removal. <br>
<code>--stemming</code>: Perform stemming. <br>
<code>--invertedindex</code>: Perform inverted index creation.


<div align="center"> 
  
### <code> elias_coding.py </code>

<hr>
  
</div>

The main function calls different functions depending on the arguments passed to the program. The program can be run in two modes with two different algorithms: encoding and decoding with the Elias Gamma and Elias Delta algorithms. Each number is iterated over and passed to the specific function.

#### Elias Delta Coding
- The encode_elias_delta function takes a number as input and returns the result. The function first calculates the log_2 of the given number and adds 1. This number is then converted to binary and the first bit is removed. The remaining bits are then concatenated with the original number in unary. The simplified version of this formula can be seen below: $$n = 1 + \lfloor log_{2}(x) \rfloor \newline result = n_{binary} + x_{unary}$$

#### Elias Gamma Coding
- The encode_elias_gamma function takes a number as input and returns the result. The function first calculates the log_2 of the given number and adds 1. After this, variables n and b are calculated using the following simplified formula: $$n = 1 + log_{2}(x) \newline b = (x - 2)^{log_{2}(x)} \newline result = n_{unary} + b_{binary}$$

#### Elias Delta Decoding
- The decode_elias_delta function takes a string as input and returns the result as an integer. The code does the reverse of the encoding function, and then verifies the calculated kdd, kdr, and kdd_binary values against the values calculated from the input string. If the values do not match, the function returns an error message.

#### Elias Gamma Decoding
- The decode_elias_gamma function takes a string as input and returns the result as an integer. The code does the reverse of the encoding function, and then verifies the calculated value against the basic rules for Elias Coding.

> Usage: 

```php
$ python3 elias_coding.py [options] [data]
```   

> Options: 

<code>--alg</code>: The algorithm to use. Can be either 'elias_delta' or 'elias_gamma'. <br>
<code>--encode</code>: Encode the data. <br>
<code>--decode</code>: Decode the data. <br>

<div align="center"> 
  
### <code> page_rank.py </code>

<hr>
  
</div>

The purpose of the program was to utilize the page rank algorithm which took the arguments of max iteration, lambda, threshold and a list of nodes. The basic idea was to parse through a large data set (web-Stanford.txt) which provided 2,312,502 node connections, the page rank algorithm is then applied to find specified nodes and determine the page rank of those nodes, in order of highest priority. When developing this program, the biggest issue I faced was that of the large data set. My first few iterations of the program worked extremely quickly on a smaller data set which I extracted. Finally, I was able to implement an efficent program, while it is not instanenous it is significantly faster. It avoids recomputing the reciprocal of the number of outbound edges for each node at each iteration by precomputing it once before the iterations begin. It also calculates the number of outbound edges for each node in a more efficient way by iterating over the edges only once, which reduces the number of iterations required to converge. A selection sort is then applied to then display the results to the user.

- The function <code>load_data()</code> loads the data set and splits the lines, seperating the from_nodes and in_nodes and applies them to a simple graph, which is just a Python dictionary. It returns the graph of the nodes and the number of outbound links given in each node.

- The function <code>page_rank()</code> aplies the page rank algorithm to each node in the graph. It uses an iterative approach and returns the current pagerank values.

- The function <code>page_rank_handler()</code> applies the user's arguments to the page rank algorithm (<code>page_rank()</code>) and prints the page ID and the rank of that page.

- The function <code>arg_handler()</code> handles all the user arguments and returns them.

- The function <code>main()</code> runs the program, by applying the arguments to the <code>page_rank_handler()</code>.
   
> Usage: 

```php
$ python3 page_rank.py --maxiteration x --lambda y --thr z --nodes [data]
```   

##### Note: The user passes in the node list as individual values, space seperated.


<div align="center"> 
  
### <code> noisy_channel.py </code>

<hr>
  
</div>

- The noisy_channel.py module defines the functions required for implementing the Noisy Channel Model, including the noisy_channel_model, generate_candidates, and channel_model functions.

- The nltk module is used for tokenization and stopword removal. The Counter class from the collections module is used to count the occurrences of each word in the dataset. The math module is used for exponentiation.

- The script also includes a workaround for SSL certificate verification, in case SSL verification fails.

- The noisy_channel_model function generates a set of candidate words for the misspelled word and returns a dictionary of candidate words with their respective probabilities.

- The generate_candidates function generates a set of candidate words by performing operations such as deleting, transposing, replacing, and inserting characters.

- The channel_model function calculates the probability of a word being a candidate by calculating the cost of transforming one word into another using edit distance.

- The main function uses argparse to parse command-line arguments. The --correct option takes a list of misspelled words and returns the most probable correction for each misspelled word. The --proba option takes a list of words and returns their respective probabilities in the dataset.

> Usage: 

```php
$ python noisy_channel.py [options] [values]
```   

> Options: 

<code>--correct</code>: that gets a list of words in an array and for each prints best word to replace. <br>
<code>--proba</code>: that gets a list of words in an array and for each item prints $P(w)$.

<div align="center"> 
  
###  -- A03 --
  
### <code> training_sentiment.py </code>

<hr>
  
</div>

- The program first parses the arguments provided by the user. If no dataset argument and/or classifier argument is provided, the program will let the user know to select one of each. If more than one dataset and/or classifier argument is provided, the program will run the first one from the list. This is done by the arg_handler and parse_args functions.
- The program then loads the dataset into a pandas dataframe from the data folder. This is done by the load_dataset function.
- The program then loads the classifier into a vectorizer by the init_vectorizer function.
- The data is parsed by the process_text function, and used to train the classifier in the init_classifier function. The classifier is then used to predict the sentiment of the test data.
- The metrics of the classifier is then calculated and printed to the console using the calculate_performance_metrics and calculate_cross_validation_performance_metrics functions.
- Lastly, the program generates and saves a confusion matrix to the disk, as well as serializing the classifier and vectorizer to the disk. This is done by the save_confusion_matrix and serialize_classifier_and_vectorizer functions.


> Usage: 

```php
$ python3 training_sentiment.py [-h] ([--imdb] [--amazon] [--yelp]) ([--naive] [--svm] [--decisiontree] [--knn <n>])
```   

> Options: 
- The program requires one of the following dataset arguments: --imdb, --amazon, --yelp. If more than one dataset is provided, the program will run the first one from the list.
- The program also requires one of the following classifier arguments: --naive, --svm, --decisiontree, --knn <n>. If more than one classifier is provided, the program will run the first one from the list.
  
<div align="center"> 
  
### <code> cluster_news.py </code>

<hr>
  
</div>

- The program preprocesses the large data set, known as 20_newsgroups, in the function def preprocess_data(). The first implementation parsed this data concurrently at first, however, it was noticed that the data set was too big to handle in this fashion. Multiple data structures were tried and failed. The solution to this problem was to utilize the function found in the sklearn data sets built-in library. Fortunately, this method allowed for the removal of all headers, footers and quotes in one function call, removing redundant data. The data is then clustered via the def cluster_data(preprocessed_data, ncluster, clustering_method). Manually clustering was tried but this slowed down the program significantly. The sklearn.cluster library has the methods required to perform kmeans, whc, ac, and dbscan clustering, thus it was utilized. This 2D array data was then used to predict the output value.
- Other functions being utilized are the def arg_handler() and def main(), where the first handles the arguments passed and main is used to call the cluster_data() function when an option is chosen.



> Usage: 

```php
$ python3 cluster_news.py [options]
```   
  
> Options: 

<code>--ncluster</code>: Number of cluster(s) array.<br>
<code>--kmeans</code>: Use KMeans clustering. <br>
<code>--whc</code>: Use Ward Hierarchical clustering. <br>
<code>--ac</code>: Use Agglomerative clustering. <br>
<code>--dbscan</code>: Use DBSCAN clustering. 

## Usage :pencil:

### CLI

#### Example for `A01`
> Enter source directory
```sh
$ cd A01
```

## Installation :hammer:

> Install virtual env :
```
$ pip install pipenv
```

> Set env version :
```
$ pipenv --python 3.10
```

> Activate env :
```
$ pipenv shell 
```

> Install dependencies :
```
$ pipenv install -r requirements.txt
```
