import geopandas as gpd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import os
import math
from scipy import stats

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

    df = df.append({"Season": season,"SUHII": round(linreg[0]*100, 3), "R-Squared": round((linreg[2]*linreg[2]),3), "Std. Error": round(linreg[4],5)}, ignore_index=True)
    
    
  g = sns.lmplot(x = 'isapercent', y = 'meanvalue', hue = 'season', truncate = True, data = melted,
              palette=dict(Summer='r',Annual='y',Winter='b', ), order = magorder, legend= False)
  g.set_axis_labels('ISA%', 'Mean LST (\u00b0C)')
  
#  plt.ylim(0,45)

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
  plt.show()
  

path = 'C:\\Users\\wang_mc\\Documents\\SUHII\\CSVs'
os.chdir(path)

summer = pd.read_csv('OsloSummer.csv')
winter = pd.read_csv('OsloWinter.csv')
annual = pd.read_csv('OsloAnnual.csv')
plotisalst(summer, winter, annual, 'Oslo', 3)

plt.figure()
sns.residplot(summer['isapercent'], summer['mean'], order=3, color='r')
sns.residplot(winter['isapercent'], winter['mean'], order=3, color='b')
sns.residplot(annual['isapercent'], annual['mean'], order=3, color='y')
plt.show()
