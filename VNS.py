# Author: Isabella de Albuquerque Ceravolo
# Program that uses VNS to solve the graph coloring problem

import networkx as nx
import graphviz as gv
from random import randint

# Creates the graph to be colored and applies an initial color to its vertices
# f_name - name of the file that contains the graph definition
def initialization(f_name):
	index = 1
	graph = nx.Graph()
	edges_file = open(f_name, 'r')
	
	for line in edges_file:
		line = line.replace("\n", "")
		nodes = line.split("\t")
		for n in nodes:
			node = int(n)
			if(not graph.has_node(node)):
				graph.add_node(node, color = index)
				index += 1
		
		graph.add_edge(int(nodes[0]), int(nodes[1]))
	
	edges_file.close()
	return graph


# Perturbs the current solution by randomly choosing two vertices and swapping its colors
# graph - the solution to be pertubed
def perturbation(graph, k):
	for i in range(1, k + 1):
		node1 = randint(1, graph.number_of_nodes())
		node2 = randint(1, graph.number_of_nodes())
		
		aux = graph.node[node1]['color']
		graph.node[node1]['color'] = graph.node[node2]['color']
		graph.node[node2]['color'] = aux
		
	return graph


# Select all the other colors that can be used in a certain node
# graph - the graph being colored
# node - the node which we will try to change its color
# colors - vector with all color used in the graph
def possible_colors(graph, node):
	colors = []
	for n in graph.nodes():
		c = graph.node[n]['color']
		if (not c in colors):
			colors.append(c) 
	
	c = graph.node[node]['color']
	pos = colors.index(c)
	del colors[pos]
		
	for n in graph.neighbors(node):
		c = graph.node[n]['color']
		if (c in colors):
			pos = colors.index(c)
			del colors[pos]
	
	return colors
	

# Verify if the graph complain with the color constraint
# graph - the graph to be validated
def is_valid(graph):
	for i in graph.nodes():
		item = graph.node[i]
		
		for j in graph[i]:
			current_item = graph.node[j]
			if (item['color'] == current_item['color']):
				return False
	
	return True


# The VNS algoritm
# G - the graph to be colored
# K - number of attempts before a perturbation
# T - number of local searches to be executed
def vns(G, K, T):
	# Parameter initialization
	nb_nodes = G.number_of_nodes()
	best = G.copy()
	change = False
	attempts = 0
			
	for i in range(0, T):
		# Local search
		selected_node = randint(1, G.number_of_nodes())
		possibilities = possible_colors(G, selected_node)
		if (len(possibilities) > 0):
			G.node[selected_node]['color'] = possibilities[0]
			change = True
				
		if (change):
			attempts = 0
			change = False
			if (is_valid(G)):
				best = G.copy()
		else:
			attempts += 1
		
		# Apply a perturbation
		if (attempts == K):
			G = perturbation(G, K)
	
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
	
	plot_solution(solution, file_name)
	print "Check the current folder to see the image that illustrates the result. ;)"
	
# Starts the main program
main()
