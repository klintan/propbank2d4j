#!/usr/bin/python

import sys, os
import re
import nltk
from nltk.corpus import propbank
from nltk import Tree
from copy import deepcopy

class probank2d4j:
    'Class to create deeplearning4j (0.3.3.3) training data for RTNT '

    def __init__(self, filename="data.txt", mode=0):
        self.instances = propbank.instances()
        self.raw_sentence = []
        self.predicates = []
        self.arguments_list = []
        self.new_sentence = []
        self.x = 0
        self.filename = filename
        self.mode = mode

    def findItem(self, activelist, item):
        return [(ind, activelist[ind].index(item)) for ind in xrange(len(activelist)) if item in activelist[ind]]

    def addPredicateLabel(self, raw_sentence, instance):
        if(len(self.findItem(raw_sentence,instance.predicate.select(instance.tree).leaves()[0]))):
            predicate_index = self.findItem(raw_sentence,instance.predicate.select(instance.tree).leaves()[0] )[0][0]
            raw_sentence[predicate_index] = ["<"+instance.roleset+">"+raw_sentence[predicate_index][0]+"</"+instance.roleset+">" ]

    def addArgumentLabel(self, raw_sentence, instance):
        for (argloc, argid) in instance.arguments:
            arguments_list =[]
            if (argloc.select(instance.tree).label() != "-NONE-"):
                arguments = argloc.select(instance.tree).leaves()
                for arg in arguments:
                    #print arg
                    if not '*' in arg:
                        arguments_list.append(arg)

            new_sentence = [item for sublist in raw_sentence_preflat for item in sublist]
            seguence_index = self.getIndexOfSequence(arguments_list,new_sentence)

            if len(seguence_index)>0:
                raw_sentence[seguence_index[0][0]].insert(0,"<"+argid+">")
                raw_sentence[seguence_index[0][1]-1].append("</"+argid+">")

    def getIndexOfSequence(self, sequence, activelist):
            return [(i, i+len(sequence)) for i in range(len(activelist)) if activelist[i:i+len(sequence)] == sequence]

    def saveAnnotatedSentence(self, sentence_list):
        #join sentence
        sentence = ' '.join([item for sublist in sentence_list for item in sublist])
        #save the sentence in the file
        with open(self.filename, "a") as text_file:
            text_file.write(sentence + "\n")


if __name__ == "__main__":
    pb2d4j = probank2d4j()
    #iterate through all the instances in the dataset
    #9351 is the max
    for i in range(0, 9351):
        print i
        next_instance = pb2d4j.instances[i+1]
        #active instance
        instance = pb2d4j.instances[i]
        if pb2d4j.x == 0:
            for s in instance.tree.subtrees(lambda t: t.height() == 2):
                if (s.label() != "-NONE-"):
                    pb2d4j.raw_sentence.append(s.leaves())
            raw_sentence_preflat = deepcopy(pb2d4j.raw_sentence)
        pb2d4j.x=1

        #save all predicates for one file and their position
        if(instance.sentnum==next_instance.sentnum):
            #add labels for argument spans
            pb2d4j.addArgumentLabel(pb2d4j.raw_sentence,instance)
            #add the predicate/roleset label
            pb2d4j.addPredicateLabel(pb2d4j.raw_sentence, instance)

        else:
            #add labels for argument spans
            pb2d4j.addArgumentLabel(pb2d4j.raw_sentence,instance)
            #add the predicate/roleset label
            pb2d4j.addPredicateLabel(pb2d4j.raw_sentence, instance)

            pb2d4j.saveAnnotatedSentence(pb2d4j.raw_sentence)
            #clear all variables
            pb2d4j.x = 0
            pb2d4j.raw_sentence = []

        #set x to 0 if we have a new file
        if(next_instance.fileid != instance.fileid):
            x = 0
            raw_sentence = []



