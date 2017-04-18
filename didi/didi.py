import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandasql as pql
from datetime import datetime


# 训练集数据文件夹
base_dir = "G:/project/dataset/didi/season_1/training_data"

train_cluster_map_file = os.path.join(base_dir, 'cluster_map', 'cluster_map')

# 这个 POI 不打算使用
train_poi_file = os.path.join(base_dir, 'poi_data', 'poi_data')

# 训练集的 gap 中间文件
train_sd_gap_file = os.path.join(base_dir, 'sd_gap.csv')

# 训练集的 order 中间文件
train_order_file = os.path.join(base_dir, 'order_data', 'order_data.csv')

train_weather_file = os.path.join(base_dir, 'weather_data', 'weather_data.csv')

train_traffic_file = os.path.join(base_dir, 'traffic_data', 'traffic-data.csv')

# test data directory
test_base_dir = "G:/project/dataset/didi/season_1/test_set_1"

test_traffic_file = os.path.join(base_dir, 'traffic_data', 'traffic-data.csv')
test_order_file = os.path.join(test_base_dir, 'order_data', 'order-data.csv')

test_submit_file = os.path.join(test_base_dir, 'test.txt')

test_weather_file = os.path.join(test_base_dir, 'weather_data', 'weather_data.csv')

# 全部交通数据
all_traffic_file = os.path.join(base_dir, '..', 'all_traffic.csv')

sd_gap_file = os.path.join(base_dir, '..', 'gap.csv')

weather_file = os.path.join(test_base_dir, '..', 'weather_data.csv')

another_weather = os.path.join(test_base_dir, '..', 'weather.txt')
full_index_file = os.path.join(base_dir, '..', 'fullindex.csv')

full_file = os.path.join(base_dir, '..', 'full_data.csv')

# 提交文件
submit_file = os.path.join(test_base_dir, '..', 'submit.csv')
result_file = os.path.join(test_base_dir, '..', 'result.csv')


all_data_df = pd.read_csv(full_file, dtype = {'id': np.int16, 'TimePiece': np.int16, 'demand': np.double, 
                                                'supply': np.double, 'gap': np.double, 'week': np.int8, 
                                                 'work': np.bool, 'traffic': np.double, 'Weather': np.int8})


def evaluate_mape(df):
    temp = df.apply(lambda s: 1.0 * abs(s['gap'] - s['prd_gap']) / s['gap'] if s['gap'] > 0 else 0, axis=1)
    return temp.mean()

def evaluate_gap(df):
    return (df['gap'] - df['prd_gap']).abs().sum()

def predict_evaluate():
    sampled_df = all_data_df[all_data_df.gap.notnull() & all_data_df.Weather.notnull() & all_data_df.traffic.notnull()]
    
    #sampled_df = sampled_df.loc[:, ['id', 'Date', 'TimePiece', 'gap', 'week', 'work']]
    result_df = sampled_df.sample(100).loc[:, ['id', 'Date', 'TimePiece', 'gap', 'week', 'work']]

    import time
    start = time.time()
    result_df['prd_gap'] = pd.DataFrame({'prd_gap': 
                                         result_df.apply(lambda s: 
                                                         train(sampled_df, train_data, train_data, s), axis=1)})
    
    print 'mape', evaluate_mape(result_df)
    print 'gap', evaluate_gap(result_df)
    print 'time', time.time() - start
    
predict_evaluate()