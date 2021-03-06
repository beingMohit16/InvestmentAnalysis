# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 22:39:39 2021

@author: mohit
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime 

"""
                                Check Point-1
"""

#importing Data
companies = pd.read_csv(r'E:\UPgrade\InvestmentAnalysis\companies.csv', encoding= 'unicode_escape')
rounds2 = pd.read_csv(r'E:\UPgrade\InvestmentAnalysis\rounds2.csv',encoding = 'unicode_escape')

#creating company and companytype column in round2
rounds2['company'] = rounds2['company_permalink'].apply(lambda x : x.split(r'/')[-1]).str.lower()
rounds2['companytype'] = rounds2['company_permalink'].apply(lambda x : x.split(r'/')[-2]).str.lower()

#rounds3 = rounds2.company_permalink.str.split(n=1, expand=True)
#rounds3.columns = ['STATUS_ID{}'.format(x+1) for x in rounds3.columns]

#Getting Unique column
print('No of the Unique companies in round2 : ',len(pd.unique(rounds2['company'])))

#getting data information
companies.info()
companies.name.describe()

#Normalization of conditional column
companies.permalink = companies.permalink.str.lower()
rounds2.company_permalink = rounds2.company_permalink.str.lower()

#cheking the unique value
rounds2.company_permalink.nunique(dropna = True)
companies.permalink.nunique(dropna = True)

#Companies in the rounds2 file which are not  present in companies
rounds2[~rounds2['company_permalink'].isin(companies['permalink'])]

#Merging the dataframe
master_frame = pd.merge(companies,rounds2,how = 'inner',left_on = 'permalink',right_on='company_permalink') 
master_frame.shape

#Removing Duplicate Column
master_frame = master_frame.drop('permalink', axis=1)

"""
                                Check Point-2
"""


#getting data information
master_frame.funding_round_type.value_counts()
master_frame.country_code.value_counts()

#test = pd.DataFrame(rounds2[rounds2['funding_round_type'].isin (['venture','angel','seed','private_equity'])].groupby('funding_round_type')['raised_amount_usd'].mean())
#test['com'] = master_frame[master_frame['funding_round_type'].isin (['venture','angel','seed','private_equity'])].groupby('funding_round_type')['company_permalink'].count()
#test['round'] = master_frame[master_frame['funding_round_type'].isin (['venture','angel','seed','private_equity'])].groupby('funding_round_type')['funding_round_code'].count()

#most representative value of the investment amount
spark_funding_type = pd.DataFrame(rounds2[rounds2['funding_round_type'].isin (['venture','angel','seed','private_equity'])].groupby('funding_round_type')['raised_amount_usd'].mean().sort_values(ascending = False))
spark_funding_type['inrange'] = spark_funding_type['raised_amount_usd'].apply(lambda x : 1 if x > 5000000 and x < 15000000 else 0)
'''
We can find that venture is the appropiate funding type for the Spark

'''
#Getting the top9 country and there amount
top9 = pd.DataFrame(master_frame[master_frame['funding_round_type'] == 'venture'].groupby('country_code')['raised_amount_usd'].sum().sort_values(ascending = False).head(9))
top9 = top9.reset_index()

"""
                                Check Point-4
"""

master_frame.category_list.value_counts()

#spark_funding_venture = pd.DataFrame(master_frame[(master_frame['funding_round_type'] == 'venture') , 
#                                                  (master_frame['country_code'].isin(['USA','GBR','IND']))
#                                                  ])

spark_funding_venture = master_frame.loc[(master_frame['country_code'].isin(['USA','GBR','IND'])),:]
spark_funding_venture = spark_funding_venture.loc[(spark_funding_venture['funding_round_type'] == 'venture'),:]

#Data Check
spark_funding_venture.country_code.value_counts()
spark_funding_venture.funding_round_type.value_counts()
spark_funding_venture.category_list.value_counts()
spark_funding_venture.category_list.describe()
spark_funding_venture['primary_sector'] = spark_funding_venture['category_list'].str.split('|').str[0].str.upper()


mapping = pd.read_csv(r'E:\UPgrade\InvestmentAnalysis\mapping.csv')
mapping.isnull().sum()
mapping.dropna(inplace = True)

#sector_mapping = mapping.melt(id_vars="category_list",var_name="main_sector")

mapping = pd.melt(mapping,id_vars = "category_list")
mapping = mapping[mapping.value != 0]
mapping = mapping.drop('value',axis = 1)
mapping.info()

mapping['category_list'] = mapping['category_list'].str.upper()



top3_eng_speaking = pd.merge(spark_funding_venture,mapping,how='left',left_on='primary_sector',right_on='category_list')
top3_eng_speaking.drop(columns=["category_list_y"],inplace=True)
#top3_eng_speking = top3_eng_speking[top3_eng_speking['_merge'] == 'both']
#top3_eng_speking.main_sector.value_counts()
#
D1=top3_eng_speaking.loc[top3_eng_speaking['country_code']=='USA']
D2=top3_eng_speaking.loc[top3_eng_speaking['country_code']=='GBR']
D3=top3_eng_speaking.loc[top3_eng_speaking['country_code']=='IND']

TNIC_usd=pd.DataFrame(D1.groupby(by='variable')['variable'].count().
                     rename('Total_Investment_Count').sort_values(ascending = False)).head(3)

TNIC_gbr=pd.DataFrame(D2.groupby(by='variable')['variable'].count().
                     rename('Total_Investment_Count').sort_values(ascending = False)).head(3)

TNIC_ind=pd.DataFrame(D3.groupby(by='variable')['variable'].count().
                     rename('Total_Investment_Count').sort_values(ascending = False)).head(3)


TAI_USD=pd.DataFrame(D1.groupby(by='variable')['raised_amount_usd'].sum().
                     rename('Total_Investment_Amount').sort_values(ascending = False))


TAI_gbr=pd.DataFrame(D2.groupby(by='variable')['raised_amount_usd'].sum().
                     rename('Total_Investment_Amount').sort_values(ascending = False))


TAI_ind=pd.DataFrame(D3.groupby(by='variable')['raised_amount_usd'].sum().
                     rename('Total_Investment_Amount').sort_values(ascending = False))


D3[D3.variable == 'News, Search and Messaging'].groupby(['homepage_url','name'])['raised_amount_usd'].count().sort_values(ascending=False).head(3)

#Graph



