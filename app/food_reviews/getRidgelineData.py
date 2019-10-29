from app import app, db
import pandas as pd
import numpy as np

# Process data for exporting, given start and end date
def getRidgeline(start_date, end_date, n_times=6):
    query = \
    """
    SELECT 
        customer_id,
        review_id, 
        review_date
    FROM 
        food_reviews
    WHERE 
        verified_purchase LIKE 'Y'
        AND review_date IS NOT NULL
        AND review_date BETWEEN '{0}' AND '{1}'
    ORDER BY
        review_date
    """.format(start_date, end_date)
    sub = pd.read_sql(query, con=db.engine)

    index = []
    for times in range(1, n_times): # how many review times to show
        for weekday in range(7): # 7 days of a week
            index.append((times, weekday))

    data = sub.assign(times=lambda df: df.groupby('customer_id')[['review_id']].transform('count'))\
        .assign(times=lambda df: np.where(df.times >= n_times-1, n_times-1, df.times))\
        .groupby(['times', sub.review_date.dt.dayofweek])[['review_id']].count()\
        .reindex(index, fill_value=0)\
        .reset_index(drop=False)\
        .assign(byTimesSum=lambda d: d.groupby('times')[['review_id']].transform('sum'))\
        .assign(p=lambda d: d.review_id / d.byTimesSum)\
        .assign(byTimesMaxP=lambda d: d.groupby('times')[['p']].transform(max))\
        .assign(p_peak=lambda d: d.p / d.byTimesMaxP)\
        .assign(p_lag1=lambda d: d.groupby('times')[['p_peak']].shift(-1))\
        .assign(p_lead1=lambda d: d.groupby('times')[['p_peak']].shift(1))\
        .assign(p_smooth=lambda d: (d.p_lag1 + d.p_peak + d.p_lead1) / 3)\
        .drop(['review_id', 'byTimesSum', 'byTimesMaxP', 'p_lag1', 'p_lead1',], axis=1)\
        .rename(columns={'times': 'review_times', 'review_date': 'weekday'})\
        .fillna(method='ffill', axis=1)

    return data.to_json(orient='records')

