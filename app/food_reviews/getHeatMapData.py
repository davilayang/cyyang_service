from app import app, db
import json
import pandas as pd

def getHeatMap(start_date, end_date, n_groups):
    query = \
    """
    SELECT 
        customer_id, review_id, review_date
    FROM 
        food_reviews
    WHERE 
        verified_purchase LIKE 'Y'
        AND review_date IS NOT NULL
        AND review_date BETWEEN '{0}' AND '{1}'
    ORDER BY
        review_date
    """.format(start_date, end_date)
    df = pd.read_sql(query, con=db.engine)\
        .assign(review_times=lambda d: d.groupby('customer_id')[['review_id']].transform('count'))

    d1 = \
    df.assign(group=lambda df: df.review_times.apply(lambda d: (n_groups) if d >= (n_groups) else d))\
    .groupby([df.review_date.dt.weekday, 'group'])[['review_id']].count()\
    .groupby(level=1).apply(lambda d: 100 * ( d / d.sum()))\
    .rename(index=dict(zip(range(7), range(1, 8))), level=0)\
    .reset_index()\
    .rename(mapper={'review_id': 'percentage'}, axis=1)\
    .astype({'group': 'category'})

    d2 = \
    df.assign(group=lambda df: df.review_times.apply(lambda d: (n_groups) if d >= (n_groups) else d))\
    .groupby([df.review_date.dt.day, 'group'])[['review_id']].count()\
    .groupby(level=1).apply(lambda d: 100 * ( d / d.sum()))\
    .reset_index()\
    .rename(mapper={'review_id': 'percentage'}, axis=1)\
    .astype({'group': 'category'})

    d = {'weekday': d1.to_dict(orient ='records'), 'monthday': d2.to_dict(orient ='records')}
    
    return json.dumps(d)

