"""
Created on Wed May 15 13:35:19 2019

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
from coocurrenceNetwork import *
import subprocess as sp
import time


if __name__ == '__main__':

    '''
    Mission 1: Article Count by Month
    '''
    
    
#    for topic in topic_list:
#        path_count = len(path[topic])
#        for csv_path in range(path_count):
#            country = path[topic][csv_path].split('/')[6]
#            print('------ '+ topic + ' ' + country + ' ' + str(csv_path) + ' ------\n\n')
#            file_name = 'D:/GeneDrivePerception/result/Articlecount/' + country + '_' + topic + '_'+ str(csv_path) + '.png'
#            
#            ac = ArticlesCount(path[topic][csv_path])
#            ac_dict = ac.get_count()
#            try:
#                ac.drawgraph(ac_dict, lim_left = 0) # lim_left defines cut how many scales among 240, default=50
#                plt.savefig(file_name)
#            except:
#                pass
            
    '''
    Mission 2: Word Cloud
    '''
    
    stats = []
    for i in range(3,4):
        print('----------- '+str(i)+' -----------'+'\n')
        stats = (merge_result([stats,get_noun_stats(sample_text,70)]))
        
    res = list_to_dict(stats)
    wordcloud = WordCloud(background_color='black',colormap='viridis')
    wordcloud.generate_from_frequencies(frequencies = res)
    plt.figure(figsize = (15,7))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    
    
    '''
    Mission 3: Parse by dates
    '''
    
    ''' write result to csv '''
    for topic in ['Gene_drive']:
        for path in range(3,4):
#            country = txt_path[topic][path].split('/')[6]
#            print('------ '+ topic + ' ' + country + ' ' + str(path) + ' ------\n\n')
            file_name = sample_text
        
            # get stats
            file = ParsebyDate(file_name)
            stats = file.get_stats(scale = 'month')
            del file
            gc.collect()
            
            # store stats
#            with open(file_name, 'w') as f:
#                w = csv.writer(f)
#                w.writerows(stats.items())
    
    ''' read result from csv '''
    
#    data = pd.read_csv('D:/GeneDrivePerception/result/Parsebydate/SouthAfrica_Genetic_5.csv',
#                       header=None,error_bad_lines=False)
#    
#    data = data.set_index(0)
    
    
    ''' Mission 4: Get the number of the articles by countries('gene drive', worldwide)
    
        the summary of article count is saved in region_count
    '''
    
#    ac0 = ArticlesCount(path['Gene_drive'][3])
#    ac0_pub = ac0.data['PUBLICATION'].tolist()
#    publications = unique(ac0_pub)
#    
#    # write the publications to a csv
#    pub_country = dict()
#    for publication in publications:
#        if publication[0] != ' ':
#            pub_country[publication] = 'NG' # initialisation
#        else:
#            pub_country[publication[1:]] = 'NG'
# 
#    with open('D:/GeneDrivePerception/result/publications.csv', 'w',encoding='utf-8', newline = '') as f:
#        w = csv.writer(f)
#        w.writerows([[key,pub_country[key]] for key in pub_country.keys()])
#    
#    
#    # get the mapping from publications to regions
#    region_info = pd.read_csv('D:/GeneDrivePerception/result/publications.csv',encoding='ISO-8859-1',header=None)
#    for i in region_info.index:
#        pub = region_info.iloc[i][0]
#        reg = region_info.iloc[i][1]
#        pub_country[pub] = reg
#    
#    # count the articles by country    
#    all_publications = ac0_pub
#    region_count = dict()
#    unrecognized = []
#    
#    for pub in all_publications:
#        try:
#            country = pub_country[pub]
#        except:
#            unrecognized.append(pub)
#            continue
#        
#        try:
#            region_count[country] += 1
#        except:
#            region_count[country] = 1
            
#    region_count['United States'] += 5 # according to manually search of the unrecognized list 
#    unrecognized = []
#    
#    
#    # save result
#    plt.figure(figsize = (20,10))
#    region_count_li = sorted(region_count.items())
#    region_li, count_li = zip(*region_count_li)
#    plt.bar(region_li, count_li)
#    plt.xticks(rotation=80)
#    plt.xlabel('Countries/Regions')
#    plt.ylabel('Article count')
#    plt.savefig('D:/GeneDrivePerception/result/region_count.png')
#    
#    # NG labelled publications
#    print(region_info[region_info.iloc[:,1]=='NG'].iloc[:,0])
    
    
    ''' Mission 5: Content analysis of the whole world'''
    
    ''' read content
        run the chosen module in terms of Spacy/NLTK before running the following code in this Mission
    '''
    
    
#    stats = []
#    for i in range(3,8):
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
    
    ''' Analyse by dates '''
    
    # write result to csv
#    for topic in ['Gene_drive']:
#        path_count = len(txt_path[topic])
#        for path in range(3,8):
##            country = txt_path[topic][path].split('/')[6]
#            print('------ '+ topic + ' ' + 'worldwide' + ' ' + str(path) + ' ------\n\n')
#            file_name = 'D:/GeneDrivePerception/result/Parsebydate/' + 'worldwide' + '_' + topic + '_'+ str(path) + '_byMonth' + '.csv'
#        
#        
#            # get stats
#            file = ParsebyDate(txt_path[topic][path])
#            stats = file.get_stats(scale = 'month')
#            del file
#            gc.collect()
#            
#            # store stats
#            with open(file_name, 'w') as f:
#                w = csv.writer(f)
#                stats_items = stats.items()
#                try:
#                    w.writerows(stats_items)
#                except:
#                    print('\n there is a problem in this file')
#                    print(stats_items)
#                    pass
#    
##     read result from csv
#    
#    data = pd.read_csv('D:/GeneDrivePerception/result/Parsebydate/Worldwide_Gene_drive_9.csv',
#                       header=None,error_bad_lines=False)
#    
#    data = data.set_index(0)
    
    
    
    ''' Mission 6: Article count by month and region'''
    
    ''' get the dict '''
#    ac0 = ArticlesCount(path['Gene_drive'][3])
#    ac0_data = ac0.data
#    ac0_dict= ac0.get_count_by_country()
#    
#    ac1 = ArticlesCount(path['Gene_drive'][4])
#    ac1_data = ac1.data
#    ac1_dict= ac1.get_count_by_country()
#    
#    ac_mandr = dict()
#    for region in region_list:
#        region_name = region[0]
#        ac_mandr[region_name] = merge_dict([ac0_dict[region_name], ac1_dict[region_name]])
    
    
    ''' draw the graph '''
    # initialise data list
#    plot_stats_Aus = []
#    plot_stats_Asia = []
#    plot_stats_Africa = []
#    plot_stats_US = []
#    plot_stats_UK = []
#    plot_stats_GE = []
#    
#    
#    # get arguments
#    plot_stats_Aus,    xticks_Aus,    timeticks_Aus    = drawgraph_arg(ac_mandr['Australia'])
#    plot_stats_Asia,   xticks_Asia,   timeticks_Asia   = drawgraph_arg(ac_mandr['All_Asia'])
#    plot_stats_Africa, xticks_Africa, timeticks_Africa = drawgraph_arg(ac_mandr['All_Africa'])
#    plot_stats_US,     xticks_US,     timeticks_US     = drawgraph_arg(ac_mandr['United States'])
#    plot_stats_UK,     xticks_UK,     timeticks_UK     = drawgraph_arg(ac_mandr['United Kingdom'])
#    plot_stats_Ge,     xticks_Ge,     timeticks_Ge     = drawgraph_arg(ac_mandr['Germany'])
#    plot_stats_Other,  xticks_Other,  timeticks_Other  = drawgraph_arg(ac_mandr['Others'])
#    
#    
#    # plot
#    plt.figure(figsize=((12,5)))
#    
#    plt.plot(plot_stats_Aus, label = 'Australia')
#    plt.xticks(xticks_Aus, timeticks_Aus, rotation=80)
#    plt.plot(plot_stats_Asia, label = 'All Asia')
#    plt.xticks(xticks_Asia, timeticks_Asia, rotation=80)
#    plt.plot(plot_stats_Africa, label = 'All Africa')
#    plt.xticks(xticks_Africa, timeticks_Africa, rotation=80)
#    
#    plt.xlabel('Timeline')
#    plt.ylabel('Article count')
#    plt.legend()
#    
#    
#    plt.figure(figsize=((12,5)))
#    
#    plt.plot(plot_stats_US, label = 'United States')
#    plt.xticks(xticks_US, timeticks_US, rotation=80)
#    plt.plot(plot_stats_UK, label = 'United Kingdom')
#    plt.xticks(xticks_UK, timeticks_UK, rotation=80)
#    plt.plot(plot_stats_Ge, label = 'Germany')
#    plt.xticks(xticks_Ge, timeticks_Ge, rotation=80)
#    plt.plot(plot_stats_Other, label = 'Others')
#    plt.xticks(xticks_Other, timeticks_Other, rotation=80)
#    
#    plt.xlabel('Timeline')
#    plt.ylabel('Article count')
#    plt.legend()
    
    
    ''' Mission 7: entity network'''
    
    time0 = time.time()
    people_relation = []
    for i in range(3, 4): # range(3, 11)
        print('----------- ' + str(i) + ' -------------')
        scanner = Network_Article(sample_text, 'spacy')
        people_relation.append(scanner.relation)
        del scanner
        gc.collect()
        
    print('finish relationship')
    
    try:
        people_network = merge_dict(people_relation)
        print('finish people_network')
    except:
        print('merge error')
    time1 = time.time()
    
    
    
    test0 = choose_and_save(people_network, topentities, 1000, '../result/sample_top1000.csv')
    test1 = choose_and_save(people_network, topentities, 2000, '../result/sample_top2000.csv')
    print((time1-time0)/60/60)
    
    sp.call('cls', shell=True)
    del test0
    del test1
    del people_network
    gc.collect()
    
    
    
    ''' Mission 8: plot degree distribution '''
    degree_list = dict()
    wind_list = ['2','5','para','arti']
    for window in wind_list:
        
        path = 'D:/GeneDrivePerception/result/cooccurrence_network/datalibrary/dlnltk' + window + '.csv'
        with open(path, 'r') as f:
            data = f.readlines()
            degree = []
            for line in data:
                try:
                    degree.append(int(line.split(',')[3]))
                    degree_list[window] = degree
                except ValueError:
                    continue
                
    
    for window in wind_list:
        plt.figure(figsize=(10,7))
        plt.title('degree distribution  spacy window: ' + window,fontsize=12)
        plt.hist(degree_list[window],bins=20)
        plt.ylim(0,500)
        plt.xlabel('value')
        plt.ylabel('count')
        print(str(window)+' '+str(np.mean(degree_list[window])))
#        with open('D:/GeneDrivePerception/result/cooccurrence_network/','w'):
#            plt.savefig('dd_' + window + '.png')















