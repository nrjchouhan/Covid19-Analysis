#!/usr/bin/env python
# coding: utf-8


#Importing libraries
import pandas as pd

# Reading cowin_vaccine_data_districtwise.csv file into vaccine_data DataFrame and making some modifications as per census data
vaccine_data = pd.read_csv('input/cowin_vaccine_data_districtwise.csv')
vaccine_data = vaccine_data[vaccine_data['S No']>0]
vaccine_data['State'] = vaccine_data['State'].str.upper()
vaccine_data['State'] = vaccine_data['State'].str.replace(' AND ',' & ')
vaccine_data['District'] = vaccine_data['District'].str.replace(' and ',' & ')
vaccine_data['District_Key'] = vaccine_data['District_Key'].str.replace(' and ',' & ')

# Extracting total number of female and male vaccinated for each district into vaccineDf DataFrame
vaccineDf = vaccine_data[['State','District_Key','District','14/08/2021.6','14/08/2021.5']]
vaccineDf = vaccineDf.rename(columns={'14/08/2021.6':'Female_Vaccinated','14/08/2021.5':'Male_Vaccinated'})
vaccineDf = vaccineDf.astype({'Female_Vaccinated':int, 'Male_Vaccinated':int})

# Merging common district keys and adding their respective female and male vaccinated data
StDistDf = vaccineDf[['District_Key','State','District']].drop_duplicates().set_index('District_Key')
vaccineDf = vaccineDf.drop(['State','District'], axis=1)
vaccineDf = vaccineDf.groupby('District_Key').sum()
vaccineDf = pd.concat([vaccineDf,StDistDf], axis=1).reset_index()

# Merging urban and rural districts and adding their respective female and male vaccinated data into UrbanRuralDf DataFrame
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

# Taking female to male vaccinated ratio for each district and keeping into vaccineRatioDistDf DataFrame
vaccineRatioDistDf = vaccineDf.copy()
vaccineRatioDistDf['Vaccination_Ratio'] = vaccineRatioDistDf['Female_Vaccinated']/vaccineRatioDistDf['Male_Vaccinated']

# Taking female to male vaccinated ratio for each state and keeping into vaccineRatioStDf DataFrame
vaccineRatioStDf = vaccineDf.drop(['District_Key','District'], axis=1)
vaccineRatioStDf = vaccineRatioStDf.groupby('State').sum()
vaccineRatioStDf = vaccineRatioStDf.reset_index()
vaccineRatioStDf['Vaccination_Ratio'] = vaccineRatioStDf['Female_Vaccinated']/vaccineRatioStDf['Male_Vaccinated']

# Taking female to male vaccinated ratio for overall country and keeping into vaccineRatioOverallDf DataFrame
vaccineRatioOverallDf = vaccineRatioStDf.copy()
vaccineRatioOverallDf = vaccineRatioOverallDf.drop(['State','Vaccination_Ratio'], axis=1)
vaccineRatioOverallDf.insert(loc=0, column='Country', value='India')
vaccineRatioOverallDf = vaccineRatioOverallDf.groupby('Country').sum()
vaccineRatioOverallDf['Vaccination_Ratio'] = vaccineRatioOverallDf['Female_Vaccinated']/vaccineRatioOverallDf['Male_Vaccinated']
vaccineRatioOverallDf = vaccineRatioOverallDf.reset_index()



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


# Telangana state is not in census population data. Some of the Andhra Pradesh districts brought in Telangana
# Adding Telangana state in populationDf DataFrame and making changes accordingly
telanganaDistList = vaccineDf[vaccineDf['State']=='TELANGANA']['District'].to_list()
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



# Dictionary of mapping of state and state code - sample entry: 'Madhya Pradesh': 'MP'
state_code_dict = vaccine_data[['State','State_Code']].drop_duplicates().set_index('State').T.to_dict('list')
state_code_dict = dict(zip(list(state_code_dict),[l[0] for l in list(state_code_dict.values())]))

# Extracting state number and state name from populationDf DataFrame into stateCensusDf DataFrame
stateCensusDf = populationDf[(populationDf['Level']=='STATE')].drop(['Level','TOT_F','TOT_M'], axis=1)


# Extracting district data from populationDf DataFrame into populationDistDf DataFrame which contains total population of female and male
populationDistDf = populationDf[(populationDf['State']>0) & (populationDf['Level']!='STATE')]
populationDistDf.drop('Level', axis=1, inplace=True)


# Replacing state number in 'State' column to state code in populationDistDf DataFrame using stateCensusDf DataFrame
populationDistDf['State'] = populationDistDf.State.astype(str)
for i in range(1,37):
    st_code = state_code_dict[stateCensusDf[stateCensusDf['State']==i]['Name'].values[0]]
    for indx in populationDistDf[populationDistDf['State'] == str(i)].index:
        populationDistDf.at[indx, 'State'] = st_code
populationDistDf = populationDistDf.reset_index(drop=True)

# Creating 'District_Key' column by concating state code and district name with '_' and inserting into populationDistDf DataFrame
populationDistDf['District_Key'] = populationDistDf['State'] + '_' + populationDistDf['Name']

# Making some changes in populationDistDf DataFrame as per vaccine data
populationDistDf['District_Key'] = populationDistDf['District_Key'].str.rstrip().replace('District', 'Sikkim', regex=True).replace({' +' : ' '}, regex=True)
populationDistDf.at[populationDistDf[populationDistDf['District_Key'] == 'MH_Raigarh'].index, 'District_Key'] = 'MH_Raigad'

# Dictionary of some remaining districts name to be replaced in census population data as per vaccine data
remainingDistDict = {
 'CT_Vijayapura':'CT_Bijapur',
 'GJ_Dohad':'GJ_Dahod',
 'HR_Mewat':'HR_Nuh',
 'KA_Bagalkot':'KA_Bagalkote',
 'OR_Anugul':'OR_Angul',
 'OR_Jagatsinghapur':'OR_Jagatsinghpur',
 'OR_Jajapur':'OR_Jajpur',
 'UP_Allahabad':'UP_Prayagraj',
 'WB_Darjiling':'WB_Darjeeling',
 'WB_Haora':'WB_Howrah',
 'WB_Hugli':'WB_Hooghly',
 'WB_Koch Bihar':'WB_Cooch Behar',
 'WB_Maldah':'WB_Malda'
}

# Updating populationDistDf DataFrame and correcting district names using remainingDistDict dictionary
for rd in remainingDistDict.keys():
    populationDistDf.at[populationDistDf[populationDistDf['District_Key'] == rd].index, 'District_Key'] = remainingDistDict[rd]
populationDistDf = populationDistDf.sort_values(by='District_Key').reset_index(drop=True)
populationDistDf = populationDistDf.rename(columns={'TOT_F':'Female_Population','TOT_M':'Male_Population'})


# distCensusList = populationDistDf['District_Key'].to_list()
# distVaccineList = vaccineDf['District_Key'].to_list()

# len([dist for dist in distCensusList if dist not in distVaccineList])
# 0
# len([dist for dist in distCensusList if dist in distVaccineList])
# 639


# Taking female to male population ratio for each district and keeping into populationRatioDistDf DataFrame
populationRatioDistDf = populationDistDf.copy()
populationRatioDistDf['Population_Ratio'] = populationRatioDistDf['Female_Population']/populationRatioDistDf['Male_Population']

# Taking female to male population ratio for each state and keeping into populationRatioStDf DataFrame
populationRatioStDf = populationRatioDistDf.drop(['Name','District_Key','Population_Ratio'], axis=1)
populationRatioStDf = populationRatioStDf.groupby('State').sum()
populationRatioStDf = populationRatioStDf.reset_index()
for k in state_code_dict.keys():
    indx = populationRatioStDf[populationRatioStDf['State'] == state_code_dict[k]].index
    populationRatioStDf.at[indx, 'State'] = k
populationRatioStDf['Population_Ratio'] = populationRatioStDf['Female_Population']/populationRatioStDf['Male_Population']

# Taking female to male population ratio for overall country and keeping into populationRatioOverallDf DataFrame
populationRatioOverallDf = populationRatioStDf.copy()
populationRatioOverallDf = populationRatioOverallDf.drop(['State','Population_Ratio'], axis=1)
populationRatioOverallDf.insert(loc=0, column='Country', value='India')
populationRatioOverallDf = populationRatioOverallDf.groupby('Country').sum()
populationRatioOverallDf['Population_Ratio'] = populationRatioOverallDf['Female_Population']/populationRatioOverallDf['Male_Population']
populationRatioOverallDf = populationRatioOverallDf.reset_index()


# Combining vaccineRatioDistDf and populationRatioDistDf DataFrame into VPRatioDist DataFrame
VPRatioDist = pd.concat([vaccineRatioDistDf[['District_Key','Vaccination_Ratio']].set_index('District_Key'), populationRatioDistDf[['District_Key','Population_Ratio']].set_index('District_Key')], axis=1).reset_index()

# Calculating Vaccination Ratio to Population Ratio and keeping into 'RatioOfRatios' column
VPRatioDist['RatioOfRatios'] = VPRatioDist['Vaccination_Ratio']/VPRatioDist['Population_Ratio']
VPRatioDist = VPRatioDist.rename(columns={'District_Key':'districtid','Vaccination_Ratio':'vaccinationratio','Population_Ratio':'populationratio','RatioOfRatios':'ratioofratios'})
VPRatioDist = VPRatioDist.dropna().sort_values(by='ratioofratios').reset_index(drop=True)


# Combining vaccineRatioStDf and populationRatioStDf DataFrame into VPRatioSt DataFrame
VPRatioSt = pd.concat([vaccineRatioStDf[['State','Vaccination_Ratio']].set_index('State'), populationRatioStDf[['State','Population_Ratio']].set_index('State')], axis=1).reset_index()

# Calculating Vaccination Ratio to Population Ratio and keeping into 'RatioOfRatios' column
VPRatioSt['RatioOfRatios'] = VPRatioSt['Vaccination_Ratio']/VPRatioSt['Population_Ratio']
VPRatioSt = VPRatioSt.rename(columns={'State':'stateid','Vaccination_Ratio':'vaccinationratio','Population_Ratio':'populationratio','RatioOfRatios':'ratioofratios'})
VPRatioSt = VPRatioSt.dropna().sort_values(by='ratioofratios').reset_index(drop=True)


# Combining vaccineRatioOverallDf and populationRatioOverallDf DataFrame into VPRatioOverall DataFrame
VPRatioOverall = pd.concat([vaccineRatioOverallDf[['Country','Vaccination_Ratio']].set_index('Country'), populationRatioOverallDf[['Country','Population_Ratio']].set_index('Country')], axis=1).reset_index()

# Calculating Vaccination Ratio to Population Ratio and keeping into 'RatioOfRatios' column
VPRatioOverall['RatioOfRatios'] = vaccineRatioOverallDf['Vaccination_Ratio']/populationRatioOverallDf['Population_Ratio']
VPRatioOverall = VPRatioOverall.rename(columns={'Country':'overallid','Vaccination_Ratio':'vaccinationratio','Population_Ratio':'populationratio','RatioOfRatios':'ratioofratios'})


# Generating output CSV files for every district, state and overall country from VPRatioDist, VPRatioSt and VPRatioOverall DataFrame respectively
VPRatioDist.to_csv('district-vaccination-population-ratio.csv', index=False)
VPRatioSt.to_csv('state-vaccination-population-ratio.csv', index=False)
VPRatioOverall.to_csv('overall-vaccination-population-ratio.csv', index=False)

