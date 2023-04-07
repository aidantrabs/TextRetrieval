import argparse
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.metrics import adjusted_rand_score, completeness_score, adjusted_mutual_info_score
from sklearn.cluster import FeatureAgglomeration 
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pickle
import nltk

def preprocess_data():
     """
     Description:
          Preprocess the data.
     Parameters:
          None
     Returns:
          preprocessed_data: the preprocessed data.
     """

     data = fetch_20newsgroups(subset='all', remove=('headers', 'footers', 'quotes'))     
     data = [d[1] for d in data]
     data = [nltk.word_tokenize(d) for d in data]

     stop_words = nltk.corpus.stopwords.words('english')

     stemmer = nltk.stem.PorterStemmer()
     lemmatizer = nltk.stem.WordNetLemmatizer()

     data = [[stemmer.stem(lemmatizer.lemmatize(w.lower())) for w in d if w not in stop_words] for d in data]

     vectorizer = TfidfVectorizer()
     data = vectorizer.fit_transform(data)

     scaler = StandardScaler(with_mean=False)
     data = scaler.fit_transform(data)

     x_train, x_test, y_train, y_test = train_test_split(data, data, test_size=0.2, random_state=42)
     preprocessed_data = (x_train, x_test, y_train, y_test)

     return preprocessed_data

def cluster_data(preprocessed_data, ncluster, clustering_method):
     """
     Description:
          Cluster the data.
     Parameters:
          preprocessed_data: the preprocessed data.
          ncluster: the number of clusters.
          clustering_method: the clustering method.
     Returns:
          None
     """

     x_train, x_test, y_train, y_test = preprocessed_data

     if clustering_method == "kmeans":
          clustering = KMeans(n_clusters=ncluster, random_state=42).fit(x_train)
     elif clustering_method == "whc":
          clustering = FeatureAgglomeration(n_clusters=ncluster).fit(x_train)
     elif clustering_method == "ac":
          clustering = AgglomerativeClustering(n_clusters=ncluster).fit(x_train)
     elif clustering_method == "dbscan":
          clustering = DBSCAN(eps=0.3, min_samples=10).fit(x_train)

     y_pred = clustering.predict(x_test)

     print("Adjusted Rand Score: ", adjusted_rand_score(y_test, y_pred))
     print("Completeness Score: ", completeness_score(y_test, y_pred))
     print("Adjusted Mutual Info Score: ", adjusted_mutual_info_score(y_test, y_pred))
     
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
     parser.add_argument("--ncluster", type=int, nargs="+", default=[20], help="Tells script about the number of cluster(s)")
     parser.add_argument("--kmeans", help="Tells script to use KMeans clustering", action="store_true")
     parser.add_argument("--whc", help="Tells script to use Ward Hierarchical Clustering", action="store_true")
     parser.add_argument("--ac", help="Tells script to use Agglomerative clustering", action="store_true")
     parser.add_argument("--dbscan", help="Tells script to use DBSCAN clustering", action="store_true")
     args = parser.parse_args()

     return args

def main():
     """
     Description:
          The main function.
     """
     
     args = arg_handler()

     preprocessed_data = preprocess_data()

     for ncluster in args.ncluster:
          if args.kmeans:
               cluster_data(preprocessed_data, ncluster, "kmeans")
          if args.whc:
               cluster_data(preprocessed_data, ncluster, "whc")
          if args.ac:
               cluster_data(preprocessed_data, ncluster, "ac")
          if args.dbscan:
               cluster_data(preprocessed_data, ncluster, "dbscan")
     
if __name__ == "__main__":
     main()
