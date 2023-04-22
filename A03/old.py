def tokenize_text(text: str):
     """
     Description:
     Tokenizes the text.

     Parameters:
     text (str): The text to tokenize.

     Returns:
     (List[str]): The list of tokens.
     """
     return nltk.word_tokenize(text)


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





def process_dataset(dataset_file_name: str):
    """
    Description:
        Process the dataset.
    Parameters:
        dataset_file_name: the name of the dataset file.
    Returns:
        None
    """
    file_name = f"data/training_sentiment/{dataset_file_name}"
    data = pandas.read_csv(file_name, sep='\t', header=None)
    result = {}

    for index, row in data.iterrows():
        sentence = row[0]
        sentiment = row[1]
        tokenized_sentence = tokenize_text( remove_stopwords(sentence) )
        for token in set(tokenized_sentence):
            result[token] = sentiment

    print(result)

    return



def train_with_dataset(dataset_file_name: str, classType: ClassifierType):
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
    if (classType == ClassifierType.NAIVE_BAYES):
        classifier = MultinomialNB()

    elif (classType == ClassifierType.KNN):
        classifier = KNeighborsClassifier(knnInteger)

    elif (classType == ClassifierType.SVM):
        classifier = SVC()

    elif (classType == ClassifierType.DECISION_TREE):
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
