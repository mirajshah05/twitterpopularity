
import json
import datetime
import numpy as np
import statsmodels.api as sm
from sklearn.cross_validation import KFold, train_test_split

file_list = ['pre_gopatriots_features.csv','during_gopatriots_features.csv','post_gopatriots_features.csv',
             'pre_gohawks_features.csv','during_gohawks_features.csv','post_gohawks_features.csv',
             'pre_nfl_features.csv','during_nfl_features.csv', 'post_nfl_features.csv',
             'pre_patriots_features.csv','during_patriots_features.csv','post_patriots_features.csv',
             'pre_sb49_features.csv','during_sb49_features.csv','post_sb49_features.csv',
             'pre_superbowl_features.csv','during_superbowl_features.csv', 'post_superbowl_features.csv']
average_error = [];
count = 0

for file in file_list:
    count = count+1
    file = '../data_new/'+file
    fd = open(file, 'r')
    list_features = np.loadtxt(fd, delimiter=',')
    y = list_features[:,0]
    X = list_features[:,1:5]

    total_error = [];

    kf = KFold(np.shape(X)[0], n_folds=10)
    for train,test in kf:
        X_train = X[train]
        y_train = y[train]

        X_test = X[test]
        y_test = y[test]

        mod = sm.OLS(y_train, X_train)
        res = mod.fit()
        params = res.params
        predicted = res.predict(X_test)
        total_error.append(np.mean(abs(y_test-predicted)))
    average_error.append(sum(total_error)/10)
    if(count%3 == 0):
        print '\nAverage errors of 3 sets:'+ str(average_error)
        average_error = [];