#!/usr/bin/env python
# coding: utf-8


#Importing libraries
import pandas as pd
import numpy as np
import datetime as dt
from dateutil.relativedelta import relativedelta

# Reading cowin_vaccine_data_districtwise.csv file into vaccine_data DataFrame
vaccine_data = pd.read_csv('input/cowin_vaccine_data_districtwise.csv')
vaccine_data = vaccine_data[vaccine_data['S No'] > 0]

# Dictionary of mapping of state and state code - sample entry: 'Madhya Pradesh': 'MP'
state_code_dict = vaccine_data[['State','State_Code']].drop_duplicates().set_index('State').T.to_dict('list')
state_code_dict = dict(zip(list(state_code_dict),[l[0] for l in list(state_code_dict.values())]))

# Reading covid cases data from districts.csv file into cases_data DataFrame. It contains cases data from 26 apr'2020
cases_data = pd.read_csv('input/districts.csv')
# Removing Unknown and unwanted districts from above DataFrame
cases_data = cases_data[(cases_data['District'] != 'Unknown') &
                        (cases_data['District'] != 'Other State') &
                        (cases_data['District'] != 'Other Region') &
                        (cases_data['District'] != 'Evacuees') &
                        (cases_data['District'] != 'Foreign Evacuees') &
                        (cases_data['District'] != 'State Pool') &
                        (cases_data['District'] != 'Foreign Evacuees') &
                        (cases_data['District'] != 'Capital Complex')].reset_index(drop=True)


# List of state code for cases_data DataFrame
st_code = []
for st in cases_data['State'].to_list():
    st_code.append(state_code_dict[st])

# Instering list of state code as 'State_Code' column in cases_data DataFrame
cases_data.insert(2, 'State_Code', st_code)
# Creating 'District_Key' column by concating state code and district name with '_' and inserting into above DataFrame
cases_data['District_Key'] = cases_data['State_Code'] + '_' + cases_data['District']

# Extracting required column from above DataFrame
cases_DF = cases_data[['District_Key','Date','Confirmed','Recovered','Deceased']]
cases_DF['Date'] = pd.to_datetime(cases_DF['Date'])

# List of districts
districtList = cases_DF['District_Key'].drop_duplicates().to_list()



# Creating DataFrame contains number of active cases per week for each district between 15 mar'2020 and 14 aug'2021
weekly_cases = []
for dist in districtList:
    distDF = cases_DF[cases_DF['District_Key'] == dist]
    # w1 indicates week from sunday to saturday
    w1start_dt = dt.datetime.strptime('2020-03-15','%Y-%m-%d')
    w1end_dt = dt.datetime.strptime('2020-03-21','%Y-%m-%d')
    # w2 indicates week from thrusday to wednesday
    w2start_dt = dt.datetime.strptime('2020-03-19','%Y-%m-%d')
    w2end_dt = dt.datetime.strptime('2020-03-25','%Y-%m-%d')
    # flag runs w1 and w2 alternatively
    flag = True
    for i in range(148):
        cc = 0
        week_DF = pd.DataFrame()
        if flag:
            week_DF = distDF[(distDF['Date'] >= w1start_dt) & (distDF['Date'] <= w1end_dt)]
            w1start_dt += dt.timedelta(days=7)
            w1end_dt += dt.timedelta(days=7)
            flag = False
        else:
            week_DF = distDF[(distDF['Date'] >= w2start_dt) & (distDF['Date'] <= w2end_dt)]
            w2start_dt += dt.timedelta(days=7)
            w2end_dt += dt.timedelta(days=7)
            flag = True
        confirmedList = week_DF['Confirmed'].to_list()
        recoveredList = week_DF['Recovered'].to_list()
        deceasedList = week_DF['Deceased'].to_list()
        # Calculating active number of cases using Confirmed - Recovered - Death
        week_list = [confirmedList[l] - recoveredList[l] - deceasedList[l] for l in range(len(confirmedList))]
        if week_list:
            cc = round(np.mean(week_list))
        
        weekly_cases.append([dist, i+1, cc])

week_cases_DF = pd.DataFrame(weekly_cases, columns=['districtid','timeid','cases']).sort_values(by=['districtid','timeid']).reset_index(drop=True)


# Creating DataFrame contains number of active cases per month for each district between 15 mar'2020 and 14 aug'2021
monthly_cases = []
for dist in districtList:
    distDF = cases_DF[cases_DF['District_Key'] == dist]
    start_dt = dt.datetime.strptime('2020-03-15','%Y-%m-%d')
    end_dt = dt.datetime.strptime('2020-04-14','%Y-%m-%d')
        
    for i in range(17):
        cc = 0
        m_DF = distDF[(distDF['Date'] >= start_dt) & (distDF['Date'] <= end_dt)]
        confirmedList = m_DF['Confirmed'].to_list()
        recoveredList = m_DF['Recovered'].to_list()
        deceasedList = m_DF['Deceased'].to_list()
        # Calculating active number of cases using Confirmed - Recovered - Death
        m_list = [confirmedList[l] - recoveredList[l] - deceasedList[l] for l in range(len(confirmedList))]
        if m_list:
            cc = round(np.mean(m_list))
        
        start_dt += relativedelta(months = +1)
        end_dt += relativedelta(months = +1)
        monthly_cases.append([dist, i+1, cc])

month_cases_DF = pd.DataFrame(monthly_cases, columns=['districtid','timeid','cases']).sort_values(by=['districtid','timeid']).reset_index(drop=True)


# Creating DataFrame contains timeid for wave-1 and wave-2 having peak initialized with zero for each district
peakDistList = []
for d in districtList:
    peakDistList.append([d, 0, 0, 0, 0])
peaksDistDF = pd.DataFrame(peakDistList, columns=['districtid','wave1-weekid','wave2-weekid','wave1-monthid','wave2-monthid']).sort_values(by='districtid').reset_index(drop=True)

# Calculating timeid for wave-1 and wave-2 peaks and updating entries in above DataFrame
for d in districtList:
    w1w = week_cases_DF.iloc[week_cases_DF[(week_cases_DF['districtid'] == d) & (week_cases_DF['timeid'] < 80)]['cases'].idxmax()]['timeid']
    peaksDistDF.at[peaksDistDF[peaksDistDF['districtid'] == d].index,'wave1-weekid'] = w1w if w1w !=1 else np.NAN
    w2w = week_cases_DF.iloc[week_cases_DF[(week_cases_DF['districtid'] == d) & (week_cases_DF['timeid'] >= 80)]['cases'].idxmax()]['timeid']
    peaksDistDF.at[peaksDistDF[peaksDistDF['districtid'] == d].index,'wave2-weekid'] = w2w if w2w !=80 else np.NAN
    w1m = month_cases_DF.iloc[month_cases_DF[(month_cases_DF['districtid'] == d) & (month_cases_DF['timeid'] < 10)]['cases'].idxmax()]['timeid']
    peaksDistDF.at[peaksDistDF[peaksDistDF['districtid'] == d].index,'wave1-monthid'] = w1m if w1m !=1 else np.NAN
    w2m = month_cases_DF.iloc[month_cases_DF[(month_cases_DF['districtid'] == d) & (month_cases_DF['timeid'] >= 10)]['cases'].idxmax()]['timeid']
    peaksDistDF.at[peaksDistDF[peaksDistDF['districtid'] == d].index,'wave2-monthid'] = w2m if w2m !=10 else np.NAN



# Creating DataFrame contains number of active cases per week for each state between 15 mar'2020 and 14 aug'2021
weekly_cases_st = []
for st in state_code_dict.keys():
    stDF = week_cases_DF.loc[week_cases_DF['districtid'].str.contains(state_code_dict[st])]
    for w in range(1,149):
        weekly_cases_st.append([st, w, sum(stDF[stDF['timeid'] == w]['cases'].to_list())])
week_cases_stDF = pd.DataFrame(weekly_cases_st, columns=['stateid','timeid','cases']).sort_values(by=['stateid','timeid']).reset_index(drop=True)

# Creating DataFrame contains number of active cases per month for each state between 15 mar'2020 and 14 aug'2021
monthly_cases_st = []
for st in state_code_dict.keys():
    stDF = month_cases_DF.loc[month_cases_DF['districtid'].str.contains(state_code_dict[st])]
    for m in range(1,18):
        monthly_cases_st.append([st, m, sum(stDF[stDF['timeid'] == m]['cases'].to_list())])
month_cases_stDF = pd.DataFrame(monthly_cases_st, columns=['stateid','timeid','cases']).sort_values(by=['stateid','timeid']).reset_index(drop=True)

# Creating DataFrame contains timeid for wave-1 and wave-2 having peak initialized with zero for each state
peakStList = []
for st in state_code_dict.keys():
    peakStList.append([st, 0, 0, 0, 0])
peaksStDF = pd.DataFrame(peakStList, columns=['stateid','wave1-weekid','wave2-weekid','wave1-monthid','wave2-monthid']).sort_values(by='stateid').reset_index(drop=True)

# Calculating timeid for wave-1 and wave-2 peaks and updating entries in above DataFrame
for st in state_code_dict.keys():
    peaksStDF.at[peaksStDF[peaksStDF['stateid'] == st].index,'wave1-weekid'] = week_cases_stDF.iloc[week_cases_stDF[(week_cases_stDF['stateid'] == st) & (week_cases_stDF['timeid'] < 80)]['cases'].idxmax()]['timeid']
    peaksStDF.at[peaksStDF[peaksStDF['stateid'] == st].index,'wave2-weekid'] = week_cases_stDF.iloc[week_cases_stDF[(week_cases_stDF['stateid'] == st) & (week_cases_stDF['timeid'] >= 80)]['cases'].idxmax()]['timeid']
    peaksStDF.at[peaksStDF[peaksStDF['stateid'] == st].index,'wave1-monthid'] = month_cases_stDF.iloc[month_cases_stDF[(month_cases_stDF['stateid'] == st) & (month_cases_stDF['timeid'] < 10)]['cases'].idxmax()]['timeid']
    peaksStDF.at[peaksStDF[peaksStDF['stateid'] == st].index,'wave2-monthid'] = month_cases_stDF.iloc[month_cases_stDF[(month_cases_stDF['stateid'] == st) & (month_cases_stDF['timeid'] >= 10)]['cases'].idxmax()]['timeid']



# Creating DataFrame contains number of active cases per week for overall duration from 15 mar'2020 to 14 aug'2021
weekly_cases_overall = []
for w in range(1,149):
    weekly_cases_overall.append(['India', w, sum(week_cases_stDF[week_cases_stDF['timeid'] == w]['cases'].to_list())])
week_cases_overallDF = pd.DataFrame(weekly_cases_overall, columns=['overallid','timeid','cases']).sort_values(by='timeid').reset_index(drop=True)

# Creating DataFrame contains number of active cases per month for overall duration from 15 mar'2020 to 14 aug'2021
monthly_cases_overall = []
for m in range(1,18):
    monthly_cases_overall.append(['India', m, sum(month_cases_stDF[month_cases_stDF['timeid'] == m]['cases'].to_list())])
month_cases_overallDF = pd.DataFrame(monthly_cases_overall, columns=['overallid','timeid','cases']).sort_values(by='timeid').reset_index(drop=True)
month_cases_overallDF

# Calculating timeid for wave-1 and wave-2 peaks for overall duration from 15 mar'2020 to 14 aug'2021
wave1weekid = week_cases_overallDF.iloc[week_cases_overallDF[week_cases_overallDF['timeid'] < 80]['cases'].idxmax()]['timeid']
wave2weekid = week_cases_overallDF.iloc[week_cases_overallDF[week_cases_overallDF['timeid'] >= 80]['cases'].idxmax()]['timeid']
wave1monthid = month_cases_overallDF.iloc[month_cases_overallDF[month_cases_overallDF['timeid'] < 10]['cases'].idxmax()]['timeid']
wave2monthid = month_cases_overallDF.iloc[month_cases_overallDF[month_cases_overallDF['timeid'] >= 10]['cases'].idxmax()]['timeid']

# Creating DataFrame contains timeid for wave-1 and wave-2 having peak for overall duration from 15 mar'2020 to 14 aug'2021
peaksOverallList = ['India', wave1weekid, wave2weekid, wave1monthid, wave2monthid]
peaksOverallDF = pd.DataFrame([peaksOverallList], columns=['overallid','wave1-weekid','wave2-weekid','wave1-monthid','wave2-monthid'])

# Generating output CSV files for every district, state and overall from peaksDistDF, peaksStDF and peaksOverallDF DataFrame respectively
peaksDistDF.to_csv('district-peaks.csv', index=False)
peaksStDF.to_csv('state-peaks.csv', index=False)
peaksOverallDF.to_csv('overall-peaks.csv', index=False)

