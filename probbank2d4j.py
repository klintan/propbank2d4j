import sys, os
import re
import nltk
from nltk.corpus import propbank
from nltk import Tree
from copy import deepcopy

pb_instances = propbank.instances()
raw_sentence = []
predicates = []
arguments_list = []
new_sentence = []
x = 0

def findItem(theList, item):
    return [(ind, theList[ind].index(item)) for ind in xrange(len(theList)) if item in theList[ind]]

def addPredicateLabel(raw_sentence, instance):
    if(len(findItem(raw_sentence,instance.predicate.select(instance.tree).leaves()[0]))):
        predicate_index = findItem(raw_sentence,instance.predicate.select(instance.tree).leaves()[0] )[0][0]
        raw_sentence[predicate_index] = ["<"+instance.roleset+">"+raw_sentence[predicate_index][0]+"</"+instance.roleset+">" ]

def addArgumentLabel(raw_sentence, instance):
    for (argloc, argid) in instance.arguments:
        arguments_list =[]
        if (argloc.select(instance.tree).label() != "-NONE-"):
            arguments = argloc.select(instance.tree).leaves()
            for arg in arguments:
                #print arg
                if not '*' in arg:
                    arguments_list.append(arg)

        new_sentence = [item for sublist in raw_sentence_preflat for item in sublist]
        a = new_sentence
        b = arguments_list
        seguence_index = [(i, i+len(b)) for i in range(len(a)) if a[i:i+len(b)] == b]

        if len(seguence_index)>0:
            raw_sentence[seguence_index[0][0]].insert(0,"<"+argid+">")
            raw_sentence[seguence_index[0][1]-1].append("</"+argid+">")




#iterate through all the instances in the dataset
#9351 is the max
for i in range(0, 9351):
    print i
    next_instance = pb_instances[i+1]
    #active instance
    instance = pb_instances[i]
    if x == 0:
        for s in instance.tree.subtrees(lambda t: t.height() == 2):
            if (s.label() != "-NONE-"):
                raw_sentence.append(s.leaves())
        raw_sentence_preflat = deepcopy(raw_sentence)
    x=1

    #save all predicates for one file and their position
    if(instance.sentnum==next_instance.sentnum):
        #add labels for argument spans
        addArgumentLabel(raw_sentence,instance)
        #add the predicate/roleset label
        addPredicateLabel(raw_sentence, instance)
    else:
        #add labels for argument spans
        addArgumentLabel(raw_sentence,instance)
        #add the predicate/roleset label
        addPredicateLabel(raw_sentence, instance)

        #join sentence
        raw_sentence = ' '.join([item for sublist in raw_sentence for item in sublist])

        #save the sentence in the file
        with open("label_data.txt", "a") as text_file:
            text_file.write(raw_sentence + "\n")

        #clear all variables
        x = 0
        raw_sentence = []
        predicates = []

    #set x to 0 if we have a new file
    if(next_instance.fileid != instance.fileid):
        x = 0
        raw_sentence = []



