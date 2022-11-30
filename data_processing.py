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


input_cases = pd.read_csv("inputs/covid-19-case-count.csv")

# remove rows where province name is Canada and Repatriated travellers
updated = input_cases['update'] == 1
cases = input_cases[updated]

cases.rename(columns={"prname": "province", "reporting_year": "year"}, inplace=True)
cases['month'] = pd.DatetimeIndex(cases['date']).month
cases['quarter'] = cases.apply(lambda x: month_to_quarter(x.month), axis=1)
cleaned_cases = cases[['province', 'quarter', 'year', 'totalcases', 'numtotal_last7', 'numdeaths', 'numdeaths_last7']]


# -- cleaning and getting data from population-count.csv

# RETURN: population columns = [province/GEO, quarter, year, population]
data = pd.read_csv('../353-project-covid-predictions/inputs/population_count.csv', index_col='REF_DATE').reset_index()

# drop all unwanted columns
data.drop(
    ['DGUID', 'UOM', 'UOM_ID', 'SCALAR_FACTOR', 'SCALAR_ID', 'VECTOR', 'COORDINATE', 'SYMBOL', 'TERMINATED', 'DECIMALS',
     'STATUS'], axis=1, inplace=True)
# Convert year-month to quarter
data['REF_DATE'] = pd.PeriodIndex(data.REF_DATE, freq='Q')

# Transpose the quarter column and make value column the values
pop_df = data.pivot(index='GEO', columns='REF_DATE', values='VALUE').reset_index()
# Rename all the columns
pop_df.columns = ['GEOGRAPHY', '2020-Q1', '2020-Q2', '2020-Q3', '2020-Q4', '2021-Q1', '2021-Q2', '2021Q3', '2021Q4',
                  '2022-Q1', '2022-Q2', '2022-Q3']

