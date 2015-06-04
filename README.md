#Propbank2d4j
This is a small script to create Deeplearning4j RTNT training data from Propbank NLTK data. 

To experiment with trying to do SRL using RTNT (Recursive Neural Tensor Network)

#Prerequisites
Need to install NLTK and after it's downloaded you also need to download the propbank corpus (terminal/cmdline):

python
> import nltk

> nltk.download()

Select the Propbank corpus.

#Training data formats
I've yet to try the training data, and since this data is for an experiment you will (soon) be able to choose from 
a range of different "mode":s which decides which format the data exports as. 0 is the default mode. 

Mode 0:
	This mode is default, it will be one predicate and argument structure per sentence.
Mode 1: 
	Several predicate and argument structures in one sentence which migth overlap
Mode 2. 
	All predicates arguments in a sentence, but if there are several per sentence they will not overlap but there will be
	one sentence per predicate/argument structure (several identical sentences, but different spans of arguments, different
	predicates)

