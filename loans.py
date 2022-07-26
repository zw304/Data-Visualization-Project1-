import os

import pandas as pd
import numpy as np
#os.getcwd()
loans = pd.read_csv('data/loans.csv')
print(loans.iloc[:5, :11])

loans_melt = pd.melt(loans,id_vars=['id', 'account_id', 'date', 'amount','payments'],#保持这几个columns不变
                        var_name='loan_m',
                    value_name='status')
loans_melt = loans_melt[loans_melt['status'] == 'X'].drop('status',axis=1)
print(loans_melt.head())
len(loans_melt.index) # 682

loan_m_split = loans_melt.loan_m.str.split('_')
#loans_melt[['terms','status']] = loans_melt.str.split('_')
print(loan_m_split[:5])
print(loan_m_split[-5:])

months=loan_m_split.str.get(0)
loan_status=loan_m_split.str.get(1)

loans_melt['terms']=months
loans_melt['status']=loan_status
print(loan_m_split[-5:])

#loans_melt["value"] = loans_melt["value"].replace("-","NA")

#reference for how to define rows: https://pythonhosted.org/trustedanalytics/ds_apir.html
def filter_status(row):
    if row['status'] == 'A' or row['status']=='B':
        return 'expired',
#    if row['status'] == 'C' or row['status'] == 'D':
    else:
        return'current'
loans_melt['loan_status'] = loans_melt.apply(lambda row:filter_status(row),axis=1)

def filter_default(row):
    if row['status'] == 'C' or row['status'] == 'A':
        return 'F',
#    if row['status'] == 'B' or row['status'] == 'D':
    else:
        return 'T'
loans_melt['loan_default'] = loans_melt.apply(lambda row: filter_default(row), axis=1)

loans_melt.drop(['loan_m','status'], inplace=True, axis=1) # drop original column

len(loans_melt.index) # 682

print(loans_melt.head())
loans_melt.to_csv('loans_py.csv',index=False)


