import pandas as pd
from flask import Flask
from flask import request
# Using flask for API
app = Flask(__name__)

# Importing data as csv-files
url1 = 'https://raw.githubusercontent.com/LordVehement/case-study-public-holiday/main/public-holiday-open-data.csv'
url2 = 'https://raw.githubusercontent.com/LordVehement/case-study-public-holiday/main/wikipedia-iso-country-codes.csv'
df1 = pd.read_csv(url1)
df2 = pd.read_csv(url2)

# Using a left merge on the two data sets
df2 = df2.rename(columns={"English short name lower case": "country"})
df3 = pd.merge(df1, df2, how='left')

# Dropping unnecessary columns
df3 = df3.drop(['ISO_2', 'Alpha-2 code', 'Numeric code', 'ISO 3166-2'], axis=1).rename(
    columns={'Alpha-3 code': 'ISO_3'})

# df4 is the final data frame that creates a summary table of number of holidays per country
df4 = df3
df4['date'] = pd.to_datetime(df3['date'])
df4 = df4.groupby(['country', df3.date.dt.year]).count().drop('ISO_3', axis=1).rename(
    columns={'date': 'num_holidays'})  # The combination of groupby() and count() can be seen as a MapReduce


@app.route('/')  # route our API to /
def is_holiday():  # introduce a function for our API
    result = False  # we start by assuming that we will have found a holiday
    date = input('date: ')  # we request the input date
    country = input('country: ')  # we request the input country
    for i in range(len(df3)):
        if df3['country'][i].lower().replace('s/+', '') == country[0].lower().replace('s/+', '') and df3['date'][i] == pd.to_datetime(date):
            result = True
            break
# The above if statement is supposed to evaluate if the arguments are equal to any data point, however it does not work
# as intended.
    if result:
        return {'Holiday': True}, 200  # if the arguments are equal to any data point then return True
    else:
        return {'Holiday': False}, 200  # if the arguments are not equal to any data point then return False


if __name__ == '__main__':  # run the application
    app.run()
