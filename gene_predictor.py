import sys
import networkx as nwx
from tkinter import messagebox
import numpy as np

sys.setrecursionlimit(50000)  # recursion limit improved

class network:
    Total_proteins = 0 # total proteins in the network
    Number_of_interactions= 0 # total interactions in the network
    unknown=[] # to store unknown proteins in the network

    single_function = {}  # storing proteins by function for reference
    multiple_functions = {} # storing functions and related proteins for reference
    method = None # one out of the two algorithms


    single_function_candidates = {} # store candidates proteins related to each function
    multiple_function_candidates = {} # store proteins with multiple functions


    predicted = {} # to store predicted mostly accurate function for each protein


    def init__(self, Total_proteins,Number_of_interactions,unknown): # class constructor
        self.Total_proteins = Total_proteins
        self.Number_of_interactions = Number_of_interactions
        self.unknown = unknown


    @ staticmethod
    def reference(): # making the references
        with  open("references.tsv", 'r') as unknown:  # making the reference list using "references.tsv"
            for line in unknown:
                if "GENE PRODUCT" not in line and line != '\n':
                    info = line.strip().split('\t')
                    symbol = info[2].upper() # protein
                    function = str(info[3]) + " " + str(info[5]) # function
                    if symbol in network.single_function: # reference list of candidate proteins for each function
                        list = set(network.single_function[symbol].split(','))
                        if function not in list:
                            network.single_function[symbol] = str(network.single_function[symbol]) + "," + function
                    else:
                        network.single_function[symbol] = function
                    if function in network.multiple_functions: # reference list of proteins with multiple functionalities
                        list = set(network.multiple_functions[function].split(','))
                        if symbol not in list:
                            network.multiple_functions[function] = str(network.multiple_functions[function]) + "," + str(symbol)
                    else:
                        network.multiple_functions[function] = symbol

    def prediction(input,m): # predictions with specified algorithm
        all = {} # to store

        if m == 1: # selected method is mv
            network.method ="Using majority Voting score"
        else: # selected method is hishigaki
            network.method = "Using Hishigaki method"

        for i in network.unknown:
            single_functions = {}  # making a dictionary of known proteins in the network by function for each protein
            list_neighbhours = input.neighbors(i)  # getting list of neighbors
            for p in list_neighbhours:
                for key in network.multiple_functions.keys():
                    values = str(network.multiple_functions[key]).split(",")
                    if p.upper() in values:  # grouping known proteins by function
                        if key in single_functions:
                            single_functions[key] = str(single_functions[key]) + "," + str(
                                p)  # updating values for already existing key
                        else:
                            single_functions[key] = p  # newly creating a key

            score={} # to store score using any of the two methods for predicting accurate function


            if single_functions != {}: # for proteins with at least one neighbor of known functionality
                if m == 1:  # selecting the algorithm as majority voting score
                    for n in single_functions.keys():  # evaluating neighbors with each functionality
                        string = single_functions[n]
                        list_nei = string.split(",")
                        score[n] = len(list_nei)  # taking the counts of neighbours to each function identified
                        # if len(list) != 0 :
                        if n in all.keys():  # key :- function, value :- related proteins with scores
                            all[n] = str(all[n]) + "," + str(i) + ":" + str(len(list_nei)) # grouping unknown proteins based on scores for known neighbors
                        else:
                            all[n] = str(i) + ":" + str(len(list_nei))

                else: # using hishigaki algorithm
                    for n in single_functions.keys():
                        string1 = single_functions[n]
                        list1 = string1.split(",")
                        nf = len(list1) # number of neighbors related to function under consideration
                        string2 = network.multiple_functions[n] # reference proteins related to function under consideration
                        list2 = string2.split(",")
                        known = [] # to store proteins identified in the network related to function under consideration
                        for m in input.nodes: # filtering all proteins identified in the network related to function under consideration
                            if m.upper() in list2:
                                known.append(m)
                        ef = (len(known) / network.Total_proteins) * nf # expected frequency of the function
                        hishigaki_score = ((nf - ef) ** 2 / ef)
                        score[n] = hishigaki_score

                        if n in all.keys(): # updating candidates for single function with calculated score
                            all[n] = str(all[n]) + "," + str(i) + ":" + str(hishigaki_score)
                        else:
                            all[n] = str(i) + ":" + str(hishigaki_score)

            if score != {}: # to get the most predicted functionality for each protein based on scores calculated
                sortd = sorted(score.items(), key=lambda item: item[1], reverse=1)  # sorted dictionary
                p = sortd[0]  # getting the protein record with highest majority voting score

                network.predicted[i] = str(p[0])


        for function in all.keys():
            values = all[function]
            list_val = values.split(',')
            candidates = {}
            for pair in list_val:
                splitted = pair.split(':')
                protein = splitted[0]
                m_score = splitted[1]

                candidates[protein] = m_score

            array = list(candidates.values())
            array = list(map(float,array))
            boundary = np.percentile(array,80)

            for i in candidates.keys(): # filtering candidates in 80th percentile
                if float(candidates[i]) > boundary:
                    if function in network.single_function_candidates.keys(): # updating candidates for single function
                        network.single_function_candidates[function] =  str(network.single_function_candidates[function])+','+str(i)
                    else :
                        network.single_function_candidates[function] = i

        for key in network.single_function_candidates.keys(): # finding candidates for multiple functions using
            # already found candidates for each single function
            values = network.single_function_candidates[key].split(',')
            for i in values:
                if i in network.multiple_function_candidates.keys():
                    network.multiple_function_candidates[i] = str(network.multiple_function_candidates[i])+','+str(key)
                else:
                    network.multiple_function_candidates[i] =  str(key)

    @staticmethod
    def network_graphing(input,method): # constructing network graph using networkx package
        network.reference()
        networkp = nwx.Graph()
        try:
            with  open(input, 'r') as unknown:  # user input file to construct the network
                for line in unknown:
                    if "#" not in line and line != '\n':
                        info = line.strip().split('\t')
                        networkp.add_edge(info[0], info[1], weight=float(info[12]))
            nwx.write_gml(networkp, ("protein.gml")) # output file :- constructed network for visualization
            network.Total_proteins = networkp.number_of_nodes()
            network.Number_of_interactions = networkp.number_of_edges()

            for i in networkp.nodes:
                if i.upper() not in network.single_function.keys(): # getting unknown proteins in the network
                    network.unknown.append(i)

            network.prediction(networkp, method)
        except: # when the tsv file content is invalid
            messagebox.showerror('', "Invalid file content ! ")










