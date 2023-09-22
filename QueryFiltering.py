# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd 
import fastparquet #make sure that this is installed in your anaconda environment
import numpy as np
import statistics as stat
import matplotlib.pyplot as plt
from scipy import stats
import array

#loads the file into the label "data"
filename='C:\\Users\james\OneDrive\Documents\Capstone\BR00121436.parquet' #edit the filename here for testing other .parquet files

data=pd.read_parquet(filename, engine='fastparquet') 

data_numerical=data._get_numeric_data() #removing columns that have non quantitiative data

df_normalized = (0.6745 * (data_numerical - data_numerical.median(axis=0))) / stats.median_abs_deviation(data_numerical, axis=0)
df_normalized=df_normalized.dropna(axis=1) #get rid of data ruined by normalization (not numeric)
df_normalized.shape

#remove outliers

n_MAD = 500
threshold = 0.6745 * n_MAD

rows_to_keep = np.empty([1,df_normalized.shape[1]])
for x in range(0,df_normalized.shape[0]-1): #parse through each individual row of new data set
    df_normalized_row = np.array([df_normalized.loc[x]])
    if (df_normalized_row<threshold).all(): #check if any values are above threshold, if not, add to kept rows
        rows_to_keep = np.vstack([rows_to_keep,df_normalized_row])  #appending rows to new array

rows_to_keep.shape #thank god I spent an hour trying to figure it out when Ryan and Matt had it in 2 lines of code
print(rows_to_keep.shape)

#remove highly correlated features
#you will need to pip install feature engine in the conda environment!!

#code from sam

from sklearn.datasets import make_classification
from feature_engine.selection import DropCorrelatedFeatures

#%%
# Calculate the correlation matrix
corr_matrix = df_normalized.corr()

# Create a dictionary to store correlated feature groups
correlated_features = {}

# Iterate through the correlation matrix
for feature in corr_matrix.columns:
    correlated_group = corr_matrix.index[corr_matrix[feature] > 0.9].tolist()
    if correlated_group:
        correlated_group.append(feature)  # Include the current feature in the group
        correlated_features[feature] = correlated_group

# Select one feature from each correlated group to retain
features_to_retain = set()
for group in correlated_features.values():
    features_to_retain.add(group[0])

# Drop the remaining correlated columns
data_dropped = data.drop(columns=set(data.columns) - features_to_retain)
#%%
# Define the queried dropped column
queried_dropped_column = 'Nuclei_Texture_InverseDifferenceMoment_DNA_10_02_256'

# Determine which retained column is correlated with the queried dropped column
correlated_retained_column = None
for retained_column in features_to_retain:
    if queried_dropped_column in correlated_features and retained_column in correlated_features[queried_dropped_column]:
        correlated_retained_column = retained_column
        break
    
print(f"The column '{correlated_retained_column}' is correlated with the queried dropped column '{queried_dropped_column}'")

#%% Parsing by headers

headers = df_normalized.columns
newdata = df_normalized

#%% Filtering based on multiple inputs
def filtering2(df, filter_words):
    df2 = df

    for word in filter_words:
        filtered_dataframes = df2.filter(like=word, axis=1)
        df2=filtered_dataframes
        print(df2.columns)
    
    return filtered_dataframes

filtering2(newdata,['Nuclei', 'AreaShape'])  #take input values from queries

