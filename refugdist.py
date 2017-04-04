# -*- coding: utf-8 -*-
"""
Created on Tue Apr 04 16:33:03 2017

@author: dahoang
"""

import geopy   as gpy
import pandas  as pd
import seaborn as sns

def haversine(lon1, lat1, lon2, lat2):
  """
  Calculate the great circle distance between two points 
  on the earth (specified in decimal degrees)
  """
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

df = pd.read_csv('')

sns.violinplot(x='year', y='country', hue='dist', data=df, palette="Set3", bw=.2, cut=1, linewidth=1)
