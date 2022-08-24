#!/usr/bin/env python
# coding: utf-8


# Importing libraries
import pandas as pd
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

# Reading covid cases data till 26 Apr'2020 from raw_data1.csv and raw_data2.csv file into cases_till_26apr DataFrame
cases_till_26apr = pd.concat([pd.read_csv('input/raw_data1.csv'),pd.read_csv('input/raw_data2.csv')])
# Converting 'Date Announced' column datatype to datetime
cases_till_26apr['Date Announced'] = pd.to_datetime(cases_till_26apr['Date Announced'])

# Extracting covid cases data between 15 mar'2020 and 25 apr'2020 from above DataFrame
cases_15marTo25apr = cases_till_26apr[(cases_till_26apr['Notes'] != 'Correction for district count') & 
                                      (cases_till_26apr['Date Announced'] > '2020-03-14') & 
                                      (cases_till_26apr['Date Announced'] < '2020-04-26')
                                     ].sort_values(by='Date Announced').dropna(subset=['Detected District']).reset_index(drop=True)

# Extracting required column from above DataFrame
cases_15marTo25apr = cases_15marTo25apr[['Date Announced','Detected State','State code','Detected District','Num Cases']]

# Creating 'District_Key' column by concating state code and district name with '_' and inserting into above DataFrame
cases_15marTo25apr['District_Key'] = cases_15marTo25apr['State code'] + '_' + cases_15marTo25apr['Detected District']

# Creating DataFrame contains number of cases found for each district on each date between 15 mar'2020 and 25 apr'2020
cases_15marTo25apr_list = []
for da in cases_15marTo25apr['Date Announced'].drop_duplicates().dt.date.to_list():
    daDF = cases_15marTo25apr[cases_15marTo25apr['Date Announced'].dt.date == da]
    daCount_dict = dict(daDF['District_Key'].value_counts())
    for dist in daCount_dict.keys():
        cases_15marTo25apr_list.append([dist, da, daCount_dict[dist]])
cases_15marTo25apr_DF = pd.DataFrame(cases_15marTo25apr_list, columns=['District_Key','Date','Cases_Found'])
cases_15marTo25apr_DF['Date'] = pd.to_datetime(cases_15marTo25apr_DF['Date'])

# List of state code for cases_data DataFrame
st_code = []
for st in cases_data['State'].to_list():
    st_code.append(state_code_dict[st])

# Instering list of state code as 'State_Code' column in cases_data DataFrame
cases_data.insert(2, 'State_Code', st_code)
# Creating 'District_Key' column by concating state code and district name with '_' and inserting into above DataFrame
cases_data['District_Key'] = cases_data['State_Code'] + '_' + cases_data['District']

# Extracting required column from above DataFrame
cases_from_26aprDF = cases_data[['District_Key','Date','Confirmed']]
cases_from_26aprDF['Date'] = pd.to_datetime(cases_from_26aprDF['Date'])

# Combining all districts and creating list of districts
dist_15marTo25apr = cases_15marTo25apr_DF['District_Key'].drop_duplicates().to_list()
dist_from_26apr = cases_from_26aprDF['District_Key'].drop_duplicates().to_list()
districtList = [d for d in dist_from_26apr if d not in dist_15marTo25apr]
districtList += dist_15marTo25apr

# Creating DataFrame contains number of cases found per week for each district between 15 mar'2020 and 25 apr'2020 
weekly_cases1 = []
for dist in districtList:
    distDF = cases_15marTo25apr_DF[cases_15marTo25apr_DF['District_Key'] == dist]
    start_dt = dt.datetime.strptime('2020-03-15','%Y-%m-%d')
    end_dt = dt.datetime.strptime('2020-03-21','%Y-%m-%d')
    for i in range(6):
        cases_count = sum(distDF[(distDF['Date'] >= start_dt) & (distDF['Date'] <= end_dt)]['Cases_Found'].to_list())
        start_dt += dt.timedelta(days=7)
        end_dt += dt.timedelta(days=7)
        weekly_cases1.append([dist, i+1, cases_count])

week_cases1_DF = pd.DataFrame(weekly_cases1, columns=['districtid','weekid','cases'])

# Creating DataFrame contains number of cases found per week for each district between 26 apr'2020 to 14 aug'2021
weekly_cases2 = []
for dist in districtList:
    distDF = cases_from_26aprDF[cases_from_26aprDF['District_Key'] == dist]
    start_dt = dt.datetime.strptime('2020-04-25','%Y-%m-%d')
    end_dt = dt.datetime.strptime('2020-05-02','%Y-%m-%d')
    if start_dt == '2020-04-25':
        week6Df = week_cases1_DF[week_cases1_DF['districtid'] == dist][cases]
        week6 = 0 if week6DF.empty else sum(week6Df.to_list())
        distDF.loc[len(distDF.index)] = [dist, start_dt, week6]
    
    for i in range(68):
        cc = 0
        week_list = distDF[(distDF['Date'] >= start_dt) & (distDF['Date'] <= end_dt)]['Confirmed'].to_list()
        if week_list:
            for c in range(len(week_list)-1):
                dc = week_list[c+1] - week_list[c]
                cc += dc if dc >= 0 else 0
        
        start_dt += dt.timedelta(days=7)
        end_dt += dt.timedelta(days=7)
        weekly_cases2.append([dist, i+7, cc])

week_cases2_DF = pd.DataFrame(weekly_cases2, columns=['districtid','weekid','cases'])

# Combining week_cases1_DF and week_cases2_DF into cases_week DataFrame
cases_week = pd.concat([week_cases1_DF, week_cases2_DF]).sort_values(by=['districtid','weekid']).reset_index(drop=True)


# Creating DataFrame contains number of cases found per month for each district between 15 mar'2020 and 25 apr'2020 
monthly_cases1 = []
for dist in districtList:
    distDF = cases_15marTo25apr_DF[cases_15marTo25apr_DF['District_Key'] == dist]
    start_dt = dt.datetime.strptime('2020-03-15','%Y-%m-%d')
    end_dt = dt.datetime.strptime('2020-04-14','%Y-%m-%d')
    monthly_cases1.append([dist, 1, sum(distDF[(distDF['Date'] >= start_dt) & (distDF['Date'] <= end_dt)]['Cases_Found'].to_list())])

month_cases1_DF = pd.DataFrame(monthly_cases1, columns=['districtid','monthid','cases'])
month_cases1_DF

# Creating DataFrame contains number of cases found per month for each district between 26 apr'2020 to 14 aug'2021
monthly_cases2 = []
for dist in districtList:
    distDF = cases_from_26aprDF[cases_from_26aprDF['District_Key'] == dist]
    start_dt = dt.datetime.strptime('2020-04-14','%Y-%m-%d')
    end_dt = dt.datetime.strptime('2020-05-14','%Y-%m-%d')
    if start_dt == '2020-04-14':
        month1Df = cases_15marTo25apr_DF[(cases_15marTo25apr_DF['districtid'] == dist) & 
                                         (cases_15marTo25apr_DF['Date'] >= '2020-03-15') & 
                                         (cases_15marTo25apr_DF['Date'] <= '2020-04-14')]['Cases_Found']
        m1 = 0 if month1Df.empty else sum(month1Df.to_list())
        distDF.loc[len(distDF.index)] = [dist, start_dt, m1]
        month2Df = cases_15marTo25apr_DF[(cases_15marTo25apr_DF['districtid'] == dist) & 
                                         (cases_15marTo25apr_DF['Date'] >= '2020-03-15') & 
                                         (cases_15marTo25apr_DF['Date'] <= '2020-04-25')]['Cases_Found']
        m2 = 0 if month2Df.empty else sum(month2Df.to_list())
        distDF.loc[len(distDF.index)] = [dist, '2020-04-25', m2]
    
    for i in range(16):
        cc = 0
        m_list = distDF[(distDF['Date'] >= start_dt) & (distDF['Date'] <= end_dt)]['Confirmed'].to_list()
        if m_list:
            for c in range(len(m_list)-1):
                dc = m_list[c+1] - m_list[c]
                cc += dc if dc >= 0 else 0
        
        start_dt += relativedelta(months = +1)
        end_dt += relativedelta(months = +1)
        monthly_cases2.append([dist, i+2, cc])

month_cases2_DF = pd.DataFrame(monthly_cases2, columns=['districtid','monthid','cases'])

# Combining month_cases1_DF and month_cases2_DF into cases_month DataFrame
cases_month = pd.concat([month_cases1_DF, month_cases2_DF]).sort_values(by=['districtid','monthid']).reset_index(drop=True)


# Creating DataFrame contains number of cases found in overall duration between 15 mar'2020 to 14 aug'2021 for each district
overall_cases = []
for dist in districtList:
    distDF = cases_month[cases_month['districtid'] == dist]
    overall_cases.append([dist, 1, sum(distDF['cases'].to_list())])

cases_overall = pd.DataFrame(overall_cases, columns=['districtid','overallid','cases']).sort_values(by='districtid')


# Generating output cases-week.csv file from cases_week DataFrame
cases_week.to_csv('cases-week.csv', index=False)

# Generating output cases-month.csv file from cases_month DataFrame
cases_month.to_csv('cases-month.csv', index=False)

# Generating output cases-overall.csv file from cases_overall DataFrame
cases_overall.to_csv('cases-overall.csv', index=False)

