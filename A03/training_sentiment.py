import argparse

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

def train_with_dataset(dataset_file_name: str):
     """
     Description:
          Train the ML model.
     Parameters:
          dataset_file: the file containing the dataset.
     Returns:
          None
     """
     with open(f"data/training_sentiment_${dataset_file_name}") as f:
          for line in f:
               print(line, end="")
               print(line.strip().split(" "))
               print(line.strip().split(" ")[-1])
               break

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
          print("Naive Bayes")

     if(args.svm):
          print("Support Vector Machine")

     if(args.dt):
          print("Decision Tree")

     if(args.knn):
          print("K-Nearest Neighbors")



     return

if __name__ == "__main__":
     main()
