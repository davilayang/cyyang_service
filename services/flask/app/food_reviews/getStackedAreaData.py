from app.api import app, db
import pandas as pd
from pandas.tseries.offsets import MonthEnd

def getStackedArea(start_date='2014-01-01', end_date='2014-12-31'):
    query = \
    """
    SELECT 
        main_category_en AS category, 
        review_date, 
        review_id AS id,
        star_rating
    FROM 
        food_reviews
    WHERE 
        energy_100g IS NOT NULL
        AND review_date IS NOT NULL
        AND main_category_en IS NOT NULL
        AND energy_100g < 3000
        AND salt_100g < 100
        AND main_category_en SIMILAR TO '[A-Z]_*'
        AND review_date BETWEEN '{0}' AND '{1}'
    ORDER BY
        review_date
    """.format(start_date, end_date)
    sub = pd.read_sql(query, con=db.engine)

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

