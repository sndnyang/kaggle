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

import xgboost as xgb

if __name__ == '__main__':
    
    dtrain = xgb.DMatrix("train.buffer")
    param = {'bst:max_depth':2, 'bst:eta':1, 'silent':1, 'objective':'binary:logistic' }
    param['nthread'] = 4
    
    num_round = 10
    print xgb.cv( param, dtrain, num_round, nfold=5,
       metrics={'error'}, seed = 0 )
    
    
    """test_features = pd.read_csv('test/orig_feature.csv')
    test_features = pd.read_csv('test/test_features.csv')
    
    test_features = test_features.sort('enrollment_id')
    columns = test_features.columns[2:]
    test_features[columns].values
    
    #
    print columns

    fp = file('lsvm_submit.csv', 'w')
    prd = clf.predict(test_features[columns].values)
    for eid, cls in zip(test_features['enrollment_id'].values, prd):
        fp.write("%d,%d\n" % (eid, cls))"""

