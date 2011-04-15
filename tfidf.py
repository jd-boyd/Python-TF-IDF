#!/usr/bin/env python
# encoding: utf-8

"""
File: tfidf.py
Author: Harry Schwartz
Date: Dec 2010

The simplest TF-IDF library imaginable.

Add your documents as two-element lists 
[docname, [list_of_words_in_the_document] ] with 
addDocument (docname, list_of_words).  Get a list of all the 
[docname, similarity_score] pairs relative to a document by 
calling similarities ( [list_of_words] ).

See README.txt for a usage example.
"""

import sys
import os
import collections

class tfidf:
    def __init__(self):
        self.weighted = False
        self.documents = []
        self.corpusDict = collections.defaultdict(int)
    
    def addDocument (self, docName, listOfWords):
        # building a dictionary
        docDict = collections.defaultdict(int)
        for w in listOfWords:
            docDict [w] += 1.0

        for w in docDict:
            self.corpusDict [w] += docDict[w]
                
        # normalizing the dictionary
        length = float (len (listOfWords))
        for k in docDict:
            docDict [k] /= length
        
        # add the normalized document to the corpus
        self.documents.append ( [docName, docDict] )
        
    def similarities (self, listOfWords):
        """Returns a list of all the [docname, similarity_score] pairs
        relative to a list of words."""
        
        # building the query dictionary
        queryDict = collections.defaultdict(int)
        for w in listOfWords:
            queryDict [w] += + 1.0
                
        # normalizing the query
        length = float (len (listOfWords))
        for k in queryDict:
            queryDict [k] /= length
        
        # computing the list of similarities
        sims = []
        for doc in self.documents:
            score = 0.0
            docDict = doc [1]
            for k in queryDict:
                if docDict.has_key (k):
                    score += (queryDict [k] / self.corpusDict [k]) + (docDict [k] / self.corpusDict [k])
            sims.append ([doc [0], score])
            
        return sims

if __name__=="__main__":
    import unittest
    class TestTFIDF(unittest.TestCase):
        def setUp(self):
            self.table = tfidf ()
        def test_add(self):
            self.table.addDocument ("foo", ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel"])
            self.table.addDocument ("bar", ["alpha", "bravo", "charlie", "india", "juliet", "kilo"])
            self.table.addDocument ("baz", ["kilo", "lima", "mike", "november"])

            sim_results=self.table.similarities (["alpha", "bravo", "charlie"])
            sim_expect=[['foo', 0.6875], ['bar', 0.75], ['baz', 0.0]]
            self.assertEqual(sim_results, sim_expect)

    unittest.main()
