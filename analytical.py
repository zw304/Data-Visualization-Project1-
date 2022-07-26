import os
import pandas as pd
import numpy as np
os.getcwd()
account = pd.read_csv('/data/accounts.csv')
district = pd.read_csv('/district_py.csv')
clients = pd.read_csv('/data/clients.csv')
links = pd.read_csv('/data/links.csv')
cards = pd.read_csv('/data/cards.csv')
loan= pd.read_csv('/loans_py.csv')
payment_orders = pd.read_csv('/data/payment_orders.csv')
transactions = pd.read_csv('/data/transactions.csv')

#join account and district:
print(account.iloc[:5, :11])
print(district.iloc[:5, :11])

#rename column name
district.rename(columns = {'id':'district_id'}, inplace = True)
district.dtypes
merge_AD = pd.merge(account,district, how= "left",on=['district_id'])
print(merge_AD)
merge_AD.dtypes

merge_AD.rename(columns = {'id':'account_id'}, inplace = True)
merge_AD.rename(columns = {'date':'open_date'}, inplace = True)
merge_AD.rename(columns = {'name':'district_name'}, inplace = True)
merge_AD.dtypes #4500

AD=merge_AD[['account_id','district_name','open_date','statement_frequency']]
AD.dtypes #done

# left join "links" table to AD table:
# group by reference: https://www.shanelynn.ie/summarising-aggregation-and-grouping-data-in-python-pandas/
links_by = links.groupby('account_id')['type'].count().reset_index(name = 'num_customers') # works
#links_by.columns = ['account_id','num_customers'] try but failed
links_by.dtypes # they are both int64, expected get

merge_ADL = pd.merge(AD,links_by, how= "left",on=['account_id'])
print(merge_ADL) # 4500rows, 5 cols

#join "cards" to "links" table:
cards.dtypes
#cards.drop('type', inplace=True, axis=1)
#cards.drop('issue_date', inplace=True, axis=1) # drop useless columns
print(cards.iloc[:5, :11])

links.rename(columns = {'id':'link_id'}, inplace = True)
links.dtypes
cards.rename(columns = {'type':'card_type'}, inplace = True)
cards.dtypes
merge_LC = links.merge(cards, how= "left",on=['link_id'])
len(merge_LC.index)#5369

print(merge_LC.iloc[:5, :11])
merge_LC1=merge_LC.groupby('account_id')['card_type'].count().reset_index(name ='credit_cards')
print(merge_LC1.iloc[:5, :11])
len(merge_LC1.index) # 4500

#join LC to ADL --> ADLC
ADLC=merge_ADL.merge(merge_LC1,how= "left",on=['account_id'])
print(ADLC.iloc[:5, :11])
ADLC.dtypes
len(ADLC.index) #4500

#join ADLC to loans:
print(loan)
print(ADLC)
ADLC_=ADLC.merge(loan,how= "left",on=['account_id'])
ADLC_.dtypes
len(ADLC_.index) #4500

ADLC_.rename(columns = {'id':'loan'}, inplace = True)
ADLC_.rename(columns = {'amount':'loan_amount'}, inplace = True)
#ADLC_.rename(columns = {'date':'open_date'}, inplace = True)
ADLC_.rename(columns = {'payments':'loan_payments'}, inplace = True)
ADLC_.rename(columns = {'terms':'loan_terms'}, inplace = True)

ADLC_.dtypes
len(ADLC_.index) #4500 rows

# drop useless columns:
ADLC_.drop('date', inplace=True, axis=1) # drop columns "date"

#loans_melt.to_csv('analytical_py.csv',index=False)
ADLC_.dtypes

#max_withdrawal: first try, failed.
#print(transactions.iloc[:5, :11])
#max_with=transactions[transactions["type"]=='debit']
#print(max_with)
#min_with=transactions[transactions["type"]=='debit']

#second try:
#merge them:
ADLC_W = ADLC.merge(max_with,how= "left")
# max
max_with1=transactions[["account_id","amount","type"]].groupby(["account_id","type"]).max()
max_with2 = max_with1.pivot_table(index=["account_id"],columns="type",values = "amount")
max_with2.drop("credit",inplace=True,axis=1)
max_with2.rename({"debit":"max_withdrawal"},inplace=True,axis=1)
print(max_with2)
min_with1=transactions[["account_id","amount","type"]].groupby(["account_id","type"]).min()
min_with2 = min_with1.pivot_table(index=["account_id"],columns="type",values = "amount")
min_with2.drop("credit",inplace=True,axis=1)
min_with2.rename({"debit":"min_withdrawal"},inplace=True,axis=1,)

# merge min&max together:
ADLC_M = pd.merge(ADLC_,max_with2, how= "left",on=['account_id'])
print(ADLC_M)
ADLC_M = pd.merge(ADLC_M,min_with2, how= "left",on=['account_id'])
print(ADLC_M)
#4500 rows & 14 columns


# join cc_payments:
cc_payments = payment_orders["account_id"].value_counts()
print(cc_payments)
cc_payments=pd.DataFrame(cc_payments)
cc_payments.reset_index(axis=1,inplace=True)
cc_payments.rename({"index":"cc_payment"},axis=1,inplace=True)
#cc_payments2 = cc_payments.reset_index().rename(columns={cc_payments.index.name:'account_id'})
#print(cc_payments2)
#ADLC_CC=ADLC_M.merge(cc_payments,how="left",on=['account_id'])
#print(ADLC_CC) # 4500rows
ADLC_M.to_csv('analytical_py.csv',index=False)

#join max_balance: 
#print(transactions)
#max_b= transactions[["account_id","balance"]].groupby("account_id")
#max().reset_index(inplace=True)
#print(max_b)
#max_b.rename({"balance":"max_balance"},axis=1,inplace=True)
#min_b = transactions[["account_id","balance"]].groupby("account_id").min().reset_index(inplace=True)
#min_b.rename({"balance":"min_balance"},axis=1,inplace=True)

# join