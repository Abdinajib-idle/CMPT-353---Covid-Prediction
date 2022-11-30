import pandas as pd
import numpy as np
import datetime as dt

# Vaccination coverage map
# vaccine columns = [province, numtotal_atleast1dose, numtotal_fully, year, quarter]

vaccinationCoverage = pd.read_csv('./inputs/vaccination-coverage-map.csv', parse_dates=['week_end'])
# print(vaccinationCoverage)

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

vaccinationCoverage = vaccinationCoverage.drop(columns=['week_end'])
print(vaccinationCoverage)