from flask import Flask, request
import pandas as pd

app = Flask(__name__)

# Data Loading
df = pd.read_csv('./merged_amz-off_3.csv.gz',\
                 dtype={'customer_id': 'object', 'product_parent': 'object', \
                        'star_rating': 'Int64', 'helpful_votes':'Int64', 
                        'total_votes': 'Int64', \
                        'code': 'object'},
                 compression='gzip')
# convert reivew_date to datetime object
df.review_date = pd.to_datetime(df.review_date)
sub = df[(df.energy_100g.notna()) & (df.energy_100g < 3000) & 
         (df.salt_100g < 100) & (df.review_date.notna()) & 
         (df.main_category_en.notna()) & (df.main_category_en.str.contains('^[A-Z].*'))]\
        .loc[:, ['main_category_en', 'review_date', 'review_id']]\
        .rename(mapper={'main_category_en': 'category', 'review_id': 'id'}, axis=1)\
        .reset_index(drop=True)


def ridgeline_byDate(start_date, end_date, sub=sub):
    sub = sub[(sub.review_date > start_date) & (sub.review_date < end_date)]

    threshold = sub.groupby('category')[['id']].count()\
        .sort_values('id', ascending=False)\
        .iloc[9, 0]

    top10 = sub.assign(counts=lambda d: d.groupby('category')[['id']].transform('count'))\
            .query('counts >= {}'.format(threshold))\
            .reset_index(drop=True)

    date_idx = []
    for category in top10.category.unique():
        for date in pd.date_range(start_date, end_date, freq='D'):
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

@app.route('/api/dRidgeline') # served at /api/data
def export_data():
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')

    return ridgeline_byDate(start_date, end_date)

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
