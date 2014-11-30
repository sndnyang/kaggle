#!/usr/bin/env python
# -*- coding: utf-8 -*-  
#####################################################
#  
# File: skl_get_data 
# Created: 2014-11-30 14:33:08
# Last Modified:  
#   
# Author: 杨秀隆 sndnyang <xiulong.yancey.yang@gmail.com>
#         sndnyang.github.io
# Description:
#  
#####################################################

import numpy as np

def prepare_data():
    train_data = np.loadtxt(fname = './train.csv', delimiter = ',')

    test_data = np.loadtxt(fname = './test.csv', delimiter = ',')

    train_label = np.loadtxt(fname = './trainLabels.csv', dtype='int', delimiter = ',')

    print train_label.shape

    return train_data, train_label, test_data

prepare_data()
