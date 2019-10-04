from flask import Flask, request
from flask import jsonify
import pandas as pd
import json

app = Flask(__name__)

df = pd.read_csv('merged_amz-off_3.csv.gz',\
                 dtype={'customer_id': 'object', 'product_parent': 'object', \
                        'star_rating': 'Int64', 'helpful_votes': 'Int64', 
                        'total_votes': 'Int64', \
                        'code': 'object'},
                 compression='gzip')
# convert reivew_date to datetime object
df.review_date = pd.to_datetime(df.review_date)

df = df[(df.energy_100g.notna()) & (df.energy_100g < 3000) & 
          (df.salt_100g < 100) & (df.review_date.notna())]\
        .loc[:, ['main_category_en', 'review_date', 'review_id']]

df = df[(df.main_category_en.notna()) & (df.main_category_en.str.contains('^[A-Z].*'))]\
        .assign(counts=lambda d: d.groupby('main_category_en')[['review_id']].transform('count'))\
        .query('counts >= 180')\
        .reset_index(drop=True)


def query_by_date(start_date, end_date):
    start_value = json.loads(pd.Series(pd.Timestamp(start_date)).to_json())['0']
    end_value = json.loads(pd.Series(pd.Timestamp(end_date)).to_json())['0']

    sub = df[(df.review_date > start_date) & (df.review_date < end_date)]

    idx = []
    for category in sub.main_category_en.unique():
        for date in pd.date_range(start_date, end_date, freq='D'):
            idx.append((category, date))

    data = sub.groupby(['main_category_en', 'review_date'])[['review_id']].count()\
        .reindex(idx, fill_value=0)\
        .reset_index()\
        .assign(m_sum=lambda d: d.groupby('main_category_en')[['review_id']].transform('sum'))\
        .assign(p=lambda d: d.review_id / d.m_sum)\
        .drop(['review_id', 'm_sum'], axis=1)\
        .assign(max_p=lambda d: d.groupby('main_category_en')[['p']].transform(max))\
        .assign(p_peak=lambda d: d.p / d.max_p).drop('max_p', axis=1)\
        .assign(p_lag=lambda d: d.groupby('main_category_en')[['p_peak']].shift(-1))\
        .assign(p_lead=lambda d: d.groupby('main_category_en')[['p_peak']].shift(1))\
        .assign(p_smooth=lambda d: (d.p_lag + d.p_peak + d.p_lead) / 3)\
        .drop(['p_lag', 'p_lead'], axis=1)\
        .fillna(method='ffill', axis=1)\
        .rename(mapper={'main_category_en': 'activity', 'review_date': 'time'}, axis=1)

    data = json.loads(data.to_json(orient='records'))
    for d in data:
        d['time'] = round((d['time'] - start_value)/ ((end_value - start_value) / 1440.0), 2)

    return data

@app.route('/api/data') # served at /api/data
def export_data():
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')

    return json.dumps(query_by_date(start_date, end_date))

# def hello_world():
#     data = [{
#             'activity': 'Running',
#             'time': 1440.0,
#             'p': 6.45223543281662e-5,
#             'p_peak': 0.04402262110550772,
#             'p_smooth': 0.04402262110550772,
#         },
#         {        
#             'activity': 'Playing racquet sports',
#             'time': 1440.0,
#             'p': 0.0,
#             'p_peak': 0.0,
#             'p_smooth': 0.0
#         }
#     ]
#     return jsonify(data)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001, debug=True)
