#!/usr/bin/env python
# -*- coding: utf-8 -*-
#####################################################
#
# File: nb_method
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

    train_features = pd.read_csv('train/train_features.csv')

    columns = train_features.columns[3:]

    train_labels = train_features["drop"].values
    train_features = train_features[columns].values

    from sklearn.naive_bayes import GaussianNB as gnb
    clf = gnb()
    from sklearn.cross_validation import cross_val_score
    from sklearn.cross_validation import train_test_split

    score = cross_val_score(clf, train_features, train_labels, cv=5, scoring='accuracy')
    print score
    #X_train, X_test, y_train, y_test = train_test_split(train_features, train_labels, test_size=0.4, random_state=1)


    #clf.fit(train_features, train_labels)
    #clf.fit(X_train, y_train)
    #print clf.score(X_test, y_test)
    #print "fit susscess"
    del train_features
    del train_labels
"""
    test_features = pd.read_csv('test/test_features.csv')
    test_features = test_features.sort('enrollment_id')

    #print columns

    fp = file('nb_submit.csv', 'w')
    prd = clf.predict(test_features[columns].values)
    for eid, cls in zip(test_features['enrollment_id'].values, prd):
        fp.write("%d,%d\n" % (eid, cls))
"""
