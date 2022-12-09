import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from pmdarima import auto_arima
# from statsmodels.tsa.arima_model import ARIMA
import statsmodels.api as sm
from statsmodels.tools.eval_measures import rmse

monthlyData = pd.read_csv("inputs/processed-data-monthly.csv")

def split_province(df, province):
    return df[df['province'] == province]

def score_polyfit(n):
    model = make_pipeline(
        PolynomialFeatures(degree=n, include_bias=True),
        LinearRegression(fit_intercept=False)
    )
    model.fit(X_train, y_train)
    print('n=%i: Polynomial train score=%.5g, valid score=%.5g' 
            % (n, model.score(X_train, y_train), model.score(X_valid, y_valid)))

def score_linear(X, y, text):
    model = LinearRegression().fit(X, y)
    print('Linear Regression train score=%.5g, valid score=%.5g'
            % (model.score(X_train, y_train), model.score(X_valid, y_valid)), text)

def fill_dates(month, year):
    # print(year+"-"+month+"-01")
    return(str(year)+"-"+str(month)+"-01")

def adf_test(series, title=''):
    print('Dickey-Fuller Test: ')
    result = adfuller(series.dropna(), autolag='AIC')   # dropna() handles differenced data

    labels = ['ADF test', 'p-value', '# lags used', '# observations']
    out = pd.Series(result[0:4], index=labels)

    for key, val in result[4].items():
        out[f'critical value {{key}}']=val
    print(out.to_string())
    print("*"*100)
    if result[1] <= 0.05:
        print("Data has no unit root and is stationary")
    else:
        print("Data has a unit root and is non-stationary")

# alberta = split_province(monthlyData, 'Alberta')
# britishColumbia = split_province(monthlyData, 'British Columbia')
# manitoba = split_province(monthlyData, 'Manitoba')
# newBrunswick = split_province(monthlyData, 'New Brunswick')
# newfoundland = split_province(monthlyData, 'Newfoundland and Labrador')
# northwest = split_province(monthlyData, 'Northwest Territories')
# novaScotia = split_province(monthlyData, 'Nova Scotia')
# nunavut = split_province(monthlyData, 'Nunavut')
# ontario = split_province(monthlyData, 'Ontario')
# princeEdward = split_province(monthlyData, 'Prince Edward Island')
# quebec = split_province(monthlyData, 'Quebec')
# saskatchewan = split_province(monthlyData, 'Saskatchewan')
# yukon = split_province(monthlyData, 'Yukon')

monthlyData = monthlyData[monthlyData['numtotal_atleast1dose'] > 0]
monthlyGrouped = monthlyData.groupby(by=['year', 'month']).sum().reset_index()

############ numtotal_atleast1dose/deaths ############
######################################################

# Setting X and y values, and reshape(-1, 1)
X = monthlyGrouped['numtotal_atleast1dose']
X = np.stack([X], axis=1)
y = monthlyGrouped['numdeaths']
y = np.stack([y], axis=1)

# Split training and validation data
X_train, X_valid, y_train, y_valid = train_test_split(X, y)

# Linear Regression
score_linear(X_train, y_train, '1 DOSE/DEATHS')
linear = LinearRegression().fit(X_train, y_train)
y_prediction = linear.predict(X_valid)

# Plot linear regression
plt.figure(figsize=(15, 8))
plt.subplot(1, 2, 1)
plt.scatter(X_train, y_train, color='b')
plt.plot(X_valid, y_prediction, color='r')
plt.title('Linear Regression: 1 DOSE/DEATHS')
plt.xlabel('At least 1 covid vaccine')
plt.xticks(rotation=45)
plt.ylabel('Deaths')
plt.ticklabel_format(style='plain')


# Polynomial Regression
poly = PolynomialFeatures(degree=6, include_bias=True)
X_poly = poly.fit_transform(X)
model = LinearRegression()
model.fit(X_poly, y)
print("Polynomial Regression degree 6 score (1 DOSE/DEATHS): ", model.score(X_poly, y), "\n")

# Polynomial Regression of degree n
# score_polyfit(3)
# score_polyfit(5)
# score_polyfit(7)
# score_polyfit(11)

# Plot polynomial regression
plt.subplot(1, 2, 2)
plt.scatter(X, y, color='blue')
plt.plot(X, model.predict(poly.fit_transform(X)), color='red')
plt.title('Polynomial Regression: 1 DOSE/DEATHS')
plt.xlabel('At least 1 covid vaccine')
plt.xticks(rotation=45)
plt.ylabel('Deaths')
plt.ticklabel_format(style='plain')
plt.savefig('images/1dose-deaths.png')
# plt.show()

############ totalcases/deaths #######################
######################################################
X = monthlyGrouped['totalcases']
X = np.stack([X], axis=1)
y = monthlyGrouped['numdeaths']
y = np.stack([y], axis=1)

# Split training and validation data
X_train, X_valid, y_train, y_valid = train_test_split(X, y)

# Linear Regression
score_linear(X_train, y_train, 'COVID CASES/DEATH')
linear = LinearRegression().fit(X_train, y_train)
y_prediction = linear.predict(X_valid)

# Plot linear regression
plt.figure(figsize=(15, 8))
plt.subplot(1, 2, 1)
plt.scatter(X_train, y_train, color='b')
plt.plot(X_valid, y_prediction, color='r')
plt.title('Linear Regression: COVID CASES/DEATH')
plt.xlabel('Total Cases')
plt.xticks(rotation=45)
plt.ylabel('Deaths')
plt.ticklabel_format(style='plain')


# Polynomial Regression
poly = PolynomialFeatures(degree=6, include_bias=True)
X_poly = poly.fit_transform(X)
model = LinearRegression()
model.fit(X_poly, y)
print("Polynomial Regression degree 6 score (COVID CASES/DEATH): ", model.score(X_poly, y), "\n")

# Polynomial Regression of degree n
# score_polyfit(3)
# score_polyfit(5)
# score_polyfit(7)
# score_polyfit(11)

# Plot polynomial regression
plt.subplot(1, 2, 2)
plt.scatter(X, y, color='blue')
plt.plot(X, model.predict(poly.fit_transform(X)), color='red')
plt.title('Polynomial Regression: COVID CASES/DEATH')
plt.xlabel('Total Cases')
plt.xticks(rotation=45)
plt.ylabel('Deaths')
plt.ticklabel_format(style='plain')
plt.savefig('images/totalcases-deaths.png')
plt.show()

# Get date
# monthlyData['date'] = pd.to_datetime(monthlyData.apply(lambda x: fill_dates(x.month, x.year), axis=1))
# monthlyData.set_index("date", inplace=True)


# Adapted from https://medium.com/analytics-vidhya/time-series-prediction-with-machine-learning-getting-started-8763eda1127f
# Time series prediction
# timeSeries = monthlyGrouped.filter(items=['numtotal_atleast1dose', 'numdeaths'])
# # timeSeries['numdeaths'] = timeSeries['numdeaths'].astype(str)

# # print(timeSeries)

# timeSeries.set_index('numtotal_atleast1dose', inplace=True)
# # print(timeSeries)

# half = int(len(timeSeries)/2)
# train = timeSeries.iloc[0:half]
# # train2 = timeSeries.iloc[0:half]
# test = timeSeries.iloc[half+1:]

# # print(len(train))
# # print(train)
# # print(timeSeries)

# plt.subplot(1, 3, 3)
# plt.xticks(rotation=45)
# plt.plot(timeSeries)
# # plt.show()

# # # Seasonal decompose
# results = seasonal_decompose(timeSeries['numdeaths'], model='additive', period=12)  # show data for each month
# plt.ticklabel_format(style='plain')
# results.plot()
# # plt.show()

# # Check for stationarity
# adf_test(timeSeries)

# # Make the data stationary; result showed the best parameters are p=0, d=1, q=1
# result = auto_arima(timeSeries['numdeaths'], seasonal=True, trace=True)     # Get the best parameter for p,d,q

# # Build ARIMA model
# model = sm.tsa.arima.ARIMA(train['numdeaths'], order=(0,1,1))
# result = model.fit()

# # Predict the test data
# start = train.iloc[0]
# end = len(timeSeries)-1

# pred = result.predict(start=train.shape[0], end=(train.shape[0]+test.shape[0]-1), typ="levels", dymamic=False).rename("Predictions")

# test['numdeaths'].plot(figsize=(12,8), legend=True)
# pred.plot(legend=True)

# error = rmse(test['numdeaths'], pred)
# print(f'ARIMA(0,1,1) RMSE Error: {error:11.10}')

# forecast = result.predict(len(timeSeries), end=len(timeSeries)+1, typ="levels", dynamic=False).rename("forecasted Data")
# timeSeries['numdeaths'].plot(figsize=(12,8), legend=True)
# forecast.plot(legend=True)
# plt.show()


