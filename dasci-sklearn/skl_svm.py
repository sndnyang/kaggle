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
from sklearn import cross_validation as cv

from sklearn.svm import SVC 

train_data, train_label, test_data = prepare_data()

clf = SVC(kernel="linear", C=1)


scores = cv.cross_val_score(clf, train_data, train_label, cv=5)
print scores

#part_pred = clf.predict(train_data[800:])

#print accuracy_score(part_pred, train_label[800:])

clf.fit(train_data, train_label)
pred = clf.predict(test_data)

f=open('result.csv','w')

f.write('Id,Solution\n')

count=1

for x in pred:
    f.write('%d,%d\n' % (count,x))
    count += 1

f.close()
