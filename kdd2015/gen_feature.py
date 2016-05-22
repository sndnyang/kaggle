#!/usr/bin/env python
# -*- coding: utf-8 -*-
#####################################################
#
# File: gen_feature
# Created: 2015-06-06 11:39:16
# Last Modified:
#
# Author: 杨秀隆 sndnyang <xiulong.yancey.yang@gmail.com>
#         sndnyang.github.io
# Description:
#
#####################################################

import numpy as np
import pandas as pd

def get_course_info(courseinfo):
    courseinfo = courseinfo[courseinfo['category'] == 'chapter']
    course_lenth = courseinfo['course_id'].value_counts()
    course_lenth = pd.DataFrame({'course_id': course_lenth.index,
                                 'chapters':course_lenth.values},
                                 columns=['course_id', 'chapters'])
    return course_lenth

def get_person_info(personinfo):

    dropgroup = personinfo.groupby('username')
    dropgroup = 1.0 * dropgroup.sum() / dropgroup.count()

    persondrop = pd.DataFrame({'username': dropgroup.index,
                                 'droprate':dropgroup['drop'].values},
                                 columns=['username', 'droprate'])
    return persondrop



def gen_feature(feature, logsets):
    maps = {}
    for name, group in logsets.groupby('event'):
        tmp = group.groupby('enrollment_id').count()['event']
        maps[name] = tmp

    logdf = pd.DataFrame(maps,columns=['enrollment_id','nagivate','problem',
                                         'video', 'wiki', 'discussion',
                                         'access'])
    logdf['enrollment_id'] = logdf.index

    features = pd.merge(feature, logdf, on='enrollment_id', how='left')
    features = features.fillna(0)

    return features

if __name__ == "__main__":

    enrolltraincsv = 'train/enrollment_train.csv'
    enrolltestcsv = 'test/enrollment_test.csv'
    logtraincsv = 'train/log_train.csv'
    #logtraincsv = 'train/small_train.csv'
    objectcsv = 'object.csv'
    truthcsv = 'train/truth_train.csv'

    droptrain = pd.read_csv(truthcsv)

    courseinfo = pd.read_csv(objectcsv)
    courseinfo = get_course_info(courseinfo)

    enrolltrain = pd.read_csv(enrolltraincsv)
    print "read finish"

    enrolltrain = pd.merge(enrolltrain, courseinfo, on='course_id')
    enrolltrain = enrolltrain.loc[:, ['enrollment_id', 'chapters', 'username']]

    persondrop = enrolltrain.loc[:, ['username', 'drop']]
    persondrop = get_person_info(persondrop)
    train_features = pd.merge(enrolltrain, persondrop, on='username')
    train_features = train_features.loc[:, ['enrollment_id', 'chapters', 'droprate']]

    trainlog = pd.read_csv(logtraincsv)
    train_features = gen_feature(train_features, trainlog)
    print "feature finish"
    del trainlog

    logtestcsv = 'test/log_test.csv'
    #logtestcsv = 'test/small_test.csv'
    enrolltest = pd.read_csv(enrolltestcsv)
    enrolltest = pd.merge(enrolltest, courseinfo, on='course_id')
    enrolltest = enrolltest.loc[:, ['enrollment_id', 'chapters', 'username']]
    test_features = pd.merge(enrolltest, persondrop, how='left', on='username')
    test_features = test_features.loc[:, ['enrollment_id', 'chapters', 'droprate']]
    test_features.fillna(0)
    testlog = pd.read_csv(logtestcsv)

    test_features = gen_feature(test_features, testlog)

    features = pd.concat([train_features, test_features])
    for col in features.columns[4:]:
        features[col] = features[col] / features['chapters']
        maximum = features[col].max()
        features[col] = features[col] / maximum

    maximum = features['chapters'].max()
    features['chapters'] = features['chapters'] / maximum

    all_features = pd.merge(droptrain, features, on='enrollment_id', how='right')
    all_features['enrollment_id'] = all_features['enrollment_id'].astype(np.int64)
    del features
    print "merge finish"

    train_feature_filename = "train/train_features.csv"
    train_features = all_features[all_features['drop'].notnull()]
    print train_features['enrollment_id'].head()
    train_features.to_csv(train_feature_filename, index = False)

    test_feature_filename = "test/test_features.csv"
    test_features = all_features[all_features['drop'].isnull()]
    test_features.to_csv(test_feature_filename, index = False)

