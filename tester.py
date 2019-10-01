import geopandas as gpd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import os
import math
from scipy import stats

def polyfit(x, y, degree):
    results = {}

    coeffs = np.polyfit(x, y, degree)

     # Polynomial Coefficients
    results['polynomial'] = coeffs.tolist()

    # r-squared
    p = np.poly1d(coeffs)
    # fit values, and mean
    yhat = p(x)                         # or [p(z) for z in x]
    ybar = np.sum(y)/len(y)          # or sum(y)/len(y)
    ssreg = np.sum((yhat-ybar)**2)   # or sum([ (yihat - ybar)**2 for yihat in yhat])
    sstot = np.sum((y - ybar)**2)    # or sum([ (yi - ybar)**2 for yi in y])
    results['determination'] = ssreg / sstot

    return results

def plotisalst(summer, winter, annual, name, magorder):
  
  joined = summer.merge(annual, 'inner', 'isapercent', suffixes = ('summer', 'annual'))
  joined = joined.merge(winter, 'inner', 'isapercent')
  joined.columns = ['isapercent','Summer', 'Annual', 'Winter']
  joined = joined.dropna()
  

  melted = pd.melt(joined, id_vars = ['isapercent'], value_vars = ['Summer', 'Annual', 'Winter'], var_name='season', value_name='meanvalue')
  
  seasons = ['Summer', 'Annual', 'Winter']
  df = pd.DataFrame(columns = ['Season', 'SUHII', 'R-Squared', 'Std. Error'])

  for season in seasons:
    linreg = stats.linregress(joined['isapercent'], joined[season])

    df = df.append({"Season": season,"SUHII": round(linreg[0]*100, 3), "R-Squared": round(polyfit(joined['isapercent'], joined[season], magorder)['determination'],3), "Std. Error": round(linreg[4],5)}, ignore_index=True)
    
    
  g = sns.lmplot(x = 'isapercent', y = 'meanvalue', hue = 'season', truncate = True, data = melted,
              palette=dict(Summer='r',Annual='y',Winter='b', ), order = magorder, legend= False)
  g.set_axis_labels('ISA%', 'Mean LST (\u00b0C)')
  
  plt.ylim(0,45)

  plt.title('%s ISA vs Mean LST' %(name))
  plt.legend(loc='lower left', bbox_to_anchor=(-.15,-0.485),
             fontsize = 'medium',
             labelspacing = 0.53,
             markerfirst = False,
             frameon = False, facecolor = 'w')

  plt.table(cellText=df[['SUHII', 'R-Squared', "Std. Error"]].values,
          rowLabels=['      ', '      ', '      '],
          colLabels=df[['SUHII', 'R-Squared', "Std. Error"]].columns,
          cellLoc='right', rowLoc='center',
          loc='lower right', bbox=[0.15,-0.45,0.85,.28])
  plt.subplots_adjust(bottom=0.3)
  plt.savefig('C:\\Users\\wang_mc\\VSCode\\CURE\\%s.png'%name)
  

path = 'C:\\Users\\wang_mc\\VSCode\\CURE'
os.chdir(path)

cityname = ['Basel', 'Berlin', 'Bristol', 'Copenhagen', 'Heraklion',
            'Munich', 'Ostrava', 'Vitoria_Gasteiz']

# ['Addis_Abeba','Amsterdam','Ankara','Athens','Beijing','Berlin','Birmingham',
#         'Bruxelles','Budapest','Casablanca','Chicago','Copenhagen','Dehli',
#         'Dubai',"Dublin",'Geneva','Glasgow','Gothenburg','Hamburg','Helsinki',
#         'Hong_Kong','Izmir','Jerusalem','Johannesburg','Lisbon','London','Madrid',
#         'Medellin','Melbourne','Milan','Montreal','Munich','Nairobi','Niigata','Oslo',
#         'Paris','Phoenix','Portland','Prag','Roma','Santiago','Seoul','Shizouka',
#         'Singapore','Stockholm','Strasburg','Sydney','Taipeh','Tallinn','Teheran',
#         'Tshwane','Turin','Vancouver','Vienna','Warsaw','Zuerich']

for city in cityname:
  summer = pd.read_csv('%sSummer.csv'%city)
  winter = pd.read_csv('%sWinter.csv'%city)
  annual = pd.read_csv('%sAnnual.csv'%city)
  plotisalst(summer, winter, annual, city, 1)
  plt.figure()
  sns.residplot(summer['isapercent'], summer['mean'], order=1, color='r')
  sns.residplot(winter['isapercent'], winter['mean'], order=1, color='b')
  sns.residplot(annual['isapercent'], annual['mean'], order=1, color='y')
  plt.savefig('C:\\Users\\wang_mc\\VSCode\\Charts\\%sResid.png'%city)
