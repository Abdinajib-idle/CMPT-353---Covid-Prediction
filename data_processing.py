import pandas as pd


# -- cleaning and getting data from covid-19-case-count.csv

def month_to_quarter(month):
    if 1 <= month <= 3:
        return 1
    elif 4 <= month <= 6:
        return 2
    elif 7 <= month <= 9:
        return 3
    else:
        return 4



######################### COVID CASES COUNT #########################
#####################################################################
input_cases = pd.read_csv("inputs/covid-19-case-count.csv")

# remove rows where province name is Canada and Repatriated travellers
updated = input_cases['update'] == 1
cases = input_cases[updated]

cases.rename(columns={"prname": "province", "reporting_year": "year"}, inplace=True)
cases['month'] = pd.DatetimeIndex(cases['date']).month
cases['quarter'] = cases.apply(lambda x: month_to_quarter(x.month), axis=1)
cleaned_cases = cases[['province', 'quarter', 'year', 'totalcases', 'numtotal_last7', 'numdeaths', 'numdeaths_last7']]
cleaned_cases = cleaned_cases.sort_values(by=['province'])

# Group covid cases data by province, year, quarter and sum the cases
cleaned_cases = cleaned_cases.groupby(['province', 'year', 'quarter']).sum().reset_index()
# cleaned_cases.to_csv('cleaned.csv')

# -- cleaning and getting data from population-count.csv
# RETURN: population columns = [province/GEO, quarter, year, population]
# data = pd.read_csv('../353-project-covid-predictions/inputs/population_count.csv', index_col='REF_DATE').reset_index()

# # drop all unwanted columns
# data.drop(
#     ['DGUID', 'UOM', 'UOM_ID', 'SCALAR_FACTOR', 'SCALAR_ID', 'VECTOR', 'COORDINATE', 'SYMBOL', 'TERMINATED', 'DECIMALS',
#      'STATUS'], axis=1, inplace=True)
# # Convert year-month to quarter
# data['REF_DATE'] = pd.PeriodIndex(data.REF_DATE, freq='Q')

# # Transpose the quarter column and make value column the values
# pop_df = data.pivot(index='GEO', columns='REF_DATE', values='VALUE').reset_index()
# # Rename all the columns
# pop_df.columns = ['GEOGRAPHY', '2020-Q1', '2020-Q2', '2020-Q3', '2020-Q4', '2021-Q1', '2021-Q2', '2021Q3', '2021Q4',
#                   '2022-Q1', '2022-Q2', '2022-Q3']

# -- cleaning and getting data from population-count.csv
# vaccine columns = [province, numtotal_atleast1dose, numtotal_fully, year, quarter]


######################### POPULATION COUNT #########################
####################################################################
populationCount = pd.read_csv('./inputs/population_count.csv', parse_dates=['REF_DATE'])
# Filter population table by REF_DATE, GEO and VALUE
populationCount = populationCount.filter(items=['REF_DATE', 'GEO', 'VALUE'])
# Rename GEO to province and VALUE to population
populationCount = populationCount.rename(columns={'GEO': 'province', 'VALUE': 'population'})
# Exclude 'Canada' in province column
populationCount = populationCount[populationCount['province'] != 'Canada']
# Extract only year from REF_DATE column
populationCount['year'] = pd.DatetimeIndex(populationCount['REF_DATE']).year
# Extract only quarter from REF_DATE colum
populationCount['quarter'] = populationCount.REF_DATE.dt.quarter
# Remove REF_DATE column
populationCount = populationCount.drop(columns=['REF_DATE'])
# Group population data by province, year, quarter and sum population
populationCount = populationCount.groupby(['province', 'year', 'quarter']).sum().reset_index()
# populationCount.to_csv('population.csv')



######################### VACCINATION COVERAGE MAP #########################
############################################################################
vaccinationCoverage = pd.read_csv('./inputs/vaccination-coverage-map.csv', parse_dates=['week_end'])
# Change column name to 'week_end' to 'province'
vaccinationCoverage = vaccinationCoverage.rename(
    columns={'prename':'province'})
# Keep columns = [province, quarter, year, numtotal_atleast1dose, numtotal_fully]
vaccinationCoverage = vaccinationCoverage.filter(
    items=['province', 'week_end', 'numtotal_atleast1dose', 'numtotal_fully'])
# Excludes 'Canada' in province column
vaccinationCoverage  = vaccinationCoverage[vaccinationCoverage['province'] != 'Canada']
# Extract year
vaccinationCoverage['year'] = pd.DatetimeIndex(vaccinationCoverage['week_end']).year
# Extract quarters
vaccinationCoverage['quarter'] = vaccinationCoverage.week_end.dt.quarter
vaccinationCoverage = vaccinationCoverage.drop(columns=['week_end']).sort_values(by=['province'])
# Group vaccination data by province, year, quarter and sum vaccinations
# vaccinationCoverage.to_csv('vaccinationbeforegroup.csv')
vaccinationCoverage = vaccinationCoverage.groupby(['province', 'year', 'quarter']).agg('sum').reset_index()
# vaccinationCoverage.to_csv('vaccinationaftergroup.csv')


print("end of function")
print(cleaned_cases)
print(populationCount)
print(vaccinationCoverage)


######################### FINAL TABLE #########################
###############################################################
# Join covid cases table with population table by province, year and quarter
final_data = pd.merge(cleaned_cases, populationCount, on=['province', 'year', 'quarter'], how='left')
# final_data.to_csv('final1.csv')
# Join covid cases, population and vaccination table by province, year and quarter
final_data = pd.merge(final_data, vaccinationCoverage, on=['province', 'year', 'quarter'], how='left')
# final_data.to_csv('final2.csv')
print(final_data)


