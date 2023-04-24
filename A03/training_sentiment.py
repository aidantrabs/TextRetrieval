import argparse;
import csv
import enum
import joblib
import matplotlib.pyplot as plt
import nltk;
import nltk.corpus;
import nltk.stem;
import nltk.tokenize;
import numpy;
import pandas;
import seaborn as sns
import sklearn

from sklearn.feature_extraction.text import CountVectorizer;
from typing import List, Union;

from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score, confusion_matrix
from sklearn.model_selection import KFold
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


CONFUSION_MATRIX_FILE_NAME = "confusion_matrix.png"

class ClassifierType(enum.Enum):
    NAIVE_BAYES = 1,
    KNN = 2,
    SVM = 3,
    DECISION_TREE = 4;


def arg_handler():
    """
    Description:
        Handle the arguments using argparse.

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


def parse_args(args: object):
    """
    Description:
        Parse the arguments.

    Parameters:
        args: The arguments.

    Returns:
        dataset: The dataset to use.
        classifierType: The classifier to use.
        data: If KNN is chosen as the ClassifierType, this is the n value to use.
    """
    data = None
    if(args.imdb):
        dataset = "imdb_labelled.txt"

    elif(args.amazon):
        dataset = "amazon_cells_labelled.txt"

    elif(args.yelp):
        dataset = "yelp_labelled.txt"

    else:
        print("Error! No dataset selected.")
        exit(1)


    if(args.naive):
        classifierType = ClassifierType.NAIVE_BAYES

    elif(args.svm):
        classifierType = ClassifierType.SVM

    elif(args.dt):
        classifierType = ClassifierType.DECISION_TREE

    elif(args.knn):
        classifierType = ClassifierType.KNN
        data = args.knn

    else:
        print("Error! No classifier selected.")
        exit(1)

    return dataset, classifierType, data


def process_text(text: str):
    """
    Description:
        Process the text fetched from a given dataset.

    Parameters:
        text: The text to process.

    Returns:
        text: The processed text.
    """

    stop_words = set(nltk.corpus.stopwords.words('english'))
    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
    return text.apply(lambda x: ' '.join([word for word in tokenizer.tokenize(x.lower()) if word not in stop_words]))


def init_classifier(dataset_file_name: str, classifierType: ClassifierType, n: Union[int, None]):
    """
    Description:
        Initialize the classifier and vectorizer.

    Parameters:
        dataset_file_name: The name of the dataset file.
        classifierType: the type of classifier to use.
        n: The n value to use if KNN is chosen as the classifier.

    Returns:
        vectorizer: The vectorizer.
        classifier: The classifier.
        X: The X.
        Y: The Y.
    """
    file_name = f"data/training_sentiment/{dataset_file_name}"
    data = pandas.read_csv(file_name, sep='\t', header=None)
    text = process_text(data[0])

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(text)
    Y = data[1]

    if(classifierType == ClassifierType.NAIVE_BAYES):
        classifier = MultinomialNB()

    elif(classifierType == ClassifierType.KNN):
        classifier = SVC()

    elif(classifierType == ClassifierType.SVM):
        classifier = DecisionTreeClassifier()

    elif(classifierType == ClassifierType.DECISION_TREE):
        classifier = KNeighborsClassifier(n)

    classifier.fit(X, Y)
    return vectorizer, classifier, X, Y


def calculate_performance_metrics(X, Y, y_pred):
    """
    Description:
        Calculate the performance metrics.

    Parameters:
        classifier: The classifier.
        X: The X.
        Y: The Y.

    Returns:
        accuracy: The accuracy.
        precision: The precision.
        recall: The recall.
        f1: The f1 score.
    """
    accuracy = accuracy_score(Y, y_pred)
    precision = precision_score(Y, y_pred, average="macro")
    recall = recall_score(Y, y_pred, average="macro")
    f1 = f1_score(Y, y_pred, average="macro")

    return accuracy, precision, recall, f1


def calculate_cross_validation_performance_metrics(classifier, X, Y, kf):
    """
    Description:
        Calculate the cross validation metrics.

    Parameters:
        classifier: The classifier.
        X: The X.
        Y: The Y.
        kf: The KFold object.

    Returns:
        accuracy: The accuracy of the classifier.
        precision: The precision of the classifier.
        recall: The recall of the classifier.
        f1: The f1 score of the classifier.
    """
    from sklearn.model_selection import cross_val_score
    accuracy = cross_val_score(classifier, X, Y, cv=kf, scoring="accuracy")
    precision = cross_val_score(classifier, X, Y, cv=kf, scoring="precision_macro")
    recall = cross_val_score(classifier, X, Y, cv=kf, scoring="recall_macro")
    f1 = cross_val_score(classifier, X, Y, cv=kf, scoring="f1_macro")

    return accuracy, precision, recall, f1


def save_confusion_matrix(X, Y, y_pred):
    """
    Description:
        Plot the confusion matrix.

    Parameters:
        classifier: The classifier.
        X: The X.
        Y: The Y.
    """
    matrix = confusion_matrix(Y, y_pred)
    sns.heatmap(matrix, annot=True, fmt="d")
    plt.xlabel("Predicted Label")
    plt.ylabel("Actual Label")
    plt.title("Confusion Matrix")
    plt.savefig(CONFUSION_MATRIX_FILE_NAME)
    return


def save_vectorizer_and_classifier(vectorizer, classifier):
    """
    Description:
        Save the vectorizer and classifier to the disk.

    Parameters:
        vectorizer: The vectorizer.
        classifier: The classifier.
    """
    with open("vectorizer.dat", "wb") as file:
        joblib.dump(vectorizer, file)

    with open("classifier.dat", "wb") as file:
        joblib.dump(classifier, file)

    return


def main():
    """
    Description:
        The main function.
    """
    nltk.download("stopwords")
    nltk.download("punkt")

    args = arg_handler()
    dataset, classifierType, data = parse_args(args)

    vectorizer, classifier, X, Y = init_classifier(dataset, classifierType, data)
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    y_pred = classifier.predict(X)

    # Calculate performance metrics
    accuracy, recall, precision, f1 = calculate_performance_metrics(X, Y, y_pred)
    print(f"Performance Metrics - {dataset} - {classifierType}:")
    print(f"")

    print("Performance of Classification:\n\tAccuracy: {:.3f}\n\tRecall: {:.3f}\n\tPrecision: {:.3f}\n\tF1-score: {:.3f}".format(accuracy, recall, precision, f1))

    # Calculate performance metrics with cross-validation
    cross_accuracy, cross_recall, cross_precision, cross_f1 = calculate_cross_validation_performance_metrics(classifier, X, Y, kf)
    print("Evaluation of Performance with Cross-Validation:\n\tAccuracy: {:.3f}\n\tRecall: {:.3f}\n\tPrecision: {:.3f}\n\tF1-score: {:.3f}".format(np.mean(cross_accuracy), np.mean(cross_recall), np.mean(cross_precision), np.mean(cross_f1)))

    # Plot the confusion matrix
    save_confusion_matrix(X, Y, y_pred)

    # Save the vectorizer and classifier
    save_vectorizer_and_classifier(vectorizer, classifier)
    return


if (__name__ == "__main__"):
    main()
