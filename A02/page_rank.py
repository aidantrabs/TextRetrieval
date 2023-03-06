import argparse

DATA_SET = "data/test-web-Stanford.txt"

def load_data():
     """
     Description:
          Load the data from the data set.

     Parameters:
          None

     Returns:
          nodes: the set of nodes.
          edges: the list of edges.
     """
     nodes = set()
     edges = []
     with open(DATA_SET, 'r') as f:
          for line in f:
               line = line.strip()
               if not line.startswith('#'):
                    from_node, to_node = line.split('\t')
                    nodes.add(int(from_node))
                    nodes.add(int(to_node))
                    edges.append((int(from_node), int(to_node)))

     return nodes, edges

def init_page_rank(nodes):
     """
     Description:
          Initialize the PageRank values for all nodes.

     Parameters:
          nodes: the set of nodes.

     Returns:
          page_rank: the dictionary of PageRank values for all nodes.
     """
     page_rank = {}
     for node in nodes:
          page_rank[node] = 1 / len(nodes)

     return page_rank

def page_rank(nodes, edges, maxiteration, lambda_, thr, nodes_to_print):
     """
     Description:
          Calculate the PageRank values for all nodes.

     Parameters:
          nodes: the set of nodes.
          edges: the list of edges.
          maxiteration: the maximum number of iterations to stop if algorithm has not converged.
          lambda_: the λ parameter value.
          thr: the threshold value to stop if algorithm has converged.
          nodes_to_print: the NodeIDs that we want to get their PageRank values at the end of iterations.

     Returns:
          page_rank: the dictionary of PageRank values for all nodes.
     """
     page_rank = init_page_rank(nodes)
     for _ in range(maxiteration):
          new_page_rank = {}
          for node in nodes:
               new_page_rank[node] = (1 - lambda_) / len(nodes)
               for from_node, to_node in edges:
                    if to_node == node:
                         new_page_rank[node] += lambda_ * page_rank[from_node] / len([to_node for from_node, to_node in edges if from_node == from_node and to_node == node])
          if sum([abs(new_page_rank[node] - page_rank[node]) for node in nodes]) < thr:
               break
          page_rank = new_page_rank

     for node in nodes_to_print:
          if node in page_rank:
               print("NodeID: ", node, ", PageRank: ", page_rank[node])
          else:
               print("NodeID: ", node, " not found in input data")

     return page_rank

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
     parser.add_argument("--maxiteration", type=int, default=100, help="the maximum number of iterations to stop if algorithm has not converged.")
     parser.add_argument("--lambda_", type=float, default=0.85, help="the λ parameter value.")
     parser.add_argument("--thr", type=float, default=0.0001, help="the threshold value to stop if algorithm has converged.")
     parser.add_argument("--nodes", type=int, nargs="+", help="the NodeIDs that we want to get their PageRank values at the end of iterations.")
     args = parser.parse_args()

     return args

def main():
     """
     Description:
          Main function.

     Parameters:
          None

     Returns:
          None
     """
     args = arg_handler()

     print("maxiteration: ", args.maxiteration)
     print("lambda_: ", args.lambda_)
     print("thr: ", args.thr)
     print("nodes: ", args.nodes)

     nodes, edges = load_data()
     
     page_rank(nodes, edges, args.maxiteration, args.lambda_, args.thr, args.nodes)

if __name__ == "__main__":
     main() 