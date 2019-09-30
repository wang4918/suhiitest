# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 10:00:46 2019

@author: wang_mc
"""

import geopandas as gpd
import pandas as pd
import os
from scipy import stats


path = 'C:\\Users\\wang_mc\\VSCode\\CSVs'
os.chdir(path)

def getSuhii(csvfile):
    suhii = stats.linregress(csvfile['isapercent'], csvfile['mean'])[0]
    return suhii*100

cityname = ['Addis_Abeba','Amsterdam','Ankara','Athens','Beijing','Berlin','Birmingham',
        'Bruxelles','Budapest','Casablanca','Chicago','Copenhagen','Dehli',
        'Dubai',"Dublin",'Geneva','Glasgow','Gothenburg','Hamburg','Helsinki',
        'Hong_Kong','Izmir','Jerusalem','Johannesburg','Lisbon','London','Madrid',
        'Medellin','Melbourne','Milan','Montreal','Munich','Nairobi','Niigata','Oslo',
        'Paris','Phoenix','Portland','Prag','Roma','Santiago','Seoul','Shizouka',
        'Singapore','Stockholm','Strasburg','Sydney','Taipeh','Tallinn','Teheran',
        'Tshwane','Turin','Vancouver','Vienna','Warsaw','Zuerich']

for city in cityname:
    shp = gpd.read_file('C:\\Users\\wang_mc\\Documents\\SUHII\\UnloadedTrak\\%s_DIS_Indizes.shp'%city)
    summer = pd.read_csv('%sSummer.csv'%city)
    winter = pd.read_csv('%sWinter.csv'%city)
    annual = pd.read_csv('%sAnnual.csv'%city)
    shp = shp.assign(SummerSUHII = getSuhii(summer))
    shp = shp.assign(WinterSUHII = getSuhii(winter))
    shp = shp.assign(AnnualSUHII = getSuhii(annual))
    shp.to_file('%s_DIS_Indizes.shp'%city)





























