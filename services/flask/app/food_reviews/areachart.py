# web/app/food_reviews/areachart.py

from app.utilities import get_dataframe_from_db
from pandas import to_datetime, date_range
from pandas.tseries.offsets import MonthEnd

def get_data(start_date, end_date):

    """
    get_data

    Function to call get_dataframe_from_db and pass query as argument to
    get data for processing

    Args: 
        start_date (str):

        end_date (str): 
    Returns: 
        data (pandas DataFrame):

    """

    query = \
    f"""
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
        AND review_date BETWEEN '{start_date}' AND '{end_date}'
    ORDER BY
        review_date
    """

    data = get_dataframe_from_db(query)

    return data

def prepare_areachart(start_date, end_date):

    """
    prepare_areachart

    Args:
        start_date (str)
        end_date (str)

    Returns:
        data (panads DataFrame)

    """

    df = get_data(start_date, end_date)

    threshold = df.groupby('category')[['id']].count()\
        .sort_values('id', ascending=False)\
        .iloc[9, 0]

    top10 = df.assign(counts=lambda d: d.groupby('category')[['id']].transform('count'))\
            .query('counts >= {}'.format(threshold))\
            .assign(year=lambda d: d.review_date.dt.year, month=lambda d: d.review_date.dt.month)\
            .assign(date=lambda d: to_datetime({'year': d.year, 'month': d.month, 'day': 1}) + MonthEnd(0))\
            .drop(['review_date', 'year', 'month'], axis=1)\
            .reset_index(drop=True)

    date_idx = []
    for category in top10.category.unique():  # category
        for rating in range(1, 6): # rating from 1 to 5
            for date in date_range(start_date, end_date, freq='M'):  # months in given time
                date_idx.append((category, rating, date))

    data = top10.groupby(['category', 'star_rating', 'date'])[['id']].count()\
        .reindex(date_idx, fill_value=0)\
        .unstack(level=[0, 1])  # unstack to move indices to columns
    # drop the id column
    data.columns = data.columns.droplevel(level=0)
    # remove index name
    data.index.name = None

    return data.reset_index().to_json(orient='split')
