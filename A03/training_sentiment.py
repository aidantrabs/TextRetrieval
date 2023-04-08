import argparse;
import csv;
import pandas;
import nltk;
import nltk.corpus;
import nltk.stem;
import nltk.tokenize;
from enum import Enum;
from sklearn.feature_extraction.text import CountVectorizer;
from typing import List;

class ClassifierType(Enum):
    NAIVE_BAYES = 1,
    SVM = 2,
    DECISION_TREE = 3,
    KNN = 4;


def arg_handler():
    """
    Description:
        Handle the arguments.
    Parameters:
        None
    Returns:
        args: the arguments.
    """
    parser = argparse.ArgumentParser()
    dataset = parser.add_argument_group("Dataset")
    dataset.add_argument("--imdb", action="store_true", help="Use the IMDB dataset for training the ML model.")
    dataset.add_argument("--amazon", action="store_true", help="Use the Amazon dataset for training the ML model.")
    dataset.add_argument("--yelp", action="store_true", help="Use the Yelp dataset for training the ML model.")

    classifier = parser.add_argument_group("Classifier")
    classifier.add_argument("--naive", action="store_true", help="Use the Naive Bayes algorithm for training the classifier.")
    classifier.add_argument("--svm", action="store_true", help="Use the Support Vector Machine algorithm for training the classifier.")
    classifier.add_argument("--decisiontree", "-dt", dest="dt", action="store_true", help="Use the Decision Tree algorithm for training the classifier.")
    classifier.add_argument("--knn", action="store", nargs=1, help="Use the K-Nearest Neighbors algorithm for training the classifier.")
    return parser.parse_args()


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


def remove_stopwords(tokens: List[str]):
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


def train_with_dataset(dataset_file_name: str):
    """
    Description:
        Train the ML model.
    Parameters:
        dataset_file: the file containing the dataset.
    Returns:
        None
    """
    file_name = f"data/training_sentiment/{dataset_file_name}"
    data = pandas.read_csv(file_name, sep='\t', header=None)

    tokenized = get_tokenized_corpus(data[0])
    processed_text = remove_stopwords(tokenized)

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(processed_text)
    Y = data[1]
    if (classType == 1):
        classifier = MultinomialNB()

    elif(classType == 2):
        classifier = KNeighborsClassifier(knnInteger)

    elif(classType == 3):
        classifier = SVC()

    else:
        classifier = DecisionTreeClassifier()

    # Train the classifier
    classifier.fit(X, Y)

    # Define cross-validation technique
    kf = KFold(n_splits=5, shuffle=True, random_state=42)


    # Print performance metrics
    y_pred = classifier.predict(X)
    accuracy = accuracy_score(Y, y_pred)
    recall = recall_score(Y, y_pred, average="macro")
    precision = precision_score(Y, y_pred, average="macro")
    f1 = f1_score(Y, y_pred, average="macro")
    print("Performance of Classification:\n\tAccuracy: {:.3f}\n\tRecall: {:.3f}\n\tPrecision: {:.3f}\n\tF1-score: {:.3f}".format(accuracy, recall, precision, f1))


    # Evaluate performance with cross-validation
    cross_accuracy = cross_val_score(classifier, X, Y, cv=kf, scoring="accuracy")
    cross_recall = cross_val_score(classifier, X, Y, cv=kf, scoring="recall_macro")
    cross_precision = cross_val_score(classifier, X, Y, cv=kf, scoring="precision_macro")
    cross_f1 = cross_val_score(classifier, X, Y, cv=kf, scoring="f1_macro")
    print("Evaluation of Performance with Cross-Validation:\n\tAccuracy: {:.3f}\n\tRecall: {:.3f}\n\tPrecision: {:.3f}\n\tF1-score: {:.3f}".format(np.mean(cross_accuracy), np.mean(cross_recall), np.mean(cross_precision), np.mean(cross_f1)))

    # Plot the confusion matrix
    cm = confusion_matrix(Y, y_pred)
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.title("Confusion Matrix")
    plt.savefig("sentiment_classifier.png")
    #plt.show()

    # Save the model
    with open(saveName, "wb") as file:
        joblib.dump(classifier, file)

    #Save the vectorizer
    with open(vectName, "wb") as file:
        joblib.dump(vectorizer, file)


        # for line in f:
        #      print(line, end="")
        #      print(line.strip().split(" "))
        #      print(line.strip().split(" ")[-1])
        #      break

    return


def classify_with(text: List[str], classifierType: ClassifierType):
    """
    Description:
        Classify the text.
    Parameters:
        classifierType: the type of classifier to use.
    Returns:
        None
    """
    return

def main():
    """
    Description:
        The main function.
    """
    args = arg_handler()
    if(args.imdb):
        train_with_dataset("imdb_labelled.txt")

    if(args.amazon):
        train_with_dataset("amazon_cells_labelled.txt")

    if(args.yelp):
        train_with_dataset("yelp_labelled.txt")

    if(args.naive):
        classify_with("Naive Bayes", ClassifierType.NAIVE_BAYES)

    if(args.svm):
        classify_with("Support Vector Machine", ClassifierType.SUPPORT_VECTOR_MACHINE)

    if(args.dt):
        classify_with("Decision Tree", ClassifierType.DECISION_TREE)

    if(args.knn):
        classify_with("K-Nearest Neighbors", ClassifierType.K_NEAREST_NEIGHBORS)

    return


if (__name__ == "__main__"):
    main()
