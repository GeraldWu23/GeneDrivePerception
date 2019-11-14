# -*- coding: utf-8 -*-
"""
Created on Fri May 17 10:56:49 2019

@author: wukak
"""

''' import packages '''
import sys
sys.path.append('D:\\GeneDrivePerception\\scripts')
from paths import *
import numpy as np
from data import *
from collections import Counter
import spacy
nlp = spacy.load('en')
nlp.max_length = 2000000 # could be dangerous, the original max_length is 1'000'000
import gc
from wordcloud import WordCloud
import matplotlib.pyplot as plt


''' class ReadContent 

        self.path = the path of the document
        self.nouns = the list of all the nouns recognised
        self.textdata = a string of the text
        self.parse(start=None, end=None): parse the string to nlped document and obtain stats of the nouns
        self.most_common(nums): choose a proper number and get the first 'nums' item in the frequency rank list of nouns

'''
class ReadContent:
    def __init__(self,path):
        self.path = path
        self.nouns = []
        with open(self.path,'r',encoding='utf-8') as file:
            self.textdata = file.read()
    
    def parse(self,start=None,end=None):
        # parse the document
        if (start is not None) and (end is not None):
            self.document = nlp(self.textdata[start:end])
        elif (start is not None):
            self.document = nlp(self.textdata[start:])
        else:
            self.document = nlp(self.textdata)
        
        # get stats
        self.nouns.extend([token.text for token in self.document 
                           if token.is_stop != True and token.is_punct != True and (token.pos_ == "NOUN" or token.pos_ == "PROPN")])
        self.noun_freq = Counter(self.nouns)
        
    def most_common(self,nums): # top 'nums' noun(s) in noun_freq
        try:
            return self.noun_freq.most_common(nums)
        except:
            print('NUMSERROR')
    
    
    
    
''' auxiliary functions '''

# merge two result list from ReadContent.most_common()
def merge_result(stats:list):
    if stats == []:
        print('Empty List')
        return 
    
    if type(stats[0]) is not list:
        return [term for term in stats if term[0] not in FORBIDDENWORDS]
    
    
    stats_dict = dict()
    stats_list = []
    
    # merge into one dictionary
    for lst in stats:
        for item in lst:    
            key = item[0]
            
            value = int(item[1])
            
            try:
                stats_dict[key] += value
            except:
                stats_dict[key] =  value
                
    # convert to list
    for key in stats_dict.keys():
        value = stats_dict[key]
        stats_list.append((key,value))
    
    
    return [term for term in stats_list if term[0] not in FORBIDDENWORDS]
    

# get noun stats through ReadContent
def get_noun_stats(path,nums):
    ob0 = ReadContent(path)
    
    size = len(ob0.textdata)
    if size <= 1800000:
        ob0.parse()
        ob0_res = ob0.most_common(nums)
        del ob0
        gc.collect()
        return [term for term in ob0_res if term[0] not in FORBIDDENWORDS]
    else:
        ob_num = 1 + int(size/1500000)
        result = []
        ob = []
        for i in range(ob_num):
            ob.append(ReadContent(path))
            #ob[i] = ReadContent(path)
            if i < ob_num-1:
                ob[i].parse(start = 1500000*i, end = 1500000*(i+1))
            else:
                ob[i].parse(start = 1500000*i)                
            
            res = ob[i].most_common(nums)
            result.append(res)
            ob[i] = 0
            gc.collect()
            
        return [term for term in merge_result(result) if term[0] not in FORBIDDENWORDS]
    

# convert the result from list to dict
def list_to_dict(lst:list):
    stats_dict = dict()
    for item in lst:    
        key = item[0]
        value = int(item[1])
        try:
            stats_dict[key] += value
        except:
            stats_dict[key] =  value
    
    return stats_dict


if __name__ == '__main__':
    pass
    
    
#    stats = []
#    for i in range(5,6):
#        print('----------- '+str(i)+' -----------'+'\n')
#        stats = (merge_result([stats,get_noun_stats(txt_path['Gene_drive'][i],50)]))
#        
#    res = list_to_dict(stats)
#    wordcloud = WordCloud(background_color='black',colormap='viridis')
#    wordcloud.generate_from_frequencies(frequencies = res)
#    plt.figure(figsize = (15,7))
#    plt.imshow(wordcloud, interpolation="bilinear")
#    plt.axis("off")
#    plt.show()

 
    
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        