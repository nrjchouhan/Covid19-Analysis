#!/usr/bin/env python
# coding: utf-8


#Importing libraries
import pandas as pd
import numpy as np
import datetime as dt

# Reading cowin_vaccine_data_districtwise.csv file into vaccine_data DataFrame and making some modifications as per census data
vaccine_data = pd.read_csv('input/cowin_vaccine_data_districtwise.csv')
vaccine_data = vaccine_data[vaccine_data['S No']>0]
vaccine_data['State'] = vaccine_data['State'].str.upper()
vaccine_data['State'] = vaccine_data['State'].str.replace(' AND ',' & ')
vaccine_data['District'] = vaccine_data['District'].str.replace(' and ',' & ')
vaccine_data['District_Key'] = vaccine_data['District_Key'].str.replace(' and ',' & ')

# Last week is 8 aug'2021 to 14 aug'2021
# Extracting total number of vaccinated persons before and after last week for each district into vaccineDf DataFrame
vaccineDf = vaccine_data[['State','District_Key','District','07/08/2021.3','14/08/2021.3']]
vaccineDf = vaccineDf.rename(columns={'State':'stateid','07/08/2021.3':'VaccinatedBeforeLastWeek','14/08/2021.3':'VaccinatedAfterLastWeek'})
vaccineDf = vaccineDf.astype({'VaccinatedBeforeLastWeek':int, 'VaccinatedAfterLastWeek':int})

# Extracting total number of vaccinated persons before and after last week for each state into vaccineStDf DataFrame
vaccineStDf = vaccineDf[['stateid','VaccinatedBeforeLastWeek','VaccinatedAfterLastWeek']]
vaccineStDf = vaccineStDf.groupby('stateid').sum().reset_index()

# Calculating vaccinated persons in last week and keeping into 'VaccinatedInLastWeek' column
vaccineStDf['VaccinatedInLastWeek'] = vaccineStDf['VaccinatedAfterLastWeek'] - vaccineStDf['VaccinatedBeforeLastWeek']

# Calculating rate of vaccination in last week and keeping into 'rateofvaccination' column
vaccineStDf['rateofvaccination'] = vaccineStDf['VaccinatedInLastWeek']/7


# Reading census population 2011 data from excel file into census_data DataFrame
census_data = pd.read_excel('input/DDW_PCA0000_2011_Indiastatedist.xlsx')

# Creating dictionary of districts where mapping is from incorrect spelling of districts in census data to correct spelling
spellingCorrectionDist = {
    'Mahbubnagar':'Mahabubnagar',
    'Rangareddy':'Ranga Reddy',
    'Sri Potti Sriramulu Nellore':'S.P.S. Nellore',
    'Y.S.R.':'Y.S.R. Kadapa',
    'Dibang Valley':'Upper Dibang Valley',
    'Kaimur (Bhabua)':'Kaimur',
    'Pashchim Champaran':'West Champaran',
    'Purba Champaran':'East Champaran',
    'Janjgir - Champa':'Janjgir Champa',
    'Ahmadabad':'Ahmedabad',
    'Banas Kantha':'Banaskantha',
    'Dohad':'Dahod',
    'Kachchh':'Kutch',
    'Mahesana':'Mehsana',
    'Panch Mahals':'Panchmahal',
    'Sabar Kantha':'Sabarkantha',
    'The Dangs':'Dang',
    'Lahul & Spiti':'Lahaul & Spiti',
    'Gurgaon':'Gurugram',
    'Mewat':'Nuh',
    'Kodarma':'Koderma',
    'Pashchimi Singhbhum':'West Singhbhum',
    'Purbi Singhbhum':'East Singhbhum',
    'SaraikelaKharsawan':'',
    'Badgam':'Budgam',
    'Bandipore':'Bandipora',
    'Baramula':'Baramulla',
    'Shupiyan':'Shopiyan',
    'Bagalkot':'Bagalkote',
    'Bangalore':'Bengaluru',
    'Bangalore Rural':'Bengaluru Rural',
    'Belgaum':'Belagavi',
    'Bellary':'Ballari',
    'Bijapur':'Vijayapura',
    'Chamarajanagar':'Chamarajanagara',
    'Chikmagalur':'Chikkamagaluru',
    'Gulbarga':'Kalaburagi',
    'Mysore':'Mysuru',
    'Shimoga':'Shivamogga',
    'Tumkur':'Tumakuru',
    'Ahmadnagar':'Ahmednagar',
    'Bid':'Beed',
    'Buldana':'Buldhana',
    'Gondiya':'Gondia',
    'Khandwa (East Nimar)':'Khandwa',
    'Khargone (West Nimar)':'Khargone',
    'Narsimhapur':'Narsinghpur',
    'Anugul':'Angul',
    'Baleshwar':'Balasore',
    'Baudh':'Boudh',
    'Debagarh':'Deogarh',
    'Jagatsinghapur':'Jagatsinghpur',
    'Jajapur':'Jajpur',
    'Firozpur':'Ferozepur',
    'Muktsar':'Sri Muktsar Sahib',
    'Sahibzada Ajit Singh Nagar':'S.A.S. Nagar',
    'Chittaurgarh':'Chittorgarh',
    'Dhaulpur':'Dholpur',
    'Jalor':'Jalore',
    'Jhunjhunun':'Jhunjhunu',
    'Kanniyakumari':'Kanyakumari',
    'The Nilgiris':'Nilgiris',
    'Allahabad':'Prayagraj',
    'Bara Banki':'Barabanki',
    'Faizabad':'Ayodhya',
    'Jyotiba Phule Nagar':'Amroha',
    'Kanshiram Nagar':'Kasganj',
    'Kheri':'Lakhimpur Kheri',
    'Mahamaya Nagar':'Hathras',
    'Mahrajganj':'Maharajganj',
    'Sant Ravidas Nagar (Bhadohi)':'Bhadohi',
    'Garhwal':'Pauri Garhwal',
    'Hardwar':'Haridwar',
    'Darjiling':'Darjeeling',
    'Haora':'Howrah',
    'Hugli':'Hooghly',
    'Koch Bihar':'Cooch Behar',
    'Maldah':'Malda',
    'North Twenty Four Parganas':'North 24 Parganas',
    'Puruliya':'Purulia',
    'South Twenty Four Parganas':'South 24 Parganas'
}

# Extracting required column from census_data DataFrame into populationDf DataFrame which contains total population of female and male for each district
populationDf = census_data[['State','Level','Name','TRU','TOT_F','TOT_M']]
populationDf = populationDf[(populationDf['TRU']=='Total')].drop(['TRU'], axis=1)


# Updating populationDf DataFrame and correcting spellings using spellingCorrectionDist dictionary
for cd in spellingCorrectionDist.keys():
    cdIndex = populationDf[populationDf['Name'] == cd].index
    populationDf.at[cdIndex,'Name'] = spellingCorrectionDist[cd]

# Merging 'DADRA & NAGAR HAVELI' and 'DAMAN & DIU' states in populationDf DataFrame
DmnDiuIndex = populationDf[populationDf['Name'] == 'DAMAN & DIU'].index
populationDf.at[DmnDiuIndex,'Name'] = 'DADRA & NAGAR HAVELI & DAMAN & DIU'
populationDf.at[DmnDiuIndex,'TOT_F'] = 242895
populationDf.at[DmnDiuIndex,'TOT_M'] = 344061
DNHDistIndex = populationDf[populationDf['Name'] == 'Dadra & Nagar Haveli'].index
populationDf.at[DNHDistIndex,'State'] = 25
DNHStIndex = populationDf[populationDf['Name'] == 'DADRA & NAGAR HAVELI'].index
populationDf.drop(DNHStIndex, inplace=True)

# Merging 'Mumbai' and 'Mumbai Suburban' district in populationDf DataFrame
MumIndex = populationDf[populationDf['Name'] == 'Mumbai'].index
populationDf.at[MumIndex,'TOT_F'] = 5726442
populationDf.at[MumIndex,'TOT_M'] = 6715931
MumSubIndex = populationDf[populationDf['Name'] == 'Mumbai Suburban'].index
populationDf.drop(MumSubIndex, inplace=True)

# Updating districts and state data as per vaccine data in populationDf DataFrame
LadakhRow = {'State':26, 'Level':'STATE', 'Name':'LADAKH', 'TOT_F':117533 ,'TOT_M':156756}
populationDf = populationDf.append(LadakhRow, ignore_index=True)
JKIndex = populationDf[populationDf['Name'] == 'JAMMU & KASHMIR'].index
populationDf.at[JKIndex,'TOT_F'] = 5783107
populationDf.at[JKIndex,'TOT_M'] = 6483906
kargilIndex = populationDf[populationDf['Name'] == 'Kargil'].index
LehIndex = populationDf[populationDf['Name'] == 'Leh(Ladakh)'].index
populationDf.at[kargilIndex,'State'] = 26
populationDf.at[LehIndex,'State'] = 26
populationDf.at[LehIndex,'Name'] = 'Leh'

DehliIndex = populationDf[populationDf['Name'] == 'NCT OF DELHI'].index
populationDf.at[DehliIndex,'Name'] = 'DELHI'
NewDehliIndex = populationDf[populationDf['Name'] == 'New Delhi'].index
populationDf.at[NewDehliIndex,'Name'] = 'New'
delhiDistDf = populationDf[populationDf['State']==7]['Name'].index.to_list()
delhiDistDf.pop(0)
for dl in delhiDistDf:
    populationDf.at[dl,'Name'] = populationDf.at[dl,'Name'] + ' Delhi'

populationDf = populationDf.sort_values(by='State').reset_index(drop=True)



# Extracting required column into vaccineDf DataFrame. Merging common district keys and adding their respective data
vaccineDf = vaccineDf[['District_Key','VaccinatedBeforeLastWeek','VaccinatedAfterLastWeek','stateid','District']]
StDistDf = vaccineDf[['District_Key','stateid','District']].drop_duplicates().set_index('District_Key')
vaccineDf = vaccineDf.drop(['stateid','District'], axis=1)
vaccineDf = vaccineDf.groupby('District_Key').sum()
vaccineDf = pd.concat([vaccineDf,StDistDf], axis=1).reset_index()


# Merging urban and rural districts and adding their respective into UrbanRuralDf DataFrame
UrbanRuralDf = vaccineDf[(vaccineDf['District'].str.contains('Urban')) | 
                         (vaccineDf['District'].str.contains('Rural')) | 
                         (vaccineDf['District'].str.contains('Jaintia')) | 
                         (vaccineDf['District'].str.contains('Bardhaman'))]
UrbanRuralDf.iat[1,0] = 'KA_Bengaluru'
UrbanRuralDf.iat[1,4] = 'Bengaluru'
UrbanRuralDf.iat[2,0] = 'ML_Jaintia Hills'
UrbanRuralDf.iat[2,4] = 'Jaintia Hills'
UrbanRuralDf.iat[4,0] = 'TG_Warangal'
UrbanRuralDf.iat[4,4] = 'Warangal'
UrbanRuralDf.iat[6,0] = 'WB_Barddhaman'
UrbanRuralDf.iat[6,4] = 'Barddhaman'
UrbanRuralDf.iat[2,1] = UrbanRuralDf.iat[2,1]+UrbanRuralDf.iat[3,1]
UrbanRuralDf.iat[2,2] = UrbanRuralDf.iat[2,2]+UrbanRuralDf.iat[3,2]
UrbanRuralDf.iat[4,1] = UrbanRuralDf.iat[4,1]+UrbanRuralDf.iat[5,1]
UrbanRuralDf.iat[4,2] = UrbanRuralDf.iat[4,2]+UrbanRuralDf.iat[5,2]
UrbanRuralDf.iat[6,1] = UrbanRuralDf.iat[6,1]+UrbanRuralDf.iat[7,1]
UrbanRuralDf.iat[6,2] = UrbanRuralDf.iat[6,2]+UrbanRuralDf.iat[7,2]
UrbanRuralDf.drop([359,571,724], inplace=True)

# Removing urban and rural district entries and appending UrbanRuralDf DataFrame rows to vaccineDf DataFrame
vaccineDf.drop([271,272,351,359,570,571,722,724], inplace=True)
vaccineDf = pd.concat([vaccineDf,UrbanRuralDf]).sort_values(by='District_Key').reset_index(drop=True)



# Telangana state is not in census population data. Some of the Andhra Pradesh districts brought in Telangana
# Adding Telangana state in populationDf DataFrame and making changes accordingly
telanganaDistList = vaccineDf[vaccineDf['stateid']=='TELANGANA']['District'].to_list()
telanganaFCount = 0
telanganaMCount = 0
for td in telanganaDistList:
    tdIndex = populationDf[populationDf['Name'] == td].index
    if tdIndex.values:
        populationDf.at[tdIndex,'State'] = 36
        telanganaFCount += populationDf.at[tdIndex[0],'TOT_F']
        telanganaMCount += populationDf.at[tdIndex[0],'TOT_M']

telanganaRow = {'State':36, 'Level':'STATE', 'Name':'TELANGANA', 'TOT_F':telanganaFCount ,'TOT_M':telanganaMCount}
populationDf = populationDf.append(telanganaRow, ignore_index=True)

APIndex = populationDf[populationDf['Name'] == 'ANDHRA PRADESH'].index
populationDf.at[APIndex,'TOT_F'] = populationDf.at[APIndex[0],'TOT_F'] - telanganaFCount
populationDf.at[APIndex,'TOT_M'] = populationDf.at[APIndex[0],'TOT_M'] - telanganaMCount

populationDf = populationDf.sort_values(by='State').reset_index(drop=True)


# Extracting state data from populationDf DataFrame into populationDf DataFrame which contains total population of female and male
populationDf = populationDf[(populationDf['State']>0) & (populationDf['Level'] =='STATE')]
populationDf = populationDf.drop(['State','Level'], axis=1)
populationDf = populationDf.rename(columns={'Name':'stateid'}).sort_values(by='stateid').reset_index(drop=True)

# Adding female and male population to get total population for each state
populationDf['Total_Population'] = populationDf['TOT_F'] + populationDf['TOT_M']
populationDf = populationDf[['stateid','Total_Population']]



# Combining vaccineStDf and populationStDf DataFrame into VPStateDf DataFrame
VPStateDf = pd.concat([vaccineStDf.set_index('stateid'), populationDf.set_index('stateid')], axis=1).reset_index()

# Calculating population left for vaccination using (total population - total vaccinated after last week)
VPStateDf['populationleft'] = VPStateDf['Total_Population'] - VPStateDf['VaccinatedAfterLastWeek']
VPStateDf = VPStateDf[['stateid','populationleft','rateofvaccination']]
# Replacing negative values in population left to zero
VPStateDf1 = VPStateDf._get_numeric_data()
VPStateDf1[VPStateDf1<0] = 0

# Calculating days needed for left population to get vaccinated with at least one dose using (population left/rate of vaccination)
VPStateDf['DaysNeeded'] = VPStateDf['populationleft']/VPStateDf['rateofvaccination']
VPStateDf['DaysNeeded'] = VPStateDf['DaysNeeded'].apply(np.ceil).astype(int)

#last date of last week 14 aug'2021
lastDate = dt.datetime.strptime('2021-08-14','%Y-%m-%d')

# Calculating 'date' column in VPStateDf DataFrame contains date on which entire population will get at least one dose of vaccination for each state
DateList = []
for day in VPStateDf['DaysNeeded'].to_list():
    lastDate += dt.timedelta(days = day)
    DateList.append(lastDate)
    lastDate = dt.datetime.strptime('2021-08-14','%Y-%m-%d')
VPStateDf.drop('DaysNeeded', axis=1, inplace=True)
VPStateDf = pd.concat([VPStateDf,pd.DataFrame(DateList, columns=['date'])], axis=1)


# Generating output CSV files for every state from VPStateDf DataFrame
VPStateDf.to_csv('complete-vaccination.csv', index=False)

