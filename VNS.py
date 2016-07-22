# Author: Isabella de Albuquerque Ceravolo
# Program that uses VNS to solve the graph coloring problem

import networkx as nx
#import graphviz as gv
import timeit
from random import randint

# Creates the graph to be colored and applies an initial color to its vertices
# f_name - name of the file that contains the graph definition
def initialization(f_name):
	index = 1
	graph = nx.Graph()
	edges_file = open(f_name, 'r')
	
	#
	print "DEBUG: lendo o arquivo."
	#
	for line in edges_file:
		line = line.replace("\n", "")
		#
		print "Linha: " + line
		#
		nodes = line.split("\t")
		#
		print "Nodos: " + nodes
		#
		for n in nodes:
			node = int(n)
			if(not graph.has_node(node)):
				graph.add_node(node, color = index)
				index += 1
		
		graph.add_edge(int(nodes[0]), int(nodes[1]))
	
	edges_file.close()
	#
	print "FIM: lendo o arquivo."
	#
	return graph


# Perturbs the current solution by randomly choosing two vertices and swapping its colors
# graph - the solution to be pertubed
def perturbation(graph, k):
	#
	print "DEBUG: perturbando solução."
	#
	for i in range(1, k + 1):
		node1 = randint(1, graph.number_of_nodes())
		node2 = randint(1, graph.number_of_nodes())
		#
		print "Nodos: " + str(node1) + str(node2)
		#
		
		aux = graph.node[node1]['color']
		graph.node[node1]['color'] = graph.node[node2]['color']
		graph.node[node2]['color'] = aux
		#
		print "Nodos: " + str(graph.node[node1]['color']) + str(graph.node[node2]['color'])
	print "FIM: perturbando solução."
	#
	return graph
'''
# Tests if all nodes of a graph respects the color constraint
# graph - the solution to be verified 
def is_valid(graph, node):
	#
	print "DEBUG: verificando se a solução é válida."
	#
	node_color = graph.node[node]['color']
	
	#
	print "Nodo: " + str(node)
	#
	
	for item in graph[node]:
		current_item = graph.node[item]
		#
		print "Vizinho: " + current_item
		#
		if (current_item['color'] == node_color):
			#
			print "FIM: -FALSE- verificando se a solução é válida."
			#
			return False
	#
	print "FIM: -TRUE- verificando se a solução é válida."
	#		
	return True
	

def has_conflict(G):
	for i in G.nodes():
		item = graph.node[i]
		
		for j in G[i]:
			current_item = graph.node[j]
			
			if (current_item['color'] == current_item['color']):
				return True
			
	return False


def local_search(G, colors):
	
	index = random.randint(1, G.number_of_nodes())
	selected_node = G.node[index]
	possible_colors = colors[:]
	x = selected_node['color']
	y = possible_colors.index(x)
	del possible_colors[y]
	selected_node['color'] = random.randint(0, len(possible_colors))
	if (is_valid(G, index)):
		return G
	else:
		return None
'''

def possible_colors(graph, node, colors):
	allowed = colors[:]
	
	c = graph.node[node]['color']
	pos = colors.index(c)
	del allowed[pos]
		
	for n in graph.neighbors(node):
		c = graph.node[n]['color']
		if (c in allowed):
			pos = colors.index(c)
			del allowed[pos]
	
	return allowed
	

# Executes the VNS algoritm
def vns(G, K, T):
	# Parameter initialization
	nb_nodes = G.number_of_nodes()
	colors = list(range(1, nb_of_nodes + 1))
	best = G.copy()
	change = False
	attempts = 0
			
	for i in range(0, T):
		
		# Local search
		selected_node = random.randint(1, G.number_of_nodes())
		possibilities = possible_colors(G, selected_node, colors)
		if (len(possibilities) > 0):
			graph.node[node]['color'] = possibilities[0]
			change = True
				
		if (change):
			attempts = 0
			if (has_conf(G)):
				best = G
		else:
			attempts += 1
		
		# Apply a perturbation
		if (attempts == K):
			G = perturbation(G)
	
	return best

# Plots a solution using Graphviz lib
# graph - the solution to be transformed in an image
def plot_solution(graph, name):
	image_name = "solution_" + name
	G = gv.Graph(format='png')
	
	for node in graph.nodes():
		G.node(str(node), str(graph.node[node]['color']))
	
	for edge in graph.edges():
		G.edge(str(edge[0]), str(edge[1]))
	
	G.render(filename = image_name)

# Main program
def main():
	print "Initiating Graph Coloring Tool..."
	print "Hello!"
	
	file_name = raw_input("Please, enter with the name of the file containing the graph definition.\n").strip()
	G = initialization(file_name)
	K = int(input("Please, enter with the number of perturbations (K).\n"))
	T = int(input("Please, enter with the number of iterations (T).\n"))
	
	print "Working on a solution..."
	solution = vns(G, K, T)
	print "Done!"
	
	plot_solution(solution)
	print "Check the current folder to see the image that illustrates the result. =D"
	
# Starts the main program
main()
