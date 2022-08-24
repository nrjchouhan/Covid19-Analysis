Plugins-
Software: Terminal (.sh files run .py files)

Environment: Python 3.8.8



Dependencies-
Python Libraries: pandas 1.2.4, numpy 1.20.1, dateutil 2.8.1, json, datetime



Programs-


.sh files:

assign1.sh
Top-level script that runs the entire assignment

neighbor-districts-modified.sh
runs Q1_Assgn1.py as
python3.8 Q1_Assgn1.py

edge-generator.sh
runs Q2_Assgn1.py as
python3.8 Q2_Assgn1.py

case-generator.sh
runs Q3_Assgn1.py as
python3.8 Q3_Assgn1.py

peaks-generator.sh
runs Q4_Assgn1.py as
python3.8 Q4_Assgn1.py

vaccinated-count-generator.sh
runs Q5_Assgn1.py as
python3.8 Q5_Assgn1.py

vaccination-population-ratio-generator.sh
runs Q6_Assgn1.py as
python3.8 Q6_Assgn1.py

vaccine-type-ratio-generator.sh
runs Q7_Assgn1.py as
python3.8 Q7_Assgn1.py

vaccinated-ratio-generator.sh
runs Q8_Assgn1.py as
python3.8 Q8_Assgn1.py

complete-vaccination-generator.sh
runs Q9_Assgn1.py as
python3.8 Q9_Assgn1.py


Python files:

Q1_Assgn1.py
Input: neighbor-districts.json, Covid-19 api (district_wise.csv, cowin_vaccine_data_districtwise.csv)
Output: neighbor-districts-modified.json
Remark: Manually updated spelling mismatch district names in neighbor-districts.json input file. All input files are kept in 'input' directory.

Q2_Assgn1.py
Input: neighbor-districts-modified.json
Output: edge-graph.csv
Remark: Input file neighbor-districts-modified.json is available outside 'input' directory.

Q3_Assgn1.py
Input: Covid-19 api (districts.csv, cowin_vaccine_data_districtwise.csv, raw_data1.csv, raw_data1.csv)
Output: cases-week.csv, cases-month.csv, cases-overall.csv
Remark: Covid cases data before 26 Apr'2020 is taken from raw_data1.csv, raw_data1.csv and after 26 Apr'2020 data from districts.csv. All input files are kept in 'input' directory.

Q4_Assgn1.py
Input: Covid-19 api (districts.csv, cowin_vaccine_data_districtwise.csv)
Output: district-peaks.csv, state-peaks.csv, overall-peaks.csv
Remark: Considering 1st week/month from 15 Mar'2020. I have calculated number of active cases for each day using 'Confirmed - Recovered - Death'. For active number of cases of week/month took mean (average) of active cases of each all days in that week/month. Blank (NaN) entry in output files indicates there are no cases information available in districts.csv file or cases are 0. All input files are kept in 'input' directory.

Q5_Assgn1.py
Input: Covid-19 api (cowin_vaccine_data_districtwise.csv)
Output: district-vaccinated-count-week.csv, district-vaccinated-count-month.csv, district-vaccinated-count-overall.csv, state-vaccinated-count-week.csv, state-vaccinated-count-month.csv, state-vaccinated-count-overall.csv
Remark: Vaccination data is available from 16 Jan'2021. So considering week-1 from 10 Jan'2021 (Sunday). All input files are kept in 'input' directory.

Q6_Assgn1.py
Input: Census Population 2011 data (DDW_PCA0000_2011_Indiastatedist.xlsx), Covid-19 api (cowin_vaccine_data_districtwise.csv)
Output: district-vaccination-population-ratio.csv, state-vaccination-population-ratio.csv, overall-vaccination-population-ratio.csv
Remark: All input files are kept in 'input' directory.

Q7_Assgn1.py
Input: Covid-19 api (cowin_vaccine_data_districtwise.csv)
Output: district-vaccine-type-ratio.csv, state-vaccine-type-ratio.csv, overall-vaccine-type-ratio.csv
Remark: 'vaccineratio' as NaN (blank entry) in the district/state indicates 0 covaxin dose vaccinated. All input files are kept in 'input' directory.

Q8_Assgn1.py
Input: Census Population 2011 data (DDW_PCA0000_2011_Indiastatedist.xlsx), Covid-19 api (cowin_vaccine_data_districtwise.csv)
Output: district-vaccinated-dose-ratio.csv, state-vaccinated-dose-ratio.csv, overall-vaccinated-dose-ratio.csv
Remark: All input files are kept in 'input' directory.

Q9_Assgn1.py
Input: Census Population 2011 data (DDW_PCA0000_2011_Indiastatedist.xlsx), Covid-19 api (cowin_vaccine_data_districtwise.csv)
Output: complete-vaccination.csv
Remark: All input files are kept in 'input' directory.


How to run:
In order to run all the programs sequentially, run below mentioned command from the terminal-
bash assign1.sh
