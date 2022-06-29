"""
A file with a method that generates random genetic sequences 
of a specified length using msprime. Also has a method to covert
lists/matrices of single nucleotides into lists of strings.
"""

import msprime
import tskit
import numpy as np
import random

def generate_sequences(length,number=1,recomb_rate=0):
    """
    Generates random sequences of length "length" using 
    msprime. The resulting sequences are returned as a matrix of 
    nucleotides with each row corresponding to a sequence.
    
    Optionally takes an argument corresponding to the number of
    random sequences we wish to generate and a parameter for what
    the recombination rate for the msprime simulation should be.
    """
    
    letters = ["A","C","G","T"]
    
    if number == 1:
        return np.array([[random.choice(letters) for _ in range(length)]])
    
    ts = msprime.sim_ancestry(number, population_size=100, recombination_rate = recomb_rate, ploidy=1,sequence_length=length)
    mts = msprime.sim_mutations(ts, rate=0.001)
    
    basics = list(mts.alignments())
    
    broken_basics = np.array(list(map(lambda x: [c for c in x],basics)))
    
    
    for index in range(broken_basics.shape[1]):
        if broken_basics[0,index] == "N":
            new_genotype = random.choice(letters)
            broken_basics[:,index] = new_genotype
    
    return broken_basics

def seq_strs(seq_array):
    """
    Converts a 1D/2D sequence of characters into a 1D list of
    string by concatenating each row into a single string
    """
    str_list = []
    if seq_array.ndim == 2:
        for i in range(seq_array.shape[0]):
            str_list.append("".join(seq_array[i,:]))

    else:        
        str_list.append("".join(seq_array))
    
    return str_list