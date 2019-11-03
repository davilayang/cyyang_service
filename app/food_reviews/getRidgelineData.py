from app import app, db
import pandas as pd
import numpy as np

nutrients = [
    'energy_100g', 'fat_100g', 'fiber_100g', 
    'carbohydrates_100g', 'proteins_100g', 
    'salt_100g', 'sodium_100g', 'sugars_100g'
]

# Process data for exporting, given start and end date
def getRidgeline(start_date, end_date):
    sql = \
    """
    SELECT 
        review_date,
        energy_100g, fat_100g, fiber_100g, 
        carbohydrates_100g, proteins_100g, 
        salt_100g, sodium_100g, sugars_100g
    FROM 
        food_reviews
    WHERE 
        energy_100g IS NOT NULL
        AND energy_100g < 3000
        AND review_date BETWEEN '{0}' AND '{1}'
    ORDER BY
        review_date
    """.format(start_date, end_date)
    df = pd.read_sql(sql, con=db.engine)

    dateIdx = []
    for nutri in nutrients:
        for date in pd.date_range(start_date, end_date, freq='D'):
            dateIdx.append((nutri, date))

    # data preparation
    data = df.fillna(0)\
        .melt(id_vars='review_date', value_vars=nutrients)\
        .groupby(['variable', 'review_date']).agg('mean')\
        .reindex(dateIdx, fill_value=0)\
        .reset_index()
    # calculate p
    data = data\
        .assign(nutrientSum=lambda d: d.groupby('variable')[['value']].transform('sum'))\
        .assign(p=lambda d: d.value / d.nutrientSum)

    # calculate max p
    data = data\
        .assign(nutrientMaxP=lambda d: d.groupby('variable')[['p']].transform(max))\
        .assign(p_peak=lambda d: d.p / d.nutrientMaxP)

    # calculate smoothed p, 3 days smoothing
    data = data\
        .assign(p_lag1=lambda d: d.groupby('variable')[['p_peak']].shift(-1))\
        .assign(p_lead1=lambda d: d.groupby('variable')[['p_peak']].shift(1))\
        .assign(p_smooth=lambda d: (d.p_lag1 + d.p_peak + d.p_lead1) / 3)

    # clean up data
    data = data\
        .drop(['value', 'nutrientSum', 'nutrientMaxP', 'p_lag1', 'p_lead1',], axis=1)\
        .rename(columns={'variable': 'nutrient', 'review_date': 'date'})\
        .fillna(method='ffill', axis=1)

    data = data\
        .assign(p_lag1=lambda d: d.groupby('nutrient')[['p_peak']].shift(-1))\
        .assign(p_lag2=lambda d: d.groupby('nutrient')[['p_peak']].shift(-2))\
        .assign(p_lag3=lambda d: d.groupby('nutrient')[['p_peak']].shift(-3))\
        .assign(p_lead1=lambda d: d.groupby('nutrient')[['p_peak']].shift(1))\
        .assign(p_lead2=lambda d: d.groupby('nutrient')[['p_peak']].shift(2))\
        .assign(p_lead3=lambda d: d.groupby('nutrient')[['p_peak']].shift(3))\
        .assign(p_smooth7=lambda d: (d.p_lag1 + d.p_lag2 + d.p_lag3 + 
                                    d.p_lead1 + d.p_lead2 + d.p_lead3 +
                                    d.p_peak) / 7)\
        .drop(['p_lag1', 'p_lag2', 'p_lag3', 'p_lead1', 'p_lead2', 'p_lead3'], axis=1)\
        .fillna(method='ffill', axis=1)

    return data.to_json(orient='records')

# def getRidgeline(start_date, end_date, n_times=6):
#     query = \
#     """
#     SELECT 
#         customer_id,
#         review_id, 
#         review_date
#     FROM 
#         food_reviews
#     WHERE 
#         verified_purchase LIKE 'Y'
#         AND review_date IS NOT NULL
#         AND review_date BETWEEN '{0}' AND '{1}'
#     ORDER BY
#         review_date
#     """.format(start_date, end_date)
#     sub = pd.read_sql(query, con=db.engine)

#     index = []
#     for times in range(1, n_times): # how many review times to show
#         for weekday in range(7): # 7 days of a week
#             index.append((times, weekday))

#     data = sub.assign(times=lambda df: df.groupby('customer_id')[['review_id']].transform('count'))\
#         .assign(times=lambda df: np.where(df.times >= n_times-1, n_times-1, df.times))\
#         .groupby(['times', sub.review_date.dt.dayofweek])[['review_id']].count()\
#         .reindex(index, fill_value=0)\
#         .reset_index(drop=False)\
#         .assign(byTimesSum=lambda d: d.groupby('times')[['review_id']].transform('sum'))\
#         .assign(p=lambda d: d.review_id / d.byTimesSum)\
#         .assign(byTimesMaxP=lambda d: d.groupby('times')[['p']].transform(max))\
#         .assign(p_peak=lambda d: d.p / d.byTimesMaxP)\
#         .assign(p_lag1=lambda d: d.groupby('times')[['p_peak']].shift(-1))\
#         .assign(p_lead1=lambda d: d.groupby('times')[['p_peak']].shift(1))\
#         .assign(p_smooth=lambda d: (d.p_lag1 + d.p_peak + d.p_lead1) / 3)\
#         .drop(['review_id', 'byTimesSum', 'byTimesMaxP', 'p_lag1', 'p_lead1',], axis=1)\
#         .rename(columns={'times': 'review_times', 'review_date': 'weekday'})\
#         .fillna(method='ffill', axis=1)

#     return data.to_json(orient='records')

