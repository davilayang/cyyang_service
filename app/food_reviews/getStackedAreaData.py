from app import app
from flask import request, url_for

import pandas as pd
from pandas.tseries.offsets import MonthEnd

# dataset = url_for('static', filename='data/merged_amz-off_3.csv.gz')
dataset = './app/static/data/merged_amz-off_3.csv.gz'

# api path
@app.route('/api/dStackedArea') # served at /api/dStackedArea
def exportStackedArea():
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')

    # return getData_Ridgeline(start_date, end_date)
    return getStackedArea(start_date, end_date)


# Load Data
df = pd.read_csv(dataset, dtype={'customer_id': 'object',
                                 'product_parent': 'object', 
                                 'star_rating': 'Int64', 
                                 'helpful_votes':'Int64', 
                                 'total_votes': 'Int64', 
                                 'code': 'object'},
                 compression='gzip')

# Convert Review Date to Datetime Object
df.review_date = pd.to_datetime(df.review_date)

# Subset on DataFrame
sub = df[(df.energy_100g.notna()) & (df.energy_100g < 3000) & 
         (df.salt_100g < 100) & (df.review_date.notna()) & 
         (df.main_category_en.notna()) & (df.main_category_en.str.contains('^[A-Z].*'))]\
        .loc[:, ['main_category_en', 'review_date', 'review_id', 'star_rating']]\
        .rename(mapper={'main_category_en': 'category', 'review_id': 'id'}, axis=1)\
        .reset_index(drop=True)

# Process data for exporting, given start and end date
def getStackedArea(start_date='2014-01-01', end_date='2014-12-31', sub=sub):
    sub = sub[(sub.review_date > start_date) & (sub.review_date < end_date)]

    threshold = sub.groupby('category')[['id']].count()\
        .sort_values('id', ascending=False)\
        .iloc[9, 0]

    top10 = sub.assign(counts=lambda d: d.groupby('category')[['id']].transform('count'))\
            .query('counts >= {}'.format(threshold))\
            .assign(year=lambda d: d.review_date.dt.year, month=lambda d: d.review_date.dt.month)\
            .assign(date=lambda d: pd.to_datetime({'year': d.year, 'month': d.month, 'day': 1}) + MonthEnd(0))\
            .drop(['review_date', 'year', 'month'], axis=1)\
            .reset_index(drop=True)

    date_idx = []
    for category in top10.category.unique():  # category
        for rating in range(1, 6): # rating from 1 to 5
            for date in pd.date_range(start_date, end_date, freq='M'):  # months in given time
                date_idx.append((category, rating, date))

    data = top10.groupby(['category', 'star_rating', 'date'])[['id']].count()\
        .reindex(date_idx, fill_value=0)\
        .unstack(level=[0, 1])  # unstack to move indices to columns
    # drop the id column
    data.columns = data.columns.droplevel(level=0)
    # remove index name
    data.index.name = None

    # return data.reset_index().to_json(orient='records')
    return data.reset_index().to_json(orient='split')

