#!/usr/bin/env python
# -*- coding: utf-8 -*-  
#####################################################
#  
# File: skl_naive_bayes 
# Created: 2014-11-30 14:29:28
# Last Modified:  
#   
# Author: 杨秀隆 sndnyang <xiulong.yancey.yang@gmail.com>
#         sndnyang.github.io
# Description:
#  
#####################################################

from skl_get_data import prepare_data
from sklearn.metrics import accuracy_score

from sklearn.naive_bayes import GaussianNB

train_data, train_label, test_data = prepare_data()

clf = GaussianNB()

clf.fit(train_data[:500], train_label[:500])

part_pred = clf.predict(train_data[500:])

print accuracy_score(part_pred, train_label[500:])

pred = clf.predict(test_data)

print pred[:20]
