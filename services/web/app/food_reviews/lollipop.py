# from json import dumps
from re import split

from collections import Counter
from nltk.corpus import stopwords

from app.utilities import get_dataframe_from_db

def get_data():

    query = \
    f"""
    SELECT 
        review_id, customer_id, review_body
    FROM 
        food_reviews
    WHERE 
        energy_100g IS NOT NULL
        AND energy_100g < 3000
        AND review_date >= '2010-01-01'
        AND verified_purchase LIKE 'Y'
    """

    data = get_dataframe_from_db(query)

    return data


def prepare_lollipop():

    df = get_data()
        .assign(review_times=lambda df: df.groupby('customer_id')[['review_id']].transform('count'))\
        .assign(binary=lambda df: df.review_times.apply(lambda d: 'once' if d == 1 else 'more'))

    stopWords = set(stopwords.words('english')) # 179 originally
    commonWords = ["br"]
    stopWords.update(commonWords)

    # build review strings by each group
    text_once = []
    text_more = []
    for row in df.itertuples():
        if (row.binary == 'once') & (row.review_body is not None):
            for word in split(r'\W+', row.review_body.lower()):
                if (word not in stopWords) & (word != ""): 
                    text_once.append(word)
        elif (row.binary == 'more') & (row.review_body is not None):
            for word in split(r'\W+', row.review_body.lower()):
                if (word not in stopWords) & (word != ""): 
                    text_more.append(word)
                    
    counterOnce = Counter(text_once)
    counterMore = Counter(text_more)

    # if output the percentage of a token
    pctOnce = sorted([(c, counterOnce[c] / len(text_once) * 100.0) for c in counterOnce], 
                    key=lambda d: d[1], reverse=True)
    pctMore = sorted([(c, counterMore[c] / len(text_more) * 100.0) for c in counterMore], 
                    key=lambda d: d[1], reverse=True)

    d = {'once': [{'word': w, 'value': v} for (w, v) in pctOnce], 
        'more': [{'word': w, 'value': v} for (w, v) in pctMore] }

    return json.dumps(d)

