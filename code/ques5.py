
import json
import datetime
import numpy as np
import statsmodels.api as sm

arrayresult = [];
file_list = ['pre_superbowl_features.csv','during_superbowl_features.csv', 'post_superbowl_features.csv']

sample_tests_1 = ['sample1_period1_features.csv','sample4_period1_features.csv','sample5_period1_features.csv','sample8_period1_features.csv']
sample_tests_2 = ['sample2_period2_features.csv','sample6_period2_features.csv','sample9_period2_features.csv']
sample_tests_3 = ['sample3_period3_features.csv', 'sample7_period3_features.csv', 'sample10_period3_features.csv']

for file in file_list:
    file = '../data_new/'+file
    fd = open(file, 'r')
    feature_list = np.loadtxt(fd, delimiter=',')
    X = feature_list[:,1:5]
    y = feature_list[:,0]


    mod = sm.OLS(y, X)
    res = mod.fit()
    arrayresult.append(res)

for file in sample_tests_1:
    filename='../test_new/'+file
    fd = open(filename, 'r')
    feature_list = np.loadtxt(fd, delimiter=',')
    y_test = feature_list[:,0]
    X_test = feature_list[:,1:5]

    predicted = arrayresult[0].predict(X_test)
    print file+' predicted values: '+ str(predicted)

for file in sample_tests_2:
    filename='../test_new/'+file
    fd = open(filename, 'r')
    feature_list = np.loadtxt(fd, delimiter=',')
    y_test = feature_list[:,0]
    X_test = feature_list[:,1:5]

    predicted = arrayresult[1].predict(X_test)
    print file+' predicted values: '+ str(predicted)

for file in sample_tests_3:
    filename='../test_new/'+file
    fd = open(filename, 'r')
    feature_list = np.loadtxt(fd, delimiter=',')
    y_test = feature_list[:,0]
    X_test = feature_list[:,1:5]

    predicted = arrayresult[2].predict(X_test)
    print file+' predicted values: '+ str(predicted)
