import pandas as pd


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

