#!/usr/bin/env python
# -*- coding: utf-8 -*-
#####################################################
#
# File: lsvm_method
# Created: 2015-06-06 12:45:23
# Last Modified:
#
# Author: 杨秀隆 sndnyang <xiulong.yancey.yang@gmail.com>
#         sndnyang.github.io
# Description:
#
#####################################################

import pandas as pd

if __name__ == '__main__':

    #train_features = pd.read_csv('train/train_features.csv')
    train_features = pd.read_csv('train/orig_feature.csv')

    columns = train_features.columns[2:]

    train_labels = train_features["drop"].values
    train_features = train_features[columns].values

    from sklearn.svm import LinearSVC as lsvc
    clf = lsvc()
    from sklearn.cross_validation import cross_val_score

    score = cross_val_score(clf, train_features, train_labels, cv=5, scoring='accuracy')
    print score

    clf.fit(train_features, train_labels)
    print "fit susscess"
    del train_features
    del train_labels

    #test_features = pd.read_csv('test/orig_feature.csv')
    test_features = pd.read_csv('test/test_features.csv')
    test_features = test_features.sort('enrollment_id')

    #columns = test_features.columns[2:]
    print columns

    fp = file('lsvm_submit.csv', 'w')
    prd = clf.predict(test_features[columns].values)
    for eid, cls in zip(test_features['enrollment_id'].values, prd):
        fp.write("%d,%d\n" % (eid, cls))

