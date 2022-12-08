from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def get_new_data_by_month(col_name, data, df):
    df['name_of_new_col'] = df[data].subtract(df.shift(1)[data])
    df.loc[((df['month'].isin([1,2])) & (df['year'] == 2020)), 'name_of_new_col'] = None  # we dont know change in data if there is no previous data
    df.rename(columns={"name_of_new_col": col_name}, inplace=True)


# (1) --- process data further
data = pd.read_csv("inputs/processed-data-monthly.csv")
data.drop(columns=['Unnamed: 0'], inplace=True)

# --- get number of new cases/deaths/population/vaccinations during a month
get_new_data_by_month('new_cases', 'totalcases', data)
get_new_data_by_month('new_deaths', 'numdeaths', data)
get_new_data_by_month('new_vaccination', 'numtotal_atleast1dose', data)

# --- get score of deaths by population
data['death_score'] = (data['numdeaths'] / data['population'])
data['new_death_score'] = (data['new_deaths'] / data['population'])

# --- get score of cases by population
data['case_score'] = (data['totalcases'] / data['population'])
data['new_case_score'] = (data['new_cases'] / data['population'])

# --- get score of deaths by case
data['new_death_by_case'] = (data['new_deaths'] / data['new_cases'])

data.to_csv("inputs/visualization-data-monthly.csv")

#####################################################################################################################

data = pd.read_csv("inputs/visualization-data-monthly.csv", parse_dates={'date': ['year', 'month']}, keep_date_col=True)
data.drop(columns=['Unnamed: 0'], inplace=True)

pre_vacc = data[(data['month'] != '12') & (data['year'] == '2020') ].groupby('province').mean()
post_vacc = data[(data['year'] == '2022') ].groupby('province').mean()
# --- LINE GRAPH ----------------------------------------
# (1)   Case score over Time
# TODO: uncomment out to generate graph. Ensure graphs (2) (3) are commented out
# sns.set_theme(style="whitegrid")
# sns.lineplot(x=data['date'], y=data['case_score'], hue=data["province"], palette=sns.color_palette("husl", 13), linewidth=2.5)
# plt.title("Case Score Over Time")
# plt.xticks(rotation=25)
# print("saving cases-by-time line graph...")
# plt.savefig("graphs/cases-by-time")

# FINDINGS:
# most cases: PEI, Northwest Territories
# least cases:British Columbia, New brunswick

# (2)   Vaccination score over Time
# TODO: uncomment out to generate graph. Ensure graphs (1) (3) are commented out
# group of top 2 provinces with largest and smallest case score
# province_grp = data[data["province"].isin(['Prince Edward Island', 'British Columbia', 'Northwest Territories', 'New Brunswick'])]
#
# sns.lineplot(x=data['date'], y=data['vaccination_score_atleast1dose'], hue=province_grp['province'], palette='tab10', linewidth=2.5)
# plt.title("Vaccination Score Over Time")
# plt.xticks(rotation=25)
# print("saving vaccination-by-time line graph...")
# plt.savefig("graphs/vaccination-by-time")

# FINDINGS:
# no visible correlation between vaccination score and infection score

# (3)  Death score over Time
# TODO: uncomment out to generate graph. Ensure graphs (1) (2) are commented out
g = sns.scatterplot(x=data['date'], y=data['new_death_by_case'], hue=data["province"], palette=sns.color_palette("husl", 13), alpha=0.5)
plt.xticks(rotation=25)
line = plt.axvline(datetime.strptime('2020-12', '%Y-%m').date(), color='blue', label='vaccine release')
plt.ylabel("death score")
plt.legend(handles=[line])
g.legend()

plt.title("Relation Between Recent Infections and Deaths")
print("saving death-cases-by-time scatter graph...")
plt.savefig("graphs/death-cases-by-time-scatter")



# ----------------------------------------------------------------------------------



# # --- BAR GRAPH -- Comparison of Average New Province Deaths Relative to New Cases in early 2020 (before vaccinations came out in Canada) and late 2022 ------------------------
#

# (4a) Pre-vaccination Death Graph

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 7), constrained_layout=True)


pre_death_score_graph = ax1.barh(pre_vacc.index, pre_vacc['new_death_by_case'])

# Add padding between axes and labels
ax1.xaxis.set_tick_params(pad=5)
ax1.yaxis.set_tick_params(pad=10)

ax1.set_xlim([0,0.3])

# Add x, y gridlines
ax1.grid(visible=True, color='grey',
        linestyle='-.', linewidth=0.5,
        alpha=0.2)

ax1.set_title("Comparison of Mean Deaths Relative to Cases Pre-Vaccination")
#
#
# # (4b) After vaccination Death Graph

post_death_score_graph = ax2.barh(post_vacc.index, post_vacc['new_death_by_case'])

# Add padding between axes and labels
ax2.xaxis.set_tick_params(pad=5)
ax2.yaxis.set_tick_params(pad=10)

ax2.set_xlim([0,0.3])
# Add x, y gridlines
ax2.grid(visible=True, color='grey',
        linestyle='-.', linewidth=0.5,
        alpha=0.2)

ax2.set_title("Comparison of Mean Deaths Relative to Cases Post-Vaccination")

#
print("saving deaths-case-bar-graph bar graph...")
plt.savefig("graphs/deaths-case-bar-graph.png")

#
# # # --- BAR GRAPH -- Comparison of Average New Province Infections Relative to Population in early 2020 (before vaccinations came out in Canada) and 2022 ------------------------

#
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 7), constrained_layout=True)

# (5a) Pre-vaccination Infection Graph
pre_infection_score_graph = ax1.barh(pre_vacc.index, pre_vacc['new_case_score'])

# Add padding between axes and labels
ax1.xaxis.set_tick_params(pad=5)
ax1.yaxis.set_tick_params(pad=10)

ax1.set_xlim([0,0.1])

# Add x, y gridlines
ax1.grid(visible=True, color='grey',
        linestyle='-.', linewidth=0.5,
        alpha=0.2)

ax1.set_title("Comparison of Mean Infections Relative to Population Pre-Vaccination")
#
#
# # (5b) Post-vaccination Infection Graph

post_infection_score_graph = ax2.barh(post_vacc.index, post_vacc['new_case_score'])

# Add padding between axes and labels
ax2.xaxis.set_tick_params(pad=5)
ax2.yaxis.set_tick_params(pad=10)

ax2.set_xlim([0,0.1])
# Add x, y gridlines
ax2.grid(visible=True, color='grey',
        linestyle='-.', linewidth=0.5,
        alpha=0.2)

ax2.set_title("Comparison of Mean Infections Relative to Population Post-Vaccination")


print("saving case-pop-bar-graph bar graph...")
plt.savefig("graphs/case-pop-bar-graph.png")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# # --- LINREG GRAPH WITH FACET-- new vaccination counts and new deaths
# (6,7,8)
province_grp1 = data['province'].isin(['Alberta', 'British Columbia', 'Manitoba', 'New Brunswick'])
province_grp2 = data['province'].isin(['Newfoundland and Labrador', 'Northwest Territories','Nova Scotia','Nunavut' ])
province_grp3 = data['province'].isin([ 'Ontario', 'Prince Edward Island', 'Quebec', 'Saskatchewan', 'Yukon'])

grp1 = data[province_grp1]
grp2 = data[province_grp2]
grp3 = data[province_grp3]

groups = [grp1, grp2, grp3]

for groupnum, group in enumerate(groups):
    sns.lmplot(data=group, x="new_vaccination", y="new_deaths", col="province",  facet_kws=dict(sharex=False, sharey=False), scatter=True)
    plt.savefig(f'graphs/linreg-{groupnum}.png')