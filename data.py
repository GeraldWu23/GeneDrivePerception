# -*- coding: utf-8 -*-
"""
Created on Wed May 15 18:49:33 2019

@author: wukak
"""

def timestamp_dict():
    timestamp = dict()
    for year in range(2000,2020):
        for month in range(1,13):
            key = str(year + float(month)/100)
            if len(key) < 7:
                key += '0'
            timestamp[key] = 0
    
    return timestamp
            
            
if __name__ == '__main__':
    print(timestamp_dict())