# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 14:17:39 2019

@author: wukak
"""

''' import packages '''
import sys
sys.path.append('D:\\GeneDrivePerception\\scripts')
import calendar
import pandas as pd
from paths import *
import matplotlib.pyplot as plt
import numpy as np
from ArticleCount import *
from data import *
import spacy
from wordcloud import WordCloud
from readcontent import *
from Daterecognition import *
import csv
#from coocurrenceNetwork import *
import subprocess as sp
import time


class countArticle_fromtxt:
    def __init__(self, path):
        with open(path, 'r', encoding = 'utf-8') as f:
            self.data = f.readlines()
        
        # save bounds
        self.bound = [0]
        for line in range(len(self.data)):
            if self.data[line] == 'LANGUAGE: ENGLISH\n':
                self.bound.append(line)
        
        # count article and clean noise article(with no 'gene drive' or 'gene drives')
        self.count = 0        
        for b in range(len(self.bound) - 1):
            # for each article
            article = ' '.join(self.data[self.bound[b]:self.bound[b+1]]).split(' ')
            gene_drive_ind = False
            for word in range(len(article) - 1):
                if article[word].strip('\n').lstrip(',').lstrip('"').lstrip("'").lstrip('.') == 'gene':
#                    print(article[word])
                    if article[word+1].strip('\n').rstrip(',').rstrip('"').rstrip("'").rstrip('.') in ['drive', 'drives']:
#                        print(article[word+1])
                        self.count += 1
                        gene_drive_ind = True
                        break
                
            if gene_drive_ind == True:
                #print(b,b)
                pass
            else:
                #print(b)
                for i in range(self.bound[b], self.bound[b+1]):
                    self.data[i] = ''
        
        # write to an article
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(self.data)

            
            
if __name__ == '__main__':
    pass
    c = 0
    for i in range(3,8):
        test = countArticle_fromtxt(txt_path['Gene_drive'][i])
        c += test.count
        a = test.data
    print(c)
    
        
        
        
        
        
        
        
