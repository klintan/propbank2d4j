#!/usr/bin/python

import sys, os
import re
import nltk
from nltk.corpus import propbank
from nltk import Tree
from copy import deepcopy

class probank2d4j:
    'Class to create deeplearning4j (0.3.3.3) training data for RTNT '

    def __init__(self, filename="data.txt", mode=0, predicate=True, arguments=True):
        self.instances = propbank.instances()
        self.raw_sentence = []
        self.predicates = []
        self.arguments_list = []
        self.new_sentence = []
        self.x = 0
        self.filename = filename
        self.mode = mode
        self.predicate = predicate
        self.arguments = arguments

    def findItem(self, activelist, item):
        return [(ind, activelist[ind].index(item)) for ind in xrange(len(activelist)) if item in activelist[ind]]

    def addPredicateLabel(self, raw_sentence, instance):
        if(len(self.findItem(raw_sentence,instance.predicate.select(instance.tree).leaves()[0]))):
            predicate_index = self.findItem(raw_sentence,instance.predicate.select(instance.tree).leaves()[0] )[0][0]
            raw_sentence[predicate_index] = ["<"+instance.roleset+">"+raw_sentence[predicate_index][0]+"</"+instance.roleset+">" ]

    def addArgumentLabel(self, raw_sentence, instance):
        raw_sentence_preflat = deepcopy(self.raw_sentence)
        for (argloc, argid) in instance.arguments:
            arguments_list =[]
            if (argloc.select(instance.tree).label() != "-NONE-"):
                arguments = argloc.select(instance.tree).leaves()
                for arg in arguments:
                    #print arg
                    if not '*' in arg:
                        arguments_list.append(arg)

            new_sentence = [item for sublist in raw_sentence_preflat for item in sublist]
            sequence_index = self.getIndexOfSequence(arguments_list,new_sentence)

            print sequence_index
            print len(self.raw_sentence)

            if len(sequence_index)>0:
                self.raw_sentence[sequence_index[0][0]].insert(0,"<"+argid+">")
                self.raw_sentence[sequence_index[0][1]-1].append("</"+argid+">")

    def getIndexOfSequence(self, sequence, activelist):
            return [(i, i+len(sequence)) for i in range(len(activelist)) if activelist[i:i+len(sequence)] == sequence]

    def saveAnnotatedSentence(self, sentence_list):
        #join sentence
        sentence = ' '.join([item for sublist in sentence_list for item in sublist])
        #save the sentence in the file
        with open(self.filename, "a") as text_file:
            text_file.write(sentence + "\n")

    def wordlistFromTree(self,instance):
        wordlist = []
        for s in instance.tree.subtrees(lambda t: t.height() == 2):
            if (s.label() != "-NONE-"):
                wordlist.append(s.leaves())
        return wordlist

    def run(self):
        print "mode"
        print self.mode

        for i in range(0, 9351):
            #print the instance number
            print i
            #next instance
            next_instance = self.instances[i+1]
            #current instance
            instance = self.instances[i]
            #Mode 0: This mode is default, it will be one predicate and argument structure per sentence.
            if(self.mode==0):
                if(self.x == 0):
                    self.raw_sentence = self.wordlistFromTree(instance)

                    if(self.arguments):
                        #add labels for argument spans
                        self.addArgumentLabel(self.raw_sentence,instance)

                    if(self.predicate):
                        #add the predicate/roleset label
                        self.addPredicateLabel(self.raw_sentence, instance)

                    self.saveAnnotatedSentence(self.raw_sentence)
                    self.x = 1

                print instance.sentnum
                print next_instance.sentnum

                if(instance.sentnum == next_instance.sentnum ):
                    self.x = 1
                else:
                    self.x = 0

            #Mode 1: Several predicate and argument structures in one sentence which migth overlap
            elif(self.mode==1):
                if self.x == 0:
                    self.raw_sentence = self.wordlistFromTree(instance)
                    self.x=1

                #save all predicates for one file and their position
                if(instance.sentnum==next_instance.sentnum):

                    if(self.arguments):
                        #add labels for argument spans
                        self.addArgumentLabel(self.raw_sentence,instance)

                    if(self.predicate):
                        #add the predicate/roleset label
                        self.addPredicateLabel(self.raw_sentence, instance)
                else:
                    if(self.arguments):
                        #add labels for argument spans
                        self.addArgumentLabel(self.raw_sentence,instance)
                    if(self.predicate):
                        #add the predicate/roleset label
                        self.addPredicateLabel(self.raw_sentence, instance)

                    self.saveAnnotatedSentence(self.raw_sentence)
                    #clear all variables
                    self.x = 0
                    self.raw_sentence = []

                    #set x to 0 if we have a new file
                    if(next_instance.fileid != instance.fileid):
                        self.x = 0
                        self.raw_sentence = []

            #All predicates arguments in a sentence, multiple identical sentences different annotations
            elif(self.mode == 2):
                self.raw_sentence = self.wordlistFromTree(instance)

                if(self.arguments):
                    #add labels for argument spans
                    self.addArgumentLabel(self.raw_sentence,instance)

                if(self.predicate):
                    #add the predicate/roleset label
                    self.addPredicateLabel(self.raw_sentence, instance)

                self.saveAnnotatedSentence(self.raw_sentence)

            else:
                print "mode does not exist"



if __name__ == "__main__":
    pb2d4j = probank2d4j(mode=0)

    pb2d4j.run()

