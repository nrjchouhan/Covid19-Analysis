#!/usr/bin/env python
# coding: utf-8


# Importing libraries
import pandas as pd
from datetime import datetime, date, timedelta

# Reading cowin_vaccine_data_districtwise.csv file into vaccine_data DataFrame
vaccine_data = pd.read_csv('input/cowin_vaccine_data_districtwise.csv')

# Dictionary of mapping of state and state code - sample entry: 'Madhya Pradesh': 'MP'
state_code_dict = vaccine_data[vaccine_data['S No'] > 0][['State','State_Code']].drop_duplicates().set_index('State').T.to_dict('list')
state_code_dict = dict(zip(list(state_code_dict),[l[0] for l in list(state_code_dict.values())]))
state_code_dict

# List of columns names containing number of 1st and 2nd dose administrated with 'District_Key' column name
colList = ['District_Key']
startDt = date(2021,1,16)
endDt = date(2021,8,15)
dtRangeList = pd.date_range(startDt,endDt-timedelta(days=1),freq='d')
for dt in dtRangeList:
    colList.append(dt.strftime('%d/%m/%Y') + '.3')
    colList.append(dt.strftime('%d/%m/%Y') + '.4')

# Selecting columns in above list from vaccine_data DataFrame and replace NaN values with 0
vaccineDf = vaccine_data[colList].fillna(0)
vaccineDf.iat[0,0] = None
vaccineDf = vaccineDf.drop(0)
colList.remove('District_Key')
vaccineDf[colList] = vaccineDf[colList].apply(pd.to_numeric)

# Merging common districts and adding their number of dose administrated
vaccineDf = vaccineDf.groupby('District_Key',sort=False).sum()
vaccineDf = vaccineDf.reset_index()

# Taking transpose of above vaccineDf Dataframe
vDf = vaccineDf.T.reset_index()
vDf.iat[0,0] = 'Date'
vDf.columns = vDf.iloc[0]
vDf = vDf.drop(0)
vDf = vDf.reset_index(drop=True)


# Vaccination data is available from 16 jan'2021 to 14 aug'2021. So considering week-1 from 10 jan'2021 to 16 jan'2021
# Creating DataFrame contains number of 1st and 2nd dose administrated per week for each district 
vCountWeekList = []
for col in vDf.columns.difference(['Date']):
    distList = vDf[col].to_list()
    for ii in range(14):
        distList.insert(0,0)
    tid = 1
    for i in range(2,436,14):
        d1 = int(distList[i+12]) - int(distList[i-2])
        d2 = int(distList[i+13]) - int(distList[i-1])
        vCountWeekList.append([col, tid, d1, d2])
        tid += 1
vCountWeekDf = pd.DataFrame(vCountWeekList, columns = ['districtid','weekid','dose1','dose2'])
vCountWeekDf


# Creating DataFrame contains number of 1st and 2nd dose administrated per week for each state 
vCountWeekStList = []
for st in state_code_dict.keys():
    stDF = vCountWeekDf.loc[vCountWeekDf['districtid'].str.contains(state_code_dict[st])]
    for w in range(1,32):
        vCountWeekStList.append([st, w, sum(stDF[stDF['weekid'] == w]['dose1'].to_list()),sum(stDF[stDF['weekid'] == w]['dose2'].to_list())])
vCountWeekStDf = pd.DataFrame(vCountWeekStList, columns=['stateid','weekid','dose1','dose2']).sort_values(by=['stateid','weekid']).reset_index(drop=True)
vCountWeekStDf


# Creating DataFrame contains number of 1st and 2nd dose administrated per month for each district 
vCountMonthList = []
for col in vDf.columns.difference(['Date']):
    distList = vDf[(vDf['Date']=='14/01/2021.3') | 
                   (vDf['Date']=='14/01/2021.4') | 
                   (vDf['Date']=='14/02/2021.3') | 
                   (vDf['Date']=='14/02/2021.4') | 
                   (vDf['Date']=='14/03/2021.3') | 
                   (vDf['Date']=='14/03/2021.4') | 
                   (vDf['Date']=='14/04/2021.3') | 
                   (vDf['Date']=='14/04/2021.4') | 
                   (vDf['Date']=='14/05/2021.3') | 
                   (vDf['Date']=='14/05/2021.4') | 
                   (vDf['Date']=='14/06/2021.3') | 
                   (vDf['Date']=='14/06/2021.4') | 
                   (vDf['Date']=='14/07/2021.3') |
                   (vDf['Date']=='14/07/2021.4') | 
                   (vDf['Date']=='14/08/2021.3') | 
                   (vDf['Date']=='14/08/2021.4')][col].to_list()
    distList.insert(0,0)
    distList.insert(0,0)
    tid = 1
    for i in range(0,14,2):
        d1 = int(distList[i+2]) - int(distList[i])
        d2 = int(distList[i+3]) - int(distList[i+1])
        vCountMonthList.append([col, tid, d1, d2])
        tid += 1
vCountMonthDf = pd.DataFrame(vCountMonthList, columns = ['districtid','monthid','dose1','dose2'])


# Creating DataFrame contains number of 1st and 2nd dose administrated per month for each state 
vCountMonthStList = []
for st in state_code_dict.keys():
    stDF = vCountMonthDf.loc[vCountMonthDf['districtid'].str.contains(state_code_dict[st])]
    for w in range(1,8):
        vCountMonthStList.append([st, w, sum(stDF[stDF['monthid'] == w]['dose1'].to_list()),sum(stDF[stDF['monthid'] == w]['dose2'].to_list())])
vCountMonthStDf = pd.DataFrame(vCountMonthStList, columns=['stateid','monthid','dose1','dose2']).sort_values(by=['stateid','monthid']).reset_index(drop=True)
vCountMonthStDf


# Creating DataFrame contains number of 1st and 2nd dose administrated in overall duration for each district 
vCountOverallList = []
for col in vDf.columns.difference(['Date']):
    distList = vDf[(vDf['Date']=='14/08/2021.3') | 
                   (vDf['Date']=='14/08/2021.4')][col].to_list()
    vCountOverallList.append([col, 1, distList[0], distList[1]])
vCountOverallDf = pd.DataFrame(vCountOverallList, columns = ['districtid','overallid','dose1','dose2'])


# Creating DataFrame contains number of 1st and 2nd dose administrated in overall duration for each state 
vCountOverallStList = []
for st in state_code_dict.keys():
    stDF = vCountOverallDf.loc[vCountOverallDf['districtid'].str.contains(state_code_dict[st])]
    vCountOverallStList.append([st, 1, sum(stDF[stDF['overallid'] == 1]['dose1'].astype(int).to_list()),sum(stDF[stDF['overallid'] == 1]['dose2'].astype(int).to_list())])
vCountOverallStDf = pd.DataFrame(vCountOverallStList, columns=['stateid','overallid','dose1','dose2']).sort_values(by=['stateid','overallid']).reset_index(drop=True)
vCountOverallStDf


# Generating output CSV files for every week, month and overall for every district and state
vCountWeekDf.to_csv('district-vaccinated-count-week.csv', index=False)
vCountMonthDf.to_csv('district-vaccinated-count-month.csv', index=False)
vCountOverallDf.to_csv('district-vaccinated-count-overall.csv', index=False)
vCountWeekStDf.to_csv('state-vaccinated-count-week.csv', index=False)
vCountMonthStDf.to_csv('state-vaccinated-count-month.csv', index=False)
vCountOverallStDf.to_csv('state-vaccinated-count-overall.csv', index=False)