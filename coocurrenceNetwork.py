# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 14:45:35 2019

@author: wukak
"""

import sys
sys.path.append('D:\\GeneDrivePerception\\scripts')
from paths import *
import numpy as np
from data import *
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import gc
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from readcontent import *
import requests
import json
import time
import networkx as nx
from networkx.readwrite import json_graph
import csv
import re
import spacy
from numpy.random import choice
from fuzzywuzzy.process import dedupe as fuzzy_dedupe
from fuzzywuzzy.process import extract as fuzzy_extract
import subprocess as sp
import pandas as pd
nlp = spacy.load('en')
nlp.max_length = 2000000 # could be dangerous, the original max_length is 1'000'000




''' Entity Extraction '''

class entityScanner:
    ''' 
    extract entities from text
    
    self.tool = nltk or spacy
    
    '''
    def __init__(self, text, tool = 'NLTK'):
        self.text = text
        self.tool = tool

    def extract_entities(self):
        self.entities = []

        # get stats    
        if self.tool in ['NLTK', 'nltk']:
#            print('parser is '+'NLTK')
            
            self.text_tokenised = word_tokenize(self.text)
            pos = nltk.pos_tag(self.text_tokenised)
            classifier = nltk.ne_chunk(pos, binary = False)
            person = []
            name = ""
            for subtree in classifier.subtrees(filter = lambda t:t.label() in ["PERSON","GPE","ORGANIZATION"]): # choose label here, no lOCATION
                for leaf in subtree.leaves():
                    person.append(leaf[0])
                if len(person) > 1: # avoid grabbing lone surnames
                    for part in person:
                        name += part + ' '
                    if name[:-1] not in self.entities:
                        self.entities.append(cleanup(name[:-1]))
                    name = ""
                person = []
                
        elif self.tool in ['Spacy', 'spacy', 'SPACY']:
#            print('parser is '+'Spacy')
            
            self.text_tokenised = nlp(self.text)
            self.entities.extend([cleanup(token.text) for token in self.text_tokenised.ents 
                           if (token.label_ in ["PERSON","GPE","ORG"] and len(token.text.split())>1)]) # no LOC
        
        else:
            print('UNKNOWN TOOL')
            return False
    
        return self.entities
    

def cleanup(string):
    ''' clean a entity string '''
    
    FORBIDDEN = ["\n", "-", "\/", '"', "et al", "\\", "=", "*", "%", "?", "!", "~", "{", "}", "[", "]", "+", ";", ":", "_"]
    ''' cleanup the entity '''
    for forc in FORBIDDEN:
        string = string.replace(forc, '')  # remove forbidden characters
    
    string = re.sub('\d', '', string).rstrip("'s").strip(' ').strip(',').strip('.')  # remove digits, last 's, and side whitespace  
    string = ' '.join(string.split())  # remove multiple string
    
#    print(string)
    return string
    

''' Co-occurrence Network(by article) 

        path = the path of the target file
        tool = 'NLTK' or 'Spacy'

        self.text = whole text by line
        self.boundaries = boundaries between an article and another
        
        self.entities(start_line, end_line):
            get the entity list from a line to another line of the text
            
        self.add_relation(entity_list):
            modify relation dict(co-occurence network)
        
'''
class Network_Article:
    def __init__(self, path, tool):
        with open(path, 'r', encoding = 'utf-8') as file:
            self.text = file.readlines()
        
        self.tool = tool
        self.boundaries = [0]
        self.relation = dict()  # with duplication
        
        
        # get boundaries
        text_size = len(self.text)
        for line_no in range(text_size):
            if self.text[line_no][:17] == 'LANGUAGE: ENGLISH': # mark of boundary
                self.boundaries.append(line_no)
                
        # get relations
        for line_no in range(len(self.boundaries) - 1):
            entities_arti = self.entities(self.boundaries[line_no], self.boundaries[line_no + 1], tool=self.tool)
            self.add_relation(entities_arti)
            
                
    
    def entities(self, start_line, end_line, tool): 
        article = ''.join(self.text[start_line:end_line])
#        print(article)
        scanner = entityScanner(article, tool = tool)
        entity_list = scanner.extract_entities()
        del scanner
        gc.collect()
        
        return entity_list
        
        
    def add_relation(self, entity_list):
        for entity in entity_list:
            others = [ent for ent in entity_list if ent is not entity]
            
            try:

                self.relation[entity].extend(others)
                
            except:
                self.relation[entity] = others
            
        return self.relation
    
    
    def dedupe(self, relation):
        # relation is a dictionary
        if type(relation) != dict:
            raise TypeError
        
        keep_list = fuzzy_dedupe(relation.keys())
        keep_list = [ent.rstrip('!:!?').rstrip('\n') for ent in keep_list]
        relation_dedupe = dict()
        
        for key in relation.keys():
            try:
                relation_dedupe[fuzzy_extract(key, keep_list)[0][0]].extend([fuzzy_extract(value, keep_list)[0][0] for value in relation[key]]) # choose the best match in keep_list
            except:
                relation_dedupe[fuzzy_extract(key, keep_list)[0][0]] = [fuzzy_extract(value, keep_list)[0][0] for value in relation[key]] # choose the best match in keep_list
            print(key + '----->' + fuzzy_extract(key, keep_list)[0][0]) # choose the best match 
        return relation_dedupe
    
    

''' Co-occurrence Network_Sentence(by sentence) 
        

        self.window = number # it should be at least 1 and no more than size(sometimes it gets error with big size because of the limitation of the sparse tool)
        self.text = whole text by line
        self.boundaries = boundaries between an article and another
        
        self.entities(start_line, end_line):
            get the entity list from a line to another bound of the text
            
        self.add_relation(entity_list):
            modify relation dict(co-occurence network)
        
'''
class Network_Sentence:
    def __init__(self, path, number = 1, tool='NLTK'):
        with open(path, 'r', encoding = 'utf-8') as file:
            self.text = file.read()
            self.text = re.split("[.|?|!]", self.text)  # a list of sentences
        
        self.tool = tool
        self.window = number # number of sentence sparsed
        self.boundaries = [i for i in range(len(self.text) - self.window)]  # sliding window
        self.relation = dict()  # with duplication
        
        
#        # not sliding window
#        # get boundaries
#        text_size = len(self.text)
#        bound = 1 # next bound
#        while(bound < text_size-1):
#            self.boundaries.append(bound)
#            bound += self.window
            
            
        # get relations
        for bound_no in range(len(self.boundaries) - 1):
#            print(self.boundaries[bound_no],)
            entities_arti = self.entities(self.boundaries[bound_no], self.boundaries[bound_no] + self.window, tool = self.tool) # extract entities in string
            self.add_relation(entities_arti) # add relationship to relationship dict
        
#        print(len(self.text))
                
    
    def entities(self, start_bound, end_bound, tool): 
        string = ''.join(self.text[start_bound:end_bound])
        string.lstrip('\n').rstrip('\n')
        scanner = entityScanner(string, tool=tool)
        entity_list = scanner.extract_entities()
        del scanner
        gc.collect()
        
        return entity_list
        
        
    def add_relation(self, entity_list):
        #if no relationship
        if len(entity_list) <= 1:
            return self.relation
        
        # if there is more than one entities
        for entity in entity_list:
            others = [ent for ent in entity_list if ent is not entity]
            
            try:
                self.relation[entity].extend(others)
                
            except:
                self.relation[entity] = others
            
        return self.relation
    
    
    def dedupe(self, relation):
        # relation is a dictionary
        if type(relation) != dict:
            raise TypeError
        
        keep_list = fuzzy_dedupe(relation.keys())
        keep_list = [ent.rstrip("!:!?'").replace('\n','') for ent in keep_list]
        relation_dedupe = dict()
        
        for key in relation.keys():
            try:
                relation_dedupe[fuzzy_extract(key, keep_list)[0][0]].extend([fuzzy_extract(value, keep_list)[0][0] for value in relation[key]]) # choose the best match in keep_list
            except:
                relation_dedupe[fuzzy_extract(key, keep_list)[0][0]] = [fuzzy_extract(value, keep_list)[0][0] for value in relation[key]] # choose the best match in keep_list
            print(key + '----->' + fuzzy_extract(key, keep_list)[0][0]) # choose the best match 
        return relation_dedupe



''' Co-occurrence Network_Sentence(by sentence) 
        

        self.window = number # it should be at least 1 and no more than size(sometimes it gets error with big size because of the limitation of the sparse tool)
        self.text = whole text by line
        self.boundaries = boundaries between an article and another
        
        self.entities(start_line, end_line):
            get the entity list from a line to another bound of the text
            
        self.add_relation(entity_list):
            modify relation dict(co-occurence network)
        
'''

class Network_Paragraph:
    def __init__(self, path, tool='NLTK'):
        with open(path, 'r', encoding = 'utf-8') as file:
            self.text = file.read()
            self.text = re.split("\n", self.text)  # a list of paragraphs
        
        self.tool = tool
        self.boundaries = [0]  # bound between a paragraph to another
        self.relation = dict()  # with duplication
        
        
        # get boundaries
        for i in range(len(self.text)):
            # if the last character is delimiter or the paragraph ends with " or '
            try:
                if self.text[i][-1] in ['.','!','?'] or (self.text[i][-1] in ['"',"'"] and self.text[i][-2] in ['.','!','?']):
                    self.boundaries.append(i+1) # the bound index is (1 + target line's index)
            except:
                # the length of this line is less than 2, like an empty line
                continue
            
            
        # get relations
        for bound_no in range(len(self.boundaries) - 1):
            entities_arti = self.entities(self.boundaries[bound_no], self.boundaries[bound_no + 1], tool = self.tool) # extract entities in string
            self.add_relation(entities_arti) # add relationship to relationship dict
        

                
    def entities(self, start_bound, end_bound, tool): 
        string = ''.join(self.text[start_bound:end_bound])
        scanner = entityScanner(string, tool=tool)
        entity_list = scanner.extract_entities()
        del scanner
        gc.collect()
        
        return entity_list
        
        
    def add_relation(self, entity_list):
        #if no relationship
        if len(entity_list) <= 1:
            return self.relation
        
        # if there is more than one entities
        for entity in entity_list:
            others = [ent for ent in entity_list if ent is not entity]
            
            try:
                self.relation[entity].extend(others)
                
            except:
                self.relation[entity] = others
            
        return self.relation
    
    
    def dedupe(self, relation):
        # relation is a dictionary
        if type(relation) != dict:
            raise TypeError
        
        keep_list = fuzzy_dedupe(relation.keys())
        keep_list = [ent.rstrip("!:!?'").replace('\n','') for ent in keep_list]
        relation_dedupe = dict()
        
        for key in relation.keys():
            try:
                relation_dedupe[fuzzy_extract(key, keep_list)[0][0]].extend([fuzzy_extract(value, keep_list)[0][0] for value in relation[key]]) # choose the best match in keep_list
            except:
                relation_dedupe[fuzzy_extract(key, keep_list)[0][0]] = [fuzzy_extract(value, keep_list)[0][0] for value in relation[key]] # choose the best match in keep_list
            print(key + '----->' + fuzzy_extract(key, keep_list)[0][0]) # choose the best match 
        return relation_dedupe



''' entities cut off 
    
    choosing top n entities from dict and return cut dict

    num = number of entities from the top are reserved # first appearing entities will be chosen if a few of them have the same connections
'''

def topentities(entity_dict, number):
    if len(entity_dict.keys()) <= number:
        print('TOO MANY RESERVED ENTITIES, RESERVE AS WE CAN')
        number = len(entity_dict.keys())
    
    top_list = sorted(entity_dict.copy(), key = lambda x:len(entity_dict[x]), reverse=True)[:number] # list of chosen entities
    top_dict = {} # new dict
    
    for key in top_list:
        top_dict[key] = [entity for entity in entity_dict[key] if entity in top_list]
        
        # if top entity has no top entity connection
        if not top_dict[key]: 
            del top_dict[key]
            
    return top_dict
    

def randomentities(entity_dict, percentage):
    if percentage >= 1 or percentage <= 0:
        print('BAD PERCENTAGE')
        return False
    
    number = int(percentage * len(entity_dict.keys()))
    key_pool = entity_dict.keys().copy()
    chosen_list = []
    
    for _ in range(number):
        chosen_list.append(key_pool.pop(choice(key_pool)))
    
    return chosen_list



def choose_and_save(network, chop_function, chop_function_para, filepath):
    ''' 
    choose a way to sample data and save as csv
    
    network = people relationship, dict
    chop_function = topentities() / randomentities()
    chop_function_para = paramatre of the chosen function
    filepath = save path
    
    '''
    
    network_chopped = chop_function(network, chop_function_para)
    
    list_result = []
    for key in network_chopped:
        for value in network_chopped[key]:
            list_result.append([key, value])
    
    print('changed to list')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerows(list_result)
    
    print('finish writing')
    
    sp.call('cls', shell=True)
    
    return network_chopped


def csvToDict(path):
    df = pd.read_csv(path)
    network = dict()
    for i in df.index:
        key = df.iloc[i][0]
        value = df.iloc[i][1]
        
        try:
            network[key].append(value)
        except KeyError:
            network[key] = [value]
    
    return network
    






    
if __name__ == '__main__':
    pass
#    a = Network_Paragraph(sample_text)
#    text = a.text
    


    
    
    
    
            
            
            
            