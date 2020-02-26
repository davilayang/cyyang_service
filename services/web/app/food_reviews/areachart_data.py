# web/app/food_reviews/areachart_data.py

from app.utilities import get_dataframe_from_db

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

def prepare_areachart_data():

    """
    """


    return 