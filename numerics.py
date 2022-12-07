import pandas as pd
from scipy import stats

data = pd.read_csv("inputs/processed-data.csv").reset_index(drop=True).dropna()

data = data.drop(data.columns[[0]], axis=1)  # drops the extra index column


def new_cases_deaths():
    global data
    data['new_cases'] = data['totalcases'].diff(periods=1).fillna(0)
    data['new_deaths'] = data['numdeaths'].diff(periods=1).fillna(0)
    data = data[data['new_cases'] >= 0]
    data = data[data['new_deaths'] >= 0]


# creates column for new cases and fills nan values with 0
new_cases_deaths()

grouped_data = data.groupby(['province', 'year', 'quarter'])[
    ["totalcases", "vaccination_score_atleast1dose", 'vaccination_score_fully', 'numdeaths', 'new_deaths',
     'new_cases']].sum()

# Checking the correlation between number of deaths/new cases and partial vaccination scores
partialvaxed_cases_corr = grouped_data['vaccination_score_atleast1dose'].corr(
    grouped_data['new_cases'])  # 0.0010841371705994753
partialvaxed_deaths_corr = grouped_data['vaccination_score_atleast1dose'].corr(
    grouped_data['new_deaths'])  # -0.31399172469181824

# Checking the correlation between number of deaths/new cases and full vaccination scores
fullyvaxed_cases_corr = grouped_data['vaccination_score_fully'].corr(grouped_data['new_cases'])  # 0.009199529690732818
fullyvaxed_deaths_corr = grouped_data['vaccination_score_fully'].corr(
    grouped_data['new_deaths'])  # -0.26415486621789414

# statistical test to check whether at least 1 dose of vaccination
# affects covid infection or death counts in Canadian
# provinces?
# ttest_partialvax_cases = stats.ttest_ind(grouped_data['vaccination_score_atleast1dose'],
#                                          grouped_data['new_cases']).pvalue
# ttest_partialvax_deaths = stats.ttest_ind(grouped_data['vaccination_score_atleast1dose'],
#                                           grouped_data['new_deaths']).pvalue
# print(ttest_partialvax_cases, ttest_partialvax_deaths)
#
# # fully_vaxed
# ttest_fullvax_cases = stats.ttest_ind(grouped_data['vaccination_score_fully'], grouped_data['new_cases']).pvalue
# ttest_fullvax_deaths = stats.ttest_ind(grouped_data['vaccination_score_fully'], grouped_data['new_deaths']).pvalue
# print(ttest_fullvax_cases, ttest_fullvax_deaths)

# Regression testing gives results slightly closer to reality than ttest
fullyvax_newcases_reg = stats.linregress(grouped_data['vaccination_score_fully'], grouped_data['new_cases']).pvalue
fullyvax_newdeaths_reg = stats.linregress(grouped_data['vaccination_score_fully'], grouped_data['new_deaths']).pvalue
partialvax_newcases_reg = stats.linregress(grouped_data['vaccination_score_atleast1dose'],
                                           grouped_data['new_cases']).pvalue
partialvax_newdeaths_reg = stats.linregress(grouped_data['vaccination_score_atleast1dose'],
                                            grouped_data['new_deaths']).pvalue
print(fullyvax_newcases_reg, fullyvax_newdeaths_reg, partialvax_newcases_reg, partialvax_newdeaths_reg)
# 0.9318137337945325, 0.012370195384950508, 0.9919549500266782, 0.002731075660367884

# annova = stats.f_oneway(grouped_data['vaccination_score_fully'],grouped_data['vaccination_score_fully'],
# grouped_data['new_deaths'], grouped_data['new_cases']) stats.mannwhitneyu(grouped_data['vaccination_score_fully'],
# grouped_data['new_deaths']).pvalue
