# -*- coding: utf-8 -*-
"""
Created on Wed May 15 14:04:31 2019

@author: wukak
"""

''' FORBIDDENLIST '''
FORBIDDENWORDS = ['DOCUMENTS','Copyright','SECTION','TYPE','DATE','CODE','JOURNAL','LANGUAGE','LENGTH','LOAD','PUBLICATION','ENGLISH']


''' country list '''
country_list = ['Uganda','Nigeria','SouthAfrica']

Australia = ['Australia']
UnitedStates = ['United States']
UnitedKingdom = ['United Kingdom']
Germany = ['Germany']
AllAfrica = ['All_Africa','Republic of the Congo','Egypt','South Africa','Nigeria','kenya','Tanzania','Uganda','Kenya','','','']
AllAsia = ['All_Asia','Pakistan','South Korea','India','Saudi Arabia','Saudi','South Korea','Israel','Bangladesh','Singapore','United Arab Emirates','China','Sri Lanka','Iran','Qatar','Malaysia','Philippines','Japan','Oman','Thailand','Lebanon','Jordan','','','','']                                                                   
Others = ['Others']
region_list = [Australia, UnitedStates, UnitedKingdom, Germany, AllAfrica, AllAsia, Others]

''' topic list '''
topic_list = ['Genetic','Target_Malaria','Gene_drive','Gate_foundation','ETC_group']


''' csv paths '''

path = dict()
path['Genetic'] = ['D:/GeneDrivePerception/resource/Uganda/Genetic/The_Daily_Monitor_Daily_Monitor_East_African2019-05-15_11-26.CSV',
                   'D:/GeneDrivePerception/resource/Nigeria/Genetic/News_Chronicle_(Nigeria)_The_Nigerian_Observ2019-05-14_17-10.CSV',
                   'D:/GeneDrivePerception/resource/Nigeria/Genetic/News_Chronicle_(Nigeria)_The_Nigerian_Observ2019-05-14_17-13.CSV',
                   'D:/GeneDrivePerception/resource/SouthAfrica/Genetic/All_South_African_Newspapers2019-05-15_11-41.CSV',
                   'D:/GeneDrivePerception/resource/SouthAfrica/Genetic/All_South_African_Newspapers2019-05-15_11-42.CSV',
                   'D:/GeneDrivePerception/resource/SouthAfrica/Genetic/All_South_African_Newspapers2019-05-15_11-59.CSV']

path['Target_Malaria'] = ['D:/GeneDrivePerception//resource/Nigeria/TargetMalaria/News_Chronicle_(Nigeria)_The_Nigerian_Observ2019-05-14_17-14.CSV',
                          'D:/GeneDrivePerception//resource/SouthAfrica/TargetMalaria/All_South_African_Newspapers2019-05-15_12-03.CSV']
                  
path['Gene_drive'] = ['D:/GeneDrivePerception/resource/Uganda/GeneDrive/Advancing_from_genetic_modification_to_synth.CSV',
                      'D:/GeneDrivePerception/resource/Nigeria/GeneDrive/News_Chronicle_(Nigeria)_The_Nigerian_Observ2019-05-14_17-25.CSV',
                      'D:/GeneDrivePerception/resource/SouthAfrica/GeneDrive/All_South_African_Newspapers2019-05-15_12-04.CSV',
                      'D:/GeneDrivePerception/resource/Worldwide/All_English_Language_News2019-08-16_14-21.CSV']

path['Gate_foundation'] = ['D:/GeneDrivePerception/resource/Uganda/GateFoundation/The_Daily_Monitor_Daily_Monitor_East_African2019-05-15_11-35.CSV',
                           'D:/GeneDrivePerception/resource/Nigeria/GateFoundation/Business_Day_Business_Day_(Nigeria)__Busines2019-05-15_16-09.CSV',
                           'D:/GeneDrivePerception/resource/SouthAfrica/GateFoundation/All_South_African_Newspapers2019-05-15_12-09.CSV']

path['ETC_group'] = ['D:/GeneDrivePerception/resource/Nigeria/ETCgroup/News_Chronicle_(Nigeria)_The_Nigerian_Observ2019-05-14_17-27.CSV',
                     'D:/GeneDrivePerception/resource/SouthAfrica/ETCgroup/All_South_African_Newspapers2019-05-15_12-17.CSV']



''' txt paths by countries and topics'''

txt_path = dict()
txt_path['Genetic'] = ['D:/GeneDrivePerception/resource/Uganda/Genetic/The_Daily_Monitor_Daily_Monitor_East_African2019-05-14_16-45.TXT',
                       'D:/GeneDrivePerception/resource/Nigeria/Genetic/News_Chronicle_(Nigeria)_The_Nigerian_Observ2019-05-14_17-04.TXT',
                       'D:/GeneDrivePerception/resource/Nigeria/Genetic/News_Chronicle_(Nigeria)_The_Nigerian_Observ2019-05-14_17-08.TXT',
                       'D:/GeneDrivePerception/resource/SouthAfrica/Genetic/All_South_African_Newspapers2019-05-15_11-40.TXT',
                       'D:/GeneDrivePerception/resource/SouthAfrica/Genetic/All_South_African_Newspapers2019-05-15_11-47.TXT',
                       'D:/GeneDrivePerception/resource/SouthAfrica/Genetic/All_South_African_Newspapers2019-05-15_11-48.TXT',
                       'D:/GeneDrivePerception/resource/SouthAfrica/Genetic/All_South_African_Newspapers2019-05-15_11-51.TXT',
                       'D:/GeneDrivePerception/resource/SouthAfrica/Genetic/All_South_African_Newspapers2019-05-15_11-52.TXT',
                       'D:/GeneDrivePerception/resource/SouthAfrica/Genetic/All_South_African_Newspapers2019-05-15_11-54.TXT',
                       'D:/GeneDrivePerception/resource/SouthAfrica/Genetic/All_South_African_Newspapers2019-05-15_11-59.TXT'
                        ]

txt_path['Target_Malaria'] = ['D:/GeneDrivePerception/resource/Nigeria/TargetMalaria/News_Chronicle_(Nigeria)_The_Nigerian_Observ2019-05-14_17-14.TXT',
                              'D:/GeneDrivePerception/resource/SouthAfrica/TargetMalaria/All_South_African_Newspapers2019-05-15_12-03.TXT']
                  
txt_path['Gene_drive'] = ['D:/GeneDrivePerception/resource/Uganda/GeneDrive/Advancing_from_genetic_modification_to_synth.TXT',
                          'D:/GeneDrivePerception/resource/Nigeria/GeneDrive/News_Chronicle_(Nigeria)_The_Nigerian_Observ2019-05-14_17-26.TXT',
                          'D:/GeneDrivePerception/resource/SouthAfrica/GeneDrive/All_South_African_Newspapers2019-05-15_12-04.TXT',
                          'D:/GeneDrivePerception/resource/Worldwide/English/genedrive1-500.TXT',
                          'D:/GeneDrivePerception/resource/Worldwide/English/genedrive501-1000.TXT',
                          'D:/GeneDrivePerception/resource/Worldwide/English/genedrive1001-1500.TXT',
                          'D:/GeneDrivePerception/resource/Worldwide/English/genedrive1501-2000.TXT',
                          'D:/GeneDrivePerception/resource/Worldwide/English/genedrive2001-2124.TXT',
                          'D:/GeneDrivePerception/resource/Worldwide/English/genedriveonly0.TXT',
                          'D:/GeneDrivePerception/resource/Worldwide/English/genedriveonly1.TXT',
                          'D:/GeneDrivePerception/resource/Worldwide/English/genedriveonly2.TXT',
                          'D:/GeneDrivePerception/resource/Worldwide/English/genedriveonly3.TXT']
                          

txt_path['Gate_foundation'] = ['D:/GeneDrivePerception/resource/Uganda/GateFoundation/The_Daily_Monitor_Daily_Monitor_East_African2019-05-14_16-50.TXT',
                               'D:/GeneDrivePerception/resource/Nigeria/GateFoundation/News_Chronicle_(Nigeria)_The_Nigerian_Observ2019-05-14_17-15.TXT',
                               'D:/GeneDrivePerception/resource/Nigeria/GateFoundation/News_Chronicle_(Nigeria)_The_Nigerian_Observ2019-05-14_17-18.TXT',
                               'D:/GeneDrivePerception/resource/Nigeria/GateFoundation/News_Chronicle_(Nigeria)_The_Nigerian_Observ2019-05-14_17-20.TXT',
                               'D:/GeneDrivePerception/resource/SouthAfrica/GateFoundation/All_South_African_Newspapers2019-05-15_12-06.TXT',
                               'D:/GeneDrivePerception/resource/SouthAfrica/GateFoundation/All_South_African_Newspapers2019-05-15_12-07.TXT',
                               'D:/GeneDrivePerception/resource/SouthAfrica/GateFoundation/All_South_African_Newspapers2019-05-15_12-08.TXT']

txt_path['ETC_group'] = ['D:/GeneDrivePerception/resource/Nigeria/ETCgroup/News_Chronicle_(Nigeria)_The_Nigerian_Observ2019-05-14_17-03.TXT',
                         'D:/GeneDrivePerception/resource/SouthAfrica/ETCgroup/All_South_African_Newspapers2019-05-15_12-17.TXT']


''' sample text for choosing NER tool '''
sample_text = 'D:/GeneDrivePerception/resource/sampletext.txt'






