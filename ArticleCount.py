# -*- coding: utf-8 -*-
"""
Created on Wed May 15 13:35:19 2019

@author: wukak
"""

''' import packages '''
import sys
sys.path.append('D:\\GeneDrivePerception\\Project\\scripts')
import calendar
import pandas as pd
from paths import *
import matplotlib.pyplot as plt
import numpy as np
from data import *



'''
class ArticlesCount

    the input is one of the paths

    self.getcount(): return a dictionary with count of articles of each month.
    self.drawgraph(): draw the graph of the count of a period

'''

class ArticlesCount:
    def __init__(self,path):
        self.path = path
        self.data = (pd.read_csv(path,header=0,error_bad_lines=False).iloc[:,[0,1,3,4,5]]).dropna(subset=['DATE'])
        self.size = len(self.data)
        self.data.index = [str(i) for i in self.data.index]
        
        
        
        reserve_year = None
        for row in range(self.size):
            try: # some dates are not in English
            # standardise DATE column to year-month format e.g. 201910
                date_lst = self.data.loc[str(row)]['DATE'].split(' ')[:-1]
                
                month_id = list(calendar.month_name).index(date_lst[0])
    
                try:
                    year = int(date_lst[2])
                    
                    reserve_year = year # reserve year info for invalid data
                except:
                    year = reserve_year or 0000 # put the previous year as the year of the invalid timestamp
    
                if month_id < 10:
                    self.data.loc[str(row),'DATE'] = int(str(year) + '0' + str(month_id))
                else:
                    self.data.loc[str(row),'DATE'] = int(str(year)       + str(month_id))
            
            except:
                pass
         
        # get rid of duplication in terms of HEADLINE
#        print(self.data.shape)
#        self.data = self.data.groupby('HEADLINE',as_index = False)[['DATE','PUBLICATION']].min()
#        print(self.data.shape)
        
        self.data = self.data[['DATE','PUBLICATION']] # didnt solve the problem of groupby, for path['Gene_drive'][4],after groupby only Publication is shown
        self.data.index = [str(i) for i in self.data.index]
        self.size = len(self.data)
      
        
    def get_count(self):
        # format the number to year.month for showing in the graph
        self.articles_count = dict()
        for row in range(self.size):
            try:
                date = str(self.data.loc[str(row),'DATE'] / 100) # format = year.month
            except:          
                continue
            
            if len(date)<7:
                date += '0'
            
            try:
                self.articles_count[date] += 1
            except:
                self.articles_count[date] = 1
        
        return self.articles_count
    
    
    
    def get_count_by_country(self):
            # format the number to year.month for showing in the graph
            self.articles_date_country = dict() # initialise dictionary count by date and region
            for region in region_list:
                self.articles_date_country[region[0]] = dict()  # get the first item of region as the name of this region
                
            for row in range(self.size):
                
                # get date
                try:
                    date = str(self.data.loc[str(row),'DATE'] / 100) # format = year.month
                    if len(date)<7:
                        date += '0'
                except:  
                    continue             
                
            
            
                # get region
                try:
                    publication = self.data.loc[str(row),'PUBLICATION']
                    country = pub_country[publication]
                    region_name  = country_region[country]
                except:           
                    print('region name get error')
                    print(publication,date)
                    region_name = 'Others'
                
                
                try:
                    self.articles_date_country[region_name][date] += 1
                except:
                    self.articles_date_country[region_name][date] = 1
            
            return self.articles_date_country
        
        
    
    def drawgraph(self,dic,lim_left=50):
        stats = timestamp_dict()
        plot_stats = []
        
        for key in dic.keys():
            try:
                stats[key] += dic[key]
            except:
                pass
            
        keys = np.array([i for i in stats.keys()])
        
        for key in keys:
            plot_stats.append(stats[key])
        
    
        plt.figure(figsize=((12,5)))
        xticks = [i for i in range(0,240,6)] 
        plt.plot(plot_stats)
        plt.xticks(xticks,keys[xticks],rotation=80)
        plt.xlim(left=lim_left)
        plt.xlabel('Timeline')
        plt.ylabel('Article count')
    

'''

auxiliary function


    merge_dict(dict_list):
        input a list of dict, merge the result of these two dicts
        
    unique():
        get rid of duplicates of an input list

'''

def drawgraph_arg(dic):
    stats = timestamp_dict()
    plot_stats = []
    
    for key in dic.keys():
        try:
            stats[key] += dic[key]
        except:
            pass
        
    keys = np.array([i for i in stats.keys()])
    
    for key in keys:
        plot_stats.append(stats[key])
    

#    plt.figure(figsize=((12,5)))
#    xticks = [i for i in range(0,240,6)] 
#    plt.plot(plot_stats)
#    plt.xticks(xticks,keys[xticks],rotation=80)
#    plt.xlim(left=lim_left)
#    plt.xlabel('Timeline')
#    plt.ylabel('Article count')
    xticks = [i for i in range(0,240,6)]
    timeticks = keys[xticks]
    return plot_stats, xticks, timeticks
    
    
    

def merge_dict(dict_lst): # return dict
    stats = dict()
    for dictionary in dict_lst:
        keys = [i for i in dictionary.keys()]
        for key in keys:
            try:
                stats[key] += dictionary[key]
            except:
                stats[key]  = dictionary[key]
    return stats
        

def unique(lst):
    return list(set(lst))



''' Mapping from publication to region '''


pub_country = dict()
country_region = dict()
region_info = pd.read_csv('D:/GeneDrivePerception/result/publications.csv',encoding='ISO-8859-1',header=None)
for i in region_info.index:
    pub = region_info.iloc[i][0]
    country = region_info.iloc[i][1]
    pub_country[pub] = country
    for region in [Australia,UnitedStates,UnitedKingdom,Germany,AllAfrica,AllAsia]:
        if country in region:
            country_region[country] = region[0]
            break
        country_region[country] = 'Others'



if __name__ == '__main__':
    pass

#    ac0 = ArticlesCount(path['Gene_drive'][3])
#    ac0_data = ac0.data
#    ac0_dict= ac0.get_count()
#    
#    ac1 = ArticlesCount(path['Gene_drive'][4])
#    ac1_data = ac1.data
#    ac1_dict= ac1.get_count()
#    
#    ac0.drawgraph(merge_dict([ac0_dict, ac1_dict]), lim_left=0)





