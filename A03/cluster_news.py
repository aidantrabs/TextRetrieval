import argparse
from skslearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.metrics import adjusted_rand_score, completeness_score, adjusted_mutual_info_score
from sklearn.cluster import FeatureAgglomeration 

def preprocess_data(data):
     """
     Description:
          Preprocess the data.
     Parameters:
          data
     Returns:
          data
     """
     
     return data

def cluster_news(ncluster: int, kmeans: bool, whc: bool, ac: bool, dbscan: bool):
     """
     Description:
          Cluster the news.
     Parameters:
          ncluster: the number of clusters.
          kmeans: whether to use KMeans.
          whc: whether to use Ward Hierarchical Clustering.
          ac: whether to use Agglomerative Clustering.
          dbscan: whether to use DBSCAN.
     Returns:
          None
     """
     pass

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
     parser.add_argument("-ncluster", type=int, nargs="+", default=[20], help="Tells script about the number of cluster(s)")
     parser.add_argument("--kmeans", help="Tells script to use KMeans clustering")
     parser.add_argument("--whc", help="Tells script to use Ward Hierarchical Clustering")
     parser.add_argument("--ac", help="Tells script to use Agglomerative clustering")
     parser.add_argument("--dbscan", help="Tells script to use DBSCAN clustering")

def main():
     """
     Description:
          The main function.
     """
     pass

if __name__ == "__main__":
     main()
