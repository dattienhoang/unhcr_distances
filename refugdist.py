# -*- coding: utf-8 -*-
"""
Created on Tue Apr 04 16:33:03 2017

@author: dahoang
"""

#import geopy   as gpy
import numpy as np
import pandas  as pd
import seaborn as sns

def haversine(lon1, lat1, lon2, lat2):
  """
  Calculate the great circle distance between two points 
  on the earth (specified in decimal degrees)
  """
  from math import radians, cos, sin, asin, sqrt
  # convert decimal degrees to radians 
  lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
  # haversine formula 
  dlon = lon2 - lon1 
  dlat = lat2 - lat1 
  a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
  c = 2 * asin(sqrt(a)) 
  km = 6367. * c
  # convert from km to miles
  dist = km/0.621371
  return dist

df = pd.read_csv('C:/Users/Dat Tien Hoang/Documents/GitHub/unhcr_distances/unhcr_popstats_export_asylum_all_data.csv', skiprows=3)
#df = pd.read_csv('C:/Users/Dat Tien Hoang/Documents/GitHub/unhcr_distances/unhcr_popstats_export_resettlement_all_data.csv', skiprows=3)
df = df.rename(index=str, columns={'Country / territory of asylum/residence':'Destination'})
# make all the words uppercase for ease
df['Destination'] = map(lambda x: x.upper(), df['Destination'])
df['Origin']      = map(lambda x: x.upper(), df['Origin'])

countries = pd.read_csv('C:\Users\Dat Tien Hoang\Documents\GitHub\unhcr_distances\countries.csv')
#countries['Destination'] = countries['name']
#countries['Origin']      = countries['name']
#countries['Destination'] = map(lambda x: x.upper(), countries['Destination'])
#countries['Origin']      = map(lambda x: x.upper(), countries['Origin'])
#countries = df.drop('country', axis=1)
#countries = df.drop('name', axis=1)
countries['name'] = map(lambda x: x.upper(), countries['name'])
countries.ix[countries['name'] == 'VIETNAM', 'name'] = 'VIET NAM'
countries.ix[countries['name'] == 'PALESTINIAN TERRITORIES', 'name'] = 'PALESTINIAN'

# do some joins...left joins
df = df.merge(countries, how='left', left_on='Destination', right_on='name', suffixes=['_UNHCR_d', '_countries_d'])
df = df.rename(index=str, columns={'latitude':'latitude_d', 'longitude':'longitude_d'})
df = df.merge(countries, how='left', left_on='Origin', right_on='name', suffixes=['_UNHCR_o', '_countries_o'])
df = df.rename(index=str, columns={'latitude':'latitude_o', 'longitude':'longitude_o'})

# next...calculate the distances between the countries!
#df['distance'] = ''
#for i in range(len(df['distance'])):
#    df['distance'][i] = haversine(df['longitude_d'][i], df['latitude_d'][i], df['longitude_o'][i], df['latitude_o'][i])

#df = df.fillna(value=0.)
#df['distance'] = df.apply(lambda row: haversine(df['longitude_d'][row], df['latitude_d'][row], df['longitude_o'][row], df['latitude_o'][row]),axis=1)

df['distance'] = [haversine(df['longitude_d'][i], df['latitude_d'][i], df['longitude_o'][i], df['latitude_o'][i]) for i in range(len(df))]
print 'done distances!'


df.ix[df['Value'] == '*', 'Value'] = '1'
df.ix[df['distance'] == np.nan, 'Value'] = '0'


#------------------------------------------------------------------------------
## SANDBOX - just test the data cleaning needed to get a violin plot
#df_temp = df.loc[df['Destination'] == 'CANADA']
#df_temp.ix[df_temp['Value'] == '*', 'Value'] = '1'
## reformatting and cleanup
#
#df_temp['Value'] = pd.to_numeric(df_temp['Value'], errors='coerce')
##df_temp['Value'] = df_temp['Value'].fillna(1)
#
##http://stackoverflow.com/questions/26777832/replicating-rows-in-a-pandas-data-frame-by-a-column-value
#df_temp2 = df_temp.loc[np.repeat(df_temp.index.values, pd.to_numeric(df_temp['Value']))]
##df_temp2 = df_temp
##for i in range(len(df_temp)):
##    df_temp2=df_temp2.append(df_temp.iloc[i,:]*pd.to_numeric(df_temp[i,:]))
#
#
## make a violinplot, plotting by origin
#sns.violinplot(x=pd.to_numeric(df_temp2['Year']), y=pd.to_numeric(df_temp2['distance']), data=df_temp2, palette="Set3", bw=.2, cut=1, linewidth=1)
#


#------------------------------------------------------------------------------
# choose several origins
df_temp = df.loc[(df['Origin'] == 'VIET NAM') ]#| 
#        (df['Origin'] == 'PALESTINIAN') | 
#        (df['Origin'] == 'AFGHANISTAN') |
#        (df['Origin'] == 'UGANDA') |
#        (df['Origin'] == 'SUDAN')]
df_temp.ix[df_temp['Value'] == '*', 'Value'] = '1'
# reformatting and cleanup

df_temp['Value'] = pd.to_numeric(df_temp['Value'], errors='coerce')
#df_temp['Value'] = df_temp['Value'].fillna(1)

print 'doing df2'
#http://stackoverflow.com/questions/26777832/replicating-rows-in-a-pandas-data-frame-by-a-column-value
df_temp2 = df_temp.loc[np.repeat(df_temp.index.values, pd.to_numeric(df_temp['Value']))]
#df_temp2 = df_temp
#for i in range(len(df_temp)):
#    df_temp2=df_temp2.append(df_temp.iloc[i,:]*pd.to_numeric(df_temp[i,:]))
print 'done df2'

# make a violinplot, plotting by origin
sns.violinplot(x=df_temp2['Origin'].astype(str), y=pd.to_numeric(df_temp2['distance']), data=df_temp2, palette="Set3", bw=.2, cut=1, linewidth=1)


sns.violinplot(x=df_temp2['year'].astype(str), y=pd.to_numeric(df_temp2['distance']), data=df_temp2, palette="Set3", bw=.2, cut=1, linewidth=1)

# no result for vietnam and palestine....seems to be bc string mismatch when performing merge