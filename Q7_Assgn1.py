#!/usr/bin/env python
# coding: utf-8


#Importing libraries
import pandas as pd
import numpy as np 


# Reading cowin_vaccine_data_districtwise.csv file into vaccine_data DataFrame
vaccine_data = pd.read_csv('input/cowin_vaccine_data_districtwise.csv')
vaccine_data = vaccine_data[vaccine_data['S No']>0]


# Extracting total number of Covishield and Covaxin vaccinated persons for each district into vaccineDf DataFrame
vaccineDf = vaccine_data[['State','District_Key','14/08/2021.9','14/08/2021.8']]
vaccineDf = vaccineDf.rename(columns={'State':'stateid','District_Key':'districtid','14/08/2021.9':'Covishield_Vaccinated','14/08/2021.8':'Covaxin_Vaccinated'})
vaccineDf = vaccineDf.astype({'Covishield_Vaccinated':int, 'Covaxin_Vaccinated':int})


# Taking Covishield and Covaxin vaccinated ratio for each district and keeping into vaccineRatioDistDf DataFrame
vaccineRatioDistDf = vaccineDf[['districtid','Covishield_Vaccinated','Covaxin_Vaccinated']]
vaccineRatioDistDf = vaccineRatioDistDf.groupby('districtid',sort=False).sum()
vaccineRatioDistDf = vaccineRatioDistDf.reset_index()
vaccineRatioDistDf['vaccineratio'] = vaccineRatioDistDf['Covishield_Vaccinated']/vaccineRatioDistDf['Covaxin_Vaccinated']
vaccineRatioDistDf = vaccineRatioDistDf[['districtid','vaccineratio']].sort_values(by='vaccineratio').reset_index(drop=True)
vaccineRatioDistDf[vaccineRatioDistDf == np.Inf] = np.NAN
vaccineRatioDistDf


# Taking Covishield and Covaxin vaccinated ratio for each state and keeping into vaccineRatioStDf DataFrame
vaccineRatioStDf = vaccineDf[['stateid','Covishield_Vaccinated','Covaxin_Vaccinated']]
vaccineRatioStDf = vaccineRatioStDf.groupby('stateid').sum()
vaccineRatioStDf = vaccineRatioStDf.reset_index()
vaccineRatioStDf['vaccineratio'] = vaccineRatioStDf['Covishield_Vaccinated']/vaccineRatioStDf['Covaxin_Vaccinated']
vaccineRatioStDf = vaccineRatioStDf[['stateid','vaccineratio']].sort_values(by='vaccineratio').reset_index(drop=True)
vaccineRatioStDf[vaccineRatioStDf == np.Inf] = np.NAN
vaccineRatioStDf


# Taking Covishield and Covaxin vaccinated ratio for overall country and keeping into vaccineRatioOverallDf DataFrame
vaccineRatioOverallDf = vaccineDf[['Covishield_Vaccinated','Covaxin_Vaccinated']]
vaccineRatioOverallDf.insert(loc=0, column='overallid', value='India')
vaccineRatioOverallDf = vaccineRatioOverallDf.groupby('overallid').sum()
vaccineRatioOverallDf = vaccineRatioOverallDf.reset_index()
vaccineRatioOverallDf['vaccineratio'] = vaccineRatioOverallDf['Covishield_Vaccinated']/vaccineRatioOverallDf['Covaxin_Vaccinated']
vaccineRatioOverallDf = vaccineRatioOverallDf[['overallid','vaccineratio']].sort_values(by='vaccineratio').reset_index(drop=True)
vaccineRatioOverallDf


# Generating output CSV files for every district, state and overall country from vaccineRatioDistDf, vaccineRatioStDf and vaccineRatioOverallDf DataFrame respectively
vaccineRatioDistDf.to_csv('district-vaccine-type-ratio.csv', index=False)
vaccineRatioStDf.to_csv('state-vaccine-type-ratio.csv', index=False)
vaccineRatioOverallDf.to_csv('overall-vaccine-type-ratio.csv', index=False)

