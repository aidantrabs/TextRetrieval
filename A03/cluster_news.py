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