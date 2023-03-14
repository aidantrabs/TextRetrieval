import argparse
import re

DATA_SET = "data/web-Stanford.txt"

def load_data():
     """
     Description:
          Load the data set.
     Parameters:
          None
     Returns:
          graph: the graph of nodes.
          outbound: the number of outbound links for each node.
     """
     graph = {}
     outbound = {}

     with open(DATA_SET, "r") as f:
          for line in f.readlines():
               if line.startswith("#"):
                    continue

               nodes = line.strip().split()
               from_node = nodes[0]
               to_node = nodes[1]

               if to_node not in graph:
                    graph[to_node] = []

               if from_node not in graph:
                    graph[from_node] = []

               if from_node not in outbound:
                    outbound[from_node] = 0

               graph[to_node].append(from_node)
               outbound[from_node] += 1

     return graph, outbound

def page_rank(prev, curr, graph, outbound, lambda_, num_nodes):
     """
     Description:
          Calculate the PageRank for each node.
     Parameters:
          prev: the previous PageRank values.
          curr: the current PageRank values.
          graph: the graph of nodes.
          outbound: the number of outbound links for each node.
          num_nodes: the number of nodes.
     Returns:
          curr: the current PageRank values.
     """
     for node in graph:
          rank = lambda_ / num_nodes

          for neighbor in graph[node]:
               try:
                    node_length = outbound[neighbor]
                    node_rank = prev[neighbor]
               except:
                    node_length = 1
                    node_rank = 1

               rank += (1 - lambda_) * (node_rank / node_length)

          curr[node] = rank

     return curr

def page_rank_handler(graph, outbound, maxiteration, lambda_, thr, nodes):
     """
     Description:
          Handle the PageRank algorithm.
     Parameters:
          graph: the graph of nodes.
          outbound: the number of outbound links for each node.
          maxiteration: the maximum number of iterations to stop if algorithm has not converged.
          lambda_: the λ parameter value.
          thr: the threshold value to stop if algorithm has converged.
          nodes: the NodeIDs that we want to get their PageRank values at the end of iterations.
     Returns:
          None
     """
     num_nodes = len(graph)
     nodes = set(nodes)
     prev = {node: 1 / num_nodes for node in graph}
     curr = {node: 1 / num_nodes for node in graph}

     for i in range(maxiteration):
          print("Iteration: ", i)
          curr = page_rank(prev, curr, graph, outbound, lambda_, num_nodes)

          if all(abs(curr[node] - prev[node]) < thr for node in graph):
               print("Converged at iteration: ", i)
               break

          prev = curr

     page_rank_sorted = sorted(curr.items(), key=lambda x: x[1], reverse=True)
     for node, rank in page_rank_sorted:
          if node in nodes:
               print("NodeID: ", node, "\t", "PageRank: ", rank)
          else:
               print("NodeID: ", node, "\t", "PageRank: ", rank, " (not in the list of nodes to be printed)")

     return

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
     parser.add_argument("--nodes", type=int, nargs="+", default=[1, 2, 3, 4, 5], help="the NodeIDs that we want to get their PageRank values at the end of iterations.") 
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

     graph, outbound = load_data()
     page_rank_handler(graph, outbound, args.maxiteration, args.lambda_, args.thr, args.nodes)

     return

if __name__ == "__main__":
     main() 