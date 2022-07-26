import os
import pandas as pd
import numpy as np
#os.getcwd()
district = pd.read_csv('/data/districts.csv')
print(district.iloc[:5, :11])
district.dtypes # check the data type, we know that municipality_info is object, we would like to convert it into string
district['municipality_info']=district['municipality_info'].str.replace(']','').str.replace('[','')
district['unemployment_rate']=district['unemployment_rate'].str.replace(']','').str.replace('[','')
district['commited_crimes']=district['commited_crimes'].str.replace(']','').str.replace('[','')
print(district.iloc[:5, :11])
district.dtypes
#split, rename, and add more columns for municipality_info
municipality_info_split = district.municipality_info.str.split(',')
p_500=municipality_info_split.str.get(0)
p_1999=municipality_info_split.str.get(1)
p_9999=municipality_info_split.str.get(2)
p_10000=municipality_info_split.str.get(3)
district['Population < 500']=p_500
district['Population 500-1999'] = p_1999
district['Population 2000-9999'] = p_9999
district['Population >= 10000'] = p_10000
district.dtypes
district.drop('municipality_info', inplace=True, axis=1)
district.dtypes

#split, rename, and add more columns for unemployment_rate
unemployment_rate_split = district.unemployment_rate.str.split(',')
unemployment_rate_95=unemployment_rate_split.str.get(0)
unemployment_rate_96=unemployment_rate_split.str.get(1)
district['unemployment_rate_95']=unemployment_rate_95
district['unemployment_rate_96'] = unemployment_rate_96
district.drop('unemployment_rate', inplace=True, axis=1)
district.dtypes

#split, rename, and add more columns for commited_crimes
commited_crimes_split = district.commited_crimes.str.split(',')
commited_crimes_95=commited_crimes_split.str.get(0)
commited_crimes_96=commited_crimes_split.str.get(1)
district['commited_crimes_95']=commited_crimes_95
district['commited_crimes_96'] = commited_crimes_96
district.drop('commited_crimes', inplace=True, axis=1) # drop original column
district.dtypes
district.to_csv('district_py.csv')
