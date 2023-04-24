
<div align="center">



# Assignment 3 Report



#### Monday 3rd April 2023



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
- I worked on everything inside the `training_sentiment.py` file, including all functions and definitions.


## Explanations


### Training Sentiment (`training_sentiment.py`)
- The program first parses the arguments provided by the user. If no dataset argument and/or classifier argument is provided, the program will let the user know to select one of each. If more than one dataset and/or classifier argument is provided, the program will run the first one from the list. This is done by the `arg_handler` and `parse_args` functions.
- The program then loads the dataset into a pandas dataframe from the `data` folder. This is done by the `load_dataset` function.
- The program then loads the classifier into a vectorizer by the `init_vectorizer` function.
- The data is parsed by the `process_text` function, and used to train the classifier in the `init_classifier` function. The classifier is then used to predict the sentiment of the test data.
- The metrics of the classifier is then calculated and printed to the console using the `calculate_performance_metrics` and `calculate_cross_validation_performance_metrics` functions.
- Lastly, the program generates and saves a confusion matrix to the disk, as well as serializing the classifier and vectorizer to the disk. This is done by the `save_confusion_matrix` and `serialize_classifier_and_vectorizer` functions.
#### Usage
```sh
python3 training_sentiment.py [-h] ([--imdb] [--amazon] [--yelp]) ([--naive] [--svm] [--decisiontree] [--knn <n>])
```
- The program requires one of the following dataset arguments: `--imdb`, `--amazon`, `--yelp`. If more than one dataset is provided, the program will run the first one from the list.

- The program also requires one of the following classifier arguments: `--naive`, `--svm`, `--decisiontree`, `--knn <n>`. If more than one classifier is provided, the program will run the first one from the list.

### Cluster News (`cluster_news.py`)
-

#### Usage
```sh
python3 cluster_news.py
```
