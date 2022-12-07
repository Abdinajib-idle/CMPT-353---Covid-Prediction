import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np


# def fill_in_first_difference(initial, difference):
#     if difference == -9999:
#         return initial
#     else:
#         return difference

# def get_new_data_by_quarter(col_name, data, df):
#     df['name_of_new_col'] = df[data].subtract(df.shift(1)[data])
#     df.loc[
#         ((df['quarter'] == 1) & (df[
#                                      'year'] == 2020)), 'name_of_new_col'] = None  # we dont know change in data if there is no previous data
#     # df['name_of_new_col'] = df.apply(lambda x: fill_in_first_difference(x[data], x.name_of_new_col), axis=1)
#     df.rename(columns={"name_of_new_col": col_name}, inplace=True)
def get_new_data_by_month(col_name, data, df):
    df['name_of_new_col'] = df[data].subtract(df.shift(1)[data])
    df.loc[((df['month'].isin([1,2])) & (df['year'] == 2020)), 'name_of_new_col'] = None  # we dont know change in data if there is no previous data
    df.rename(columns={"name_of_new_col": col_name}, inplace=True)


# (1) --- process data further
# data = pd.read_csv("inputs/processed-data-monthly.csv")
# data.drop(columns=['Unnamed: 0'], inplace=True)
#
# # --- get number of new cases/deaths/population/vaccinations during a month
# get_new_data_by_month('new_cases', 'totalcases', data)
# get_new_data_by_month('new_deaths', 'numdeaths', data)
# get_new_data_by_month('new_vaccination', 'numtotal_atleast1dose', data)
# #
# # --- get number of new cases/deaths/population/vaccinations during a quarter
# # get_new_data_by_quarter('new_cases', 'totalcases', data)
# # get_new_data_by_quarter('new_deaths', 'numdeaths', data)
# # get_new_data_by_quarter('new_population', 'population', data)
# # get_new_data_by_quarter('new_vaccination', 'numtotal_atleast1dose', data)
#
# # --- get score of deaths by population
# data['death_score'] = (data['numdeaths'] / data['population'])
#
# # --- get score of cases by population
# data['case_score'] = (data['totalcases'] / data['population'])
#
# # # --- convert scores calculated from data_processing_monthly.py into percentage
# # data['vaccination_score_atleast1dose']
# # data['vaccination_score_fully']
#
# data.to_csv("inputs/visualization-data-monthly.csv")

data = pd.read_csv("inputs/visualization-data-monthly.csv", parse_dates={'date': ['year', 'month']}, keep_date_col=True)
# data['date'] = data['year']+data['month']
# rows are values, dates
sns.set_theme(style="whitegrid")
sns.lineplot(x=data['date'], y=data['case_score'], hue=data["province"], palette="tab10", linewidth=2.5)
plt.title("Total Case Score Over Time")
plt.xticks(rotation=25)
plt.savefig("graphs/cases-by-time")

# sns.regplot(x = "new_cases", y="new_deaths", data=data, fit_reg = False, scatter_kws={"alpha": 0.2})
# plt.savefig("linear-relationship.png")
# print("end")


# # --- BAR GRAPH -- Comparison of Province Deaths Relative to Population
# # Figure Size
# fig, (ax1, ax2) = plt.subplots(1,2, figsize=(18, 9))
# death_score = ax1.barh(data['province'], data['death_score'])
# vaccine_score = ax2.barh(data['province'], data['vaccination_score_atleast1dose'])
#
# # # Remove axes splines
# for s in ['top', 'bottom', 'left', 'right']:
#     ax1.spines[s].set_visible(False)
#
# # Add padding between axes and labels
# ax1.xaxis.set_tick_params(pad=5)
# ax1.yaxis.set_tick_params(pad=10)
#
# # Add x, y gridlines
# ax1.grid(visible=True, color='grey',
#         linestyle='-.', linewidth=0.5,
#         alpha=0.2)
#
# ax1.xlabel("Death Percentage (%)")
# ax2.xlabel("Vaccination Percentage (%)")
# plt.ylabel("Percentage of deaths by population")
# plt.title("Comparison of Province Deaths Relative to Population")
# plt.legend((death_score, vaccine_score), ('deaths (%)', 'vaccinations(%)'))
# plt.savefig("graphs/pop-deaths-bar-graph.png")
# #


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# # --- LINREG GRAPH WITH FACET-- new vaccination counts and new deaths
# province_grp1 = data['province'].isin(['Alberta', 'British Columbia', 'Manitoba', 'New Brunswick'])
# province_grp2 = data['province'].isin(['Newfoundland and Labrador', 'Northwest Territories','Nova Scotia','Nunavut' ])
# province_grp3 = data['province'].isin([ 'Ontario', 'Prince Edward Island', 'Quebec', 'Saskatchewan', 'Yukon'])
#
# grp1 = data[province_grp1]
# grp2 = data[province_grp2]
# grp3 = data[province_grp3]
#
# groups = [grp1, grp2, grp3]
#
# for groupnum, group in enumerate(groups):
#     sns.lmplot(data=group, x="new_vaccination", y="new_deaths", col="province",  facet_kws=dict(sharex=False, sharey=False), scatter=True)
#     plt.savefig(f'graphs/linreg-{groupnum}.png')