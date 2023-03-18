from statistics import median
import pandas as pd
import json
import plotly.express as px  
import numpy as np
import os

path = os.path.join(os.getcwd(),'data_clean')
data = pd.read_csv(os.path.join(path, "home_value.csv"))

# Rename GEOIDs
renamed_geoid = []
for row in data['GEOID']:
    tract_num = (row.split(',')[0]).replace("Census Tract ",'')
    if ('.' in tract_num):
        if len(tract_num) == 6:
            tract_num = '0' + tract_num
        tract_num = '17031' + tract_num.replace('.','')
    else:
        if len(tract_num) == 3:
            tract_num = '0' + tract_num
        tract_num = '17031' + tract_num + '00'
    renamed_geoid.append(int(tract_num))
data['GEOID'] = renamed_geoid

data = data.apply(pd.to_numeric, errors='coerce')

# Drop observations above median
data_2016 = data[data['YEAR'] == 2016]
data_2018 = data[data['YEAR'] == 2018]
median_house_value = np.median(data_2016['house_value'])
data_2016 = data_2016.drop(data_2016[data_2016.house_value > median_house_value].index)
print(data_2018.head())
print(data_2016.head())

data['ratio_lg_18_16'] = np.log(data_2018['house_value']/data_2016['house_value']) 
data['ratio_18_16'] = data_2018['house_value']/data_2016['house_value']

print(data.head())

# gentrification_data = pd.read_csv(os.path.join('data_clean','chicago.csv'))

# top_y_values_lg = data.nlargest(20, ['ratio_lg_18_16'])
# top_y_values = data.nlargest(20, ['ratio_18_16'])

# gent_data_grouped = gentrification_data.groupby('Typology')

# dict = {}

# for name, group in gent_data_grouped:
#     dict[name] = 0
#     for value in top_y_values_lg['GEOID']:
#         the_list = group['GEOID'].tolist()
#         if value in the_list:
#             dict[name] += 1

# print(dict)