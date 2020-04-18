from pandas import date_range
from app.utilities import get_dataframe_from_db

def get_data(start_date, end_date):

    query = \
    f"""
    SELECT 
        main_category_en AS category, 
        review_date,
        review_id AS id
    FROM 
        food_reviews
    WHERE 
        energy_100g IS NOT NULL
        AND main_category_en IS NOT NULL
        AND energy_100g < 3000
        AND main_category_en SIMILAR TO '[A-Z]_*'
        AND review_date BETWEEN '{start_date}' AND '{end_date}'
    ORDER BY
        review_date
    """

    data = get_dataframe_from_db(query)

    return data

# Process data for exporting, given start and end date
def prepare_ridgeline(start_date, end_date):

    df = get_data(start_date, end_date)

    threshold = df.groupby('category')[['id']].count()\
        .sort_values('id', ascending=False)\
        .iloc[9, 0]

    top10 = df.assign(counts=lambda d: d.groupby('category')[['id']].transform('count'))\
        .query('counts >= {}'.format(threshold))\
        .replace({'Plant-based foods and beverages': 'Plant-Based', 
                  'Products without gluten': 'No Gluten',
                  'Coffee-creamer': 'Creamer'})\
        .reset_index(drop=True)

    date_idx = []
    for category in top10.category.unique():
        for date in date_range(start_date, end_date, freq='D'):
            date_idx.append((category, date))

    data = top10.groupby(['category', 'review_date'])[['id']].count()\
        .reindex(date_idx, fill_value=0)\
        .reset_index()\
        .assign(byCategorySum=lambda d: d.groupby('category')[['id']].transform('sum'))\
        .assign(p=lambda d: d.id / d.byCategorySum)\
        .drop(['id', 'byCategorySum'], axis=1)

    data = data.assign(byCategoryMaxP=lambda d: d.groupby('category')[['p']].transform(max))\
        .assign(p_peak=lambda d: d.p / d.byCategoryMaxP)\
        .drop(['byCategoryMaxP'], axis=1)

    data = data.assign(p_lag1=lambda d: d.groupby('category')[['p_peak']].shift(-1))\
        .assign(p_lead1=lambda d: d.groupby('category')[['p_peak']].shift(1))\
        .assign(p_smooth=lambda d: (d.p_lag1 + d.p_peak + d.p_lead1) / 3)\
        .drop(['p_lag1', 'p_lead1'], axis=1)\
        .fillna(method='ffill', axis=1)

    data = data\
        .assign(p_lag1=lambda d: d.groupby('category')[['p_peak']].shift(-1))\
        .assign(p_lag2=lambda d: d.groupby('category')[['p_peak']].shift(-2))\
        .assign(p_lag3=lambda d: d.groupby('category')[['p_peak']].shift(-3))\
        .assign(p_lead1=lambda d: d.groupby('category')[['p_peak']].shift(1))\
        .assign(p_lead2=lambda d: d.groupby('category')[['p_peak']].shift(2))\
        .assign(p_lead3=lambda d: d.groupby('category')[['p_peak']].shift(3))\
        .assign(p_smooth7=lambda d: (d.p_lag1 + d.p_lag2 + d.p_lag3 + 
                                    d.p_lead1 + d.p_lead2 + d.p_lead3 +
                                    d.p_peak) / 7)\
        .drop(['p_lag1', 'p_lag2', 'p_lag3', 'p_lead1', 'p_lead2', 'p_lead3'], axis=1)\
        .fillna(method='ffill', axis=1)

    return data.to_json(orient='records')
    