# -*- coding: utf-8 -*-
"""
Created on Tue Apr 04 16:33:03 2017

@author: dahoang
"""

#import geopy   as gpy
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

df = pd.read_csv('C:/Users/Dat Tien Hoang/Documents/GitHub/unhcr_distances/unhcr_popstats_export_resettlement_all_data.csv', skiprows=3)
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

# do some joins...left joins
df = df.merge(countries, how='left', left_on='Destination', right_on='name', suffixes=['_UNHCR_d', '_countries_d'])
df = df.rename(index=str, columns={'latitude':'latitude_d', 'longitude':'longitude_d'})
df = df.merge(countries, how='left', left_on='Origin', right_on='name', suffixes=['_UNHCR_o', '_countries_o'])
df = df.rename(index=str, columns={'latitude':'latitude_o', 'longitude':'longitude_o'})

# next...calculate the distances between the countries!
df['distance'] = ''
for i in range(len(df['distance'])):
    df['distance'][i] = haversine(df['longitude_d'][i], df['latitude_d'][i], df['longitude_o'][i], df['latitude_o'][i])

# make a violinplot, plotting by origin
sns.violinplot(x='Year', y='Origin', hue='distance', data=df, palette="Set3", bw=.2, cut=1, linewidth=1)
