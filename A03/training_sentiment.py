import argparse
import enum
import joblib
import matplotlib.pyplot as plt
import nltk
import nltk.corpus
import nltk.stem
import nltk.tokenize
import numpy
import pandas
import seaborn as sns
import sklearn
import sklearn.metrics
import sklearn.naive_bayes
import sklearn.neighbors
import sklearn.svm
import sklearn.tree

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import KFold, cross_val_score
from typing import Union

CONFUSION_MATRIX_FILE_NAME = "confusion_matrix.png"
VECTORIZER_OUTPUT_FILE_NAME = "vectorizer.joblib"
CLASSIFIER_OUTPUT_FILE_NAME = "classifier.joblib"

class ClassifierType(enum.Enum):
    NAIVE_BAYES = 1,
    KNN = 2,
    SVM = 3,
    DECISION_TREE = 4


def arg_handler():
    """
    Description:
        Handle the arguments using argparse.

    Returns:
        args: the arguments in a map structure.
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
    classifier.add_argument("--knn", action="store", nargs=1, type=int, help="Use the K-Nearest Neighbors algorithm for training the classifier.")
    return parser.parse_args()


def parse_args(args: object):
    """
    Description:
        Parse the arguments collected by argparse and retrieve the dataset and classifier to use.

    Parameters:
        args: The arguments returned by arg_handler.

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
        data = args.knn[0]

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
        vectorizer: The count vectorizer.
        classifier: The classifier fitted with the X and Y vector.
        X: The X vector.
        Y: The Y vector.
    """
    file_name = f"data/training_sentiment/{dataset_file_name}"
    data = pandas.read_csv(file_name, sep='\t', header=None)
    text = process_text(data[0])

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(text)
    Y = data[1]

    if(classifierType == ClassifierType.NAIVE_BAYES):
        classifier = sklearn.naive_bayes.MultinomialNB()

    elif(classifierType == ClassifierType.KNN):
        classifier = sklearn.neighbors.KNeighborsClassifier(n)

    elif(classifierType == ClassifierType.SVM):
        classifier = sklearn.svm.SVC()

    elif(classifierType == ClassifierType.DECISION_TREE):
        classifier = sklearn.tree.DecisionTreeClassifier()

    classifier.fit(X, Y)
    return vectorizer, classifier, X, Y


def calculate_performance_metrics(Y, y_pred):
    """
    Description:
        Calculate the performance metrics using the given vectors.

    Parameters:
        Y: The Y vector.
        y_pred: The predicted Y vector.

    Returns:
        accuracy: The accuracy of the classifier.
        precision: The precision of the classifier.
        recall: The recall of the classifier.
        f1: The f1 score of the classifier.
    """
    accuracy = sklearn.metrics.accuracy_score(Y, y_pred)
    precision = sklearn.metrics.precision_score(Y, y_pred, average="macro")
    recall = sklearn.metrics.recall_score(Y, y_pred, average="macro")
    f1 = sklearn.metrics.f1_score(Y, y_pred, average="macro")

    return accuracy, precision, recall, f1


def calculate_cross_validation_performance_metrics(classifier, X, Y, kf):
    """
    Description:
        Calculate the cross validation performance metrics of a given classifier.

    Parameters:
        classifier: The classifier.
        X: The X vector.
        Y: The Y vector.
        kf: The KFold object.

    Returns:
        accuracy: The accuracy of the classifier.
        precision: The precision of the classifier.
        recall: The recall of the classifier.
        f1: The f1 score of the classifier.
    """
    accuracy = numpy.mean(cross_val_score(classifier, X, Y, cv=kf, scoring="accuracy"))
    precision = numpy.mean(cross_val_score(classifier, X, Y, cv=kf, scoring="precision_macro"))
    recall = numpy.mean(cross_val_score(classifier, X, Y, cv=kf, scoring="recall_macro"))
    f1 = numpy.mean(cross_val_score(classifier, X, Y, cv=kf, scoring="f1_macro"))

    return accuracy, precision, recall, f1


def print_metrics(title: str, dataset: str, classifierType: ClassifierType, accuracy: float, precision: float, recall: float, f1: float):
    """
    Description:
        Print the performance metrics.

    Parameters:
        title: The title of the print.
        dataset: The dataset used.
        classifierType: The classifier type used.
        accuracy: The accuracy of the classifier.
        precision: The precision of the classifier.
        recall: The recall of the classifier.
        f1: The f1 score of the classifier.
    """
    print()
    print(f"{title} | {dataset} using {classifierType.name}:")
    print("==============================================")
    print(f"Accuracy: {accuracy:.5f}")
    print(f"Precision: {precision:.5f}")
    print(f"Recall: {recall:.5f}")
    print(f"F1: {f1:.5f}")
    print("==============================================")
    print()
    return


def save_confusion_matrix(Y, y_pred):
    """
    Description:
        Save the confusion matrix to the disk.

    Parameters:
        Y: The Y vector.
        y_pred: The predicted Y vector.
    """
    matrix = sklearn.metrics.confusion_matrix(Y, y_pred)

    sns.heatmap(matrix, fmt="d", annot=True)
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted Label")
    plt.ylabel("Actual Label")
    plt.savefig(CONFUSION_MATRIX_FILE_NAME)
    return


def serialise_model(vectorizer, classifier):
    """
    Description:
        Save and dump the vectorizer and classifier to the disk.

    Parameters:
        vectorizer: The vectorizer.
        classifier: The classifier.
    """
    with open(VECTORIZER_OUTPUT_FILE_NAME, "wb") as file:
        joblib.dump(vectorizer, file)

    with open(CLASSIFIER_OUTPUT_FILE_NAME, "wb") as file:
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

    accuracy, recall, precision, f1 = calculate_performance_metrics(Y, y_pred)
    accuracy_c, recall_c, precision_c, f1_c = calculate_cross_validation_performance_metrics(classifier, X, Y, kf)
    print_metrics("Performance Metrics", dataset, classifierType, accuracy, precision, recall, f1)
    print_metrics("Cross Validation Performance Metrics", dataset, classifierType, accuracy_c, precision_c, recall_c, f1_c)
    save_confusion_matrix(Y, y_pred)
    serialise_model(vectorizer, classifier)
    return


if (__name__ == "__main__"):
    main()
