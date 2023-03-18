import pandas as pd
import json
import plotly.express as px  
import numpy as np
import os

path = os.path.join(os.getcwd(),'data_clean')
data = pd.read_csv(os.path.join(path, "home_value.csv"))
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

data_2016 = data[data['YEAR'] == 2016].reset_index()
data_2017 = data[data['YEAR'] == 2017].reset_index()
data_2018 = data[data['YEAR'] == 2018].reset_index()
data_2019 = data[data['YEAR'] == 2019].reset_index()

data_2019 = data_2019.rename(columns = {"house_value": "house_value_2019"})
data_2016 = data_2016.rename(columns = {"house_value": "house_value_2016"})

y_labels = pd.merge(data_2016, data_2019, on = ['GEOID'])
median_house_val_ratio = data_2019['house_value_2019'].median() / data_2016['house_value_2016'].median()
median_house_val_2016 = data_2016['house_value_2016'].median()

y_labels['ratio'] = y_labels['house_value_2019'] / y_labels['house_value_2016']
y_labels['label'] = np.where((y_labels['house_value_2016'] < median_house_val_2016) & (y_labels['ratio'] >  median_house_val_ratio), 1, 0)
y_labels = y_labels[['GEOID', 'label']]

#data_2019['ratio'] = np.log(data_2019['house_value']/data_2016['house_value']) # y variable

with open(os.path.join(os.getcwd(),'tracts.geojson')) as file:
        tracts = json.load(file)
    
fig = px.choropleth_mapbox(y_labels, geojson=tracts, locations='GEOID', 
                                featureidkey="properties.geoid10",
                                color = y_labels['label'],                                 
                                mapbox_style="carto-positron",
                                zoom=9, center = {"lat": 41.81, "lon": -87.7},
                                opacity=0.5,
                                labels={})

fig.show()

displ = pd.read_csv(os.path.join(path, "chicago.csv"))

displ['binary'] = 'Stable'
displ.loc[displ['Typology'] == 'At Risk of Gentrification', 'binary'] = 'Gentrifying'
displ.loc[displ['Typology'] == 'Early/Ongoing Gentrification', 'binary'] = 'Gentrifying'
displ.loc[displ['Typology'] == 'Low-Income/Susceptible to Displacement', 'binary'] = 'Gentrifying'
displ.loc[displ['Typology'] == 'Ongoing Displacement', 'binary'] = 'Gentrifying'

displ.loc[displ['Typology'] != 'At Risk of Gentrification' and displ['Typology'] != 'Early/Ongoing Gentrification', 'binary'] = 'Stable' 


fig2 = px.choropleth_mapbox(displ, geojson=tracts, locations='GEOID', 
                                featureidkey="properties.geoid10",
                                color = displ['binary'],                                 
                                mapbox_style="carto-positron",
                                zoom=9, center = {"lat": 41.81, "lon": -87.7},
                                opacity=0.5,
                                labels={})

fig2.show()