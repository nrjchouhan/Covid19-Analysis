#!/usr/bin/env python
# coding: utf-8


# Importing libraries
import json
import pandas as pd

# Opening Neighbor District JSON file
with open('input/neighbor-districts.json') as neighbor_json:
    neighbor_data = json.load(neighbor_json)

# Converting JSON file to DataFrame
neighborDF = pd.json_normalize(neighbor_data)

# List of districts - sample entry: 'bhopal/Q1797245'
dist_in_neighborJson = list(neighbor_data.keys())

# Removing Q-codes from districts
# Dictionary of districts - sample entry: 'bhopal/Q1797245': 'bhopal'
dist_in_neighborJson_dict = {}
i=0
for d in dist_in_neighborJson:
    dList = d.split('/')
    dist_in_neighborJson[i] = dList[0]
    dist_in_neighborJson[i] = dist_in_neighborJson[i].replace('_',' ')
    ith_dist = dist_in_neighborJson[i].split(' ')
    if 'district' in ith_dist:
        ith_dist.remove('district')
    dist_in_neighborJson[i] = ' '.join(ith_dist)
    dist_in_neighborJson_dict[d] = dist_in_neighborJson[i]
    i += 1

# Reading district_wise.csv file into covid_data DataFrame
covid_data = pd.read_csv('input/district_wise.csv')
covid_data = covid_data[covid_data['SlNo'] > 0]
# Removing Unknown districts
covid_data = covid_data[covid_data['District'] != 'Unknown']

# Selecting required column from covid_data DataFrame into new DataFrame
covid_data_dist = covid_data[['District','District_Key']]

# Creating Dictionary of District_Key and District for Covid data - sample entry: 'MP_Bhopal': 'bhopal'
covid_data_dist_dict = covid_data_dist.set_index('District_Key').T.to_dict('list')
covid_data_dist_dict = dict(zip(list(covid_data_dist_dict),[l[0].lower() for l in list(covid_data_dist_dict.values())]))

# Reading cowin_vaccine_data_districtwise.csv file into vaccine_data DataFrame
vaccine_data = pd.read_csv('input/cowin_vaccine_data_districtwise.csv')
vaccine_data = vaccine_data[vaccine_data['S No'] > 0]
vaccine_data

# Selecting required column from vaccine_data DataFrame into new DataFrame
vaccine_data_dist = vaccine_data[['District','District_Key']].drop_duplicates()
vaccine_data_dist

# Creating Dictionary of District_Key and District for Vaccine data - sample entry: 'MP_Bhopal': 'bhopal'
vaccine_data_dist_dict = vaccine_data_dist.set_index('District_Key').T.to_dict('list')
vaccine_data_dist_dict = dict(zip(list(vaccine_data_dist_dict),[l[0].lower() for l in list(vaccine_data_dist_dict.values())]))
vaccine_data_dist_dict

# Dictionary of duplicate district name which are in different states
duplicate_dist_mapping_dict = {
    'aurangabad/Q43086' : 'BR/BR_Aurangabad/Aurangabad',
    'aurangabad/Q592942' : 'MH/MH_Aurangabad/Aurangabad',
    'balrampur/Q16056268' : 'CT/CT_Balrampur/Balrampur',
    'balrampur/Q1948380' : 'UP/UP_Balrampur/Balrampur',
    'bilaspur/Q100157' : 'CT/CT_Bilaspur/Bilaspur',
    'bilaspur/Q1478939' : 'HP/HP_Bilaspur/Bilaspur',
    'hamirpur/Q2086180' : 'HP/HP_Hamirpur/Hamirpur',
    'hamirpur/Q2019757' : 'UP/UP_Hamirpur/Hamirpur',
    'pratapgarh/Q1473962' : 'UP/UP_Pratapgarh/Pratapgarh',
    'pratapgarh/Q1585433' : 'RJ/RJ_Pratapgarh/Pratapgarh'
}

# List of districts in Neighbor JSON file but not in covid and vaccine data
district_in_neighborJson_but_not_in_covid_and_vaccine_data = ['konkan division', 'niwari', 'noklak', 'mumbai suburban']

# Removing districts in Neighbor JSON file but not in covid and vaccine data from dictionary of districts
for x in district_in_neighborJson_but_not_in_covid_and_vaccine_data:
    for dc, d in dist_in_neighborJson_dict.items():
        if d == x:
            del dist_in_neighborJson_dict[dc]
            break

# Creating dictionary of mapping between Neighbor JSON districts to Vaccine data districts with state code and district code
# sample entry: 'bhopal/Q1797245': 'MP/MP_Bhopal/Bhopal'
neighborJson_districtKey_mapping_dict = {}
for ndist in dist_in_neighborJson_dict.keys():
    if ndist in duplicate_dist_mapping_dict.keys():
        neighborJson_districtKey_mapping_dict[ndist] = duplicate_dist_mapping_dict[ndist]
    else:
        dkey = [district_key for district_key, district in vaccine_data_dist_dict.items() if district == dist_in_neighborJson_dict[ndist]][0]
        l = dkey.split('_')
        neighborJson_districtKey_mapping_dict[ndist] = l[0]+'/'+dkey+'/'+l[1]

# List of districts from mapping dictionary of Neighbor JSON and Vaccine data districts
modified_neighbor_key = list(neighborJson_districtKey_mapping_dict.values())

# Creating list of neighbor districts of each district
modified_neighbor_value = []
for dqc in neighborJson_districtKey_mapping_dict.keys():
    neighbor_list = [neighborJson_districtKey_mapping_dict[d] for d in neighbor_data[dqc] if d in neighborJson_districtKey_mapping_dict.keys()]
    modified_neighbor_value.append(neighbor_list)

# Combining list of districts and list of neighbor districts as key-value pair into neighbor_districts_modified dictionary
neighbor_districts_modified = dict(zip(modified_neighbor_key, modified_neighbor_value))

# Sorting dictionary districts alphabetically
neighbor_districts_modified = dict(sorted(neighbor_districts_modified.items()))

# Generating output neighbor-districts-modified.json file from neighbor_districts_modified dictionary
with open("neighbor-districts-modified.json", "x") as neighbor_districts_modified_json:
    json.dump(neighbor_districts_modified, neighbor_districts_modified_json, indent=2)






