import pandas as pd

# Population_count cleaning
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

print(pop_df)
