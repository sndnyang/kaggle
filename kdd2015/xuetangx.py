#!/usr/bin/env python
# -*- coding: utf-8 -*-  
#####################################################
#  
# File: xuetangx 
# Created: 2015-06-05 19:47:14
# Last Modified:  
#   
# Author: 杨秀隆 sndnyang <xiulong.yancey.yang@gmail.com>
#         sndnyang.github.io
# Description:
#  
#####################################################

import pandas as pd

def get_course_info(courseinfo):
    courseinfo = courseinfo[courseinfo['category'] == 'chapter']
    course_lenth = courseinfo['course_id'].value_counts()
    course_lenth = pd.DataFrame({'course_id': course_lenth.index, 
                                 'chapters':course_lenth.values}, 
                                 columns=['course_id', 'chapters'])
    return course_lenth

def gen_feature(feature, logsets):
    maps = {}
    for name, group in logsets.groupby('event'):
        tmp = group.groupby('enrollment_id').count()['event']
        maps[name] = tmp

    logtrain = pd.DataFrame(maps,columns=['enrollment_id','nagivate','problem',
                                         'video', 'wiki', 'discussion', 
                                         'access'])
    logtrain['enrollment_id'] = logtrain.index

    features = pd.merge(feature, logtrain, on='enrollment_id')
    features = features.fillna(0)

    for col in features.columns[3:]:
        features[col] = features[col] / features['chapters']
        avg = features[col].mean()
        features[col] = (features[col]-avg) / avg
        
#   print features.head()
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
    trainlog = pd.read_csv(logtraincsv)
    print "read finish"

    enrolltrain = pd.merge(enrolltrain, courseinfo, on='course_id')
    enrolltrain = enrolltrain.loc[:, ['enrollment_id', 'chapters']]

    train_features = gen_feature(enrolltrain, trainlog)
    print "feature finish"
    del trainlog
   #print train_features.head()

    train_features = pd.merge(droptrain, train_features, on='enrollment_id')
    print "merge finish"

    columns = train_features.columns[2:]

    train_labels = train_features["drop"].values
    train_features = train_features[columns].values

    from sklearn.naive_bayes import GaussianNB as gnb
    clf = gnb()

  # from sklearn.svm import SVC
  # clf = SVC(kernel='linear', C=100)
    from sklearn.cross_validation import cross_val_score

    score = cross_val_score(clf, train_features, train_labels, cv=5, scoring='f1')
    print score
    print "begin to fit"

    clf.fit(train_features, train_labels)
    print "fit susscess"
    del train_features
    del train_labels

    logtestcsv = 'test/log_test.csv'
    #logtestcsv = 'test/small_test.csv'
    enrolltest = pd.read_csv(enrolltestcsv)
    enrolltest = pd.merge(enrolltest, courseinfo, on='course_id')
    enrolltest = enrolltest.loc[:, ['enrollment_id', 'chapters']]

    testlog = pd.read_csv(logtestcsv)

    test_features = gen_feature(enrolltest, testlog)
    del testlog

    columns = test_features.columns[1:]

    fp = file('submit.csv', 'w')
    prd = clf.predict(test_features[columns].values)
    for eid, cls in zip(test_features['enrollment_id'].values, prd):
        fp.write("%d,%d\n" % (eid, cls))


