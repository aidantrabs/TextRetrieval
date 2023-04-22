"""
1. Load dataset(s) (option 1-3)
2. Tokenize and remove stopwords using NLTK library
3. Train the selected classifier (option 4-7)
4. Report (print) performance of classification in terms of Accuracy, Recall, Precision and F-Measure, Plot confusion matrix
5. Save the model
"""

#Imports
import sys
import os
import pandas as pd
import numpy as np
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split, cross_val_score, KFold, cross_validate
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import joblib


#Variables
DATASETS = {"--amazon":"amazon_cells_labelled.txt", "--imdb" : "imdb_labelled.txt", "--yelp" : "yelp_labelled.txt"}
CLASSIFIERS = {"--naive": 1, "--knn": 2, "--svm": 3, "--decisiontree": 4}
fileName = ""
saveName = "sentiment_classifier.joblib"
vectName = "vectorizer.joblib"
classType = 0
optionArg = 1
optionStr = ""
optionBool = True
knnInteger = 0

# Tokenize and remove stopwords from inputted text
def preprocess_text(text: str):
    stop_words = set(stopwords.words('english'))
    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
    processed_text = text.apply(lambda x: ' '.join([word for word in tokenizer.tokenize(x.lower()) if word not in stop_words]))

    return processed_text

def run():
    global optionBool, optionStr, optionArg, fileName, classType, knnInteger
    os.system('clear')

    #Search through commandline arguements for options
    try:
        #Retrieve data set choice
        optionStr = sys.argv[optionArg]
        fileName = os.path.join('sentiment_labelled_sentences',DATASETS[optionStr])

        #Retrieve classifer type
        optionArg += 1
        optionStr = sys.argv[optionArg]
        classType = CLASSIFIERS[optionStr]
        if(classType == 2):
            #Retrieve k value
            optionArg += 1
            optionStr = sys.argv[optionArg]
            knnInteger = int(optionStr)

    #Error in input
    except:

        #Error in dataset
        if(fileName == ""):
            print("Invalid dataset entered.\nPlease select one of the following:\n--imdb\n--amazon\n--yelp\n")

        #Error in classifer
        elif(classType > 4 or classType < 1):
            print("Invalid classifer entered.\nPlease select one of the following:\n--naive\n--knn\n--svm\n--decisiontree\n")

        optionBool = False

    if(classType == 2 and knnInteger <= 0):
        print("Invalid k value entered.\nPlease a positive integer for k\n")
        optionBool = False



    if (optionBool):
        # Load the dataset
        data = pd.read_csv(fileName, sep='\t',header=None)

        # Tokenize and remove stopwords
        processed_text = preprocess_text(data[0])

        # Split the dataset into training and testing sets
        #X_train, X_test, y_train, y_test = train_test_split(data[0], data[1], test_size=0.2, random_state=42)

        # Vectorize the text data
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(processed_text)
        Y = data[1]

        # Select classifier
        if (classType == 1):
            clf = MultinomialNB()

        elif(classType == 2):
            clf = KNeighborsClassifier(knnInteger)

        elif(classType == 3):
            clf = SVC()

        else:
            clf = DecisionTreeClassifier()

        # Train the classifier
        clf.fit(X, Y)

        # Define cross-validation technique
        kf = KFold(n_splits=5, shuffle=True, random_state=42)


        # Print performance metrics
        y_pred = clf.predict(X)
        accuracy = accuracy_score(Y, y_pred)
        recall = recall_score(Y, y_pred, average="macro")
        precision = precision_score(Y, y_pred, average="macro")
        f1 = f1_score(Y, y_pred, average="macro")
        print("Performance of Classification:\n\tAccuracy: {:.3f}\n\tRecall: {:.3f}\n\tPrecision: {:.3f}\n\tF1-score: {:.3f}".format(accuracy, recall, precision, f1))


        # Evaluate performance with cross-validation
        cross_accuracy = cross_val_score(clf, X, Y, cv=kf, scoring="accuracy")
        cross_recall = cross_val_score(clf, X, Y, cv=kf, scoring="recall_macro")
        cross_precision = cross_val_score(clf, X, Y, cv=kf, scoring="precision_macro")
        cross_f1 = cross_val_score(clf, X, Y, cv=kf, scoring="f1_macro")
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
            joblib.dump(clf, file)

        #Save the vectorizer
        with open(vectName, "wb") as file:
            joblib.dump(vectorizer, file)

if __name__ == '__main__':
    run()
