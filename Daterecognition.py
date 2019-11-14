# -*- coding: utf-8 -*-
"""
Created on Tue May 21 13:50:02 2019

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
from readcontent import *
import calendar





def date_recg(line:str):
    info = line.split()
    if len(info) is not 4:
        return False
    try:
        day = int(info[1][:-1])
        month = list(calendar.month_name).index(info[0])
        year = int(info[2])
        return [day,month,year]
    except:
        return False



''' class Parsebydate 

        self.datalines = lines of text file
        self.dateline  = [index, day, month, year]
        self.lines_to_str(): given a start line id and end line id, text between these two lines will be merged into one string
        self.date_start_labels(): return the ids of an article which is the first article of this year/month
        self.get_stats(): obtain the stats of the whole file
        
        self.Timeperiod:
            each part of the text of a time period will be parsed in a Timeperiod object
            
            self.document = the nlped text
            self.nouns = return the list of nouns of this file
            self.noun_freq = a stats of the nouns
            self.most_common(): return a rank of top n frequent nouns 
'''


class ParsebyDate:
    def __init__(self, path):
        with open(path,'r',encoding='utf-8') as file:
            self.datalines = file.readlines()
            self.dateline = []
            for line_id in range(len(self.datalines)):
                date_info = date_recg(self.datalines[line_id])
                if date_info:
                    infoline = [line_id]
                    infoline.extend(date_info)
                    self.dateline.append(infoline)
        
    
    class Timeperiod:
        def __init__(self, text:str):
            self.document = nlp(text)
            self.nouns = [token.text for token in self.document if token.is_stop != True and token.is_punct != True 
                          and (token.pos_ == "NOUN" or token.pos_ == "PROPN")
                          and token.text not in FORBIDDENWORDS]
            self.noun_freq = Counter(self.nouns)
        
        def most_common(self,nums): # top 'nums' noun(s) in noun_freq
            try:
                return self.noun_freq.most_common(nums)
            except:
                print('NUMSERROR')
    
    
    def lines_to_str(self, start_id, end_id):
        if start_id >= end_id:
            return False
        
        return ' '.join(self.datalines[start_id:end_id])
    
    def date_start_label(self,scale = 'year'):
        labels = [0]
        month = 13
        year = 0
        if scale == 'year':
            for line in self.dateline:
                if line[3] != year: # if in different year
                    year = line[3]
                    if line[0] != 0 or line[0] != len(self.datalines):
                        labels.append(line[0]) # add the line number to labels
        elif scale == 'month':
            for line in self.dateline:
                if line[2] != month or line[3] != year: # if in different year or different month
                    year = line[3]
                    month = line[2]
                    if line[0] != 0 or line[0] != len(self.datalines):
                        labels.append(line[0]) # add the line number to labels
        else:
            print('wrong scale')
            return False
        
        labels.append(len(self.datalines))
        return labels
    
    def get_stats(self, top_nums=20, scale = 'year'):
        stats = dict()
        labels = self.date_start_label(scale=scale)
#        print(labels)
        
        # i for time label
        for i in range(len(labels) - 2):
            text_string = self.lines_to_str(labels[i], labels[i+1])
            try:
                part = self.Timeperiod(text_string)
                result = part.most_common(nums = top_nums)
                del part
                gc.collect()
            except:
                size = len(text_string)
                ob_num = 1 + int(size/1500000)
                result = []
                ob = []
                
                # j for a part of the text string
                for j in range(ob_num):
                    
                    if j < ob_num-1:
                        part = self.Timeperiod(text_string[1500000*j:1500000*(j+1)])
                        ob.append(part)
                        part_stats = part.most_common(nums = top_nums)
                        ob[j] = 0
                        gc.collect()
                        result.append(part_stats)
                    else:
                        part = self.Timeperiod(text_string[1500000*j:])
                        ob.append(part)
                        part_stats = part.most_common(nums = top_nums)
                        ob[j] = 0
                        gc.collect()    
                        result.append(part_stats)
                    
                
            if scale == 'year':
                timestamp = str(self.datalines[labels[i+1]].split()[2])
            elif scale == 'month':
                timestamp = str(self.datalines[labels[i+1]].split()[0]) + ' ' + str(self.datalines[labels[i+1]].split()[2])
            else:
                print('wrong scale')
                return False
            
            print(timestamp)
            try:
                stats[timestamp] = merge_result(result)
            except:
                print(result)
            
        return stats
        
    
    
if __name__ == '__main__':
    # write result to csv
    pass
    
    
    
    
    
    
    
    
    
    
    
    