# web/app/food_reviews/heatmap_time_of_review

from app.utilities import get_dataframe_from_db
from json import dumps


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
        customer_id, review_id, review_date
    FROM 
        food_reviews
    WHERE 
        verified_purchase LIKE 'Y'
        AND review_date IS NOT NULL
        AND review_date BETWEEN '{start_date}' AND '{end_date}'
    ORDER BY
        review_date
    """

    data = get_dataframe_from_db(query)

    return data


def heatmap_data(df)

    """
    heatmap_data
    
    Args:
        df (pandas DataFrame):

    Returns:


    """

    df.loc[:, 'review_times'] = (
        df.groupby('customer_id')[['review_id']].transform('count')
    )

    d = {}
    # data from 2 groups to 5 groups
    for n_groups in range(2, 6): 
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
        
        # export data
        d[n_groups] =  {'weekday': d1.to_dict(orient ='records'), 
                        'monthday': d2.to_dict(orient ='records')}

    # return dumps(d)
    return d