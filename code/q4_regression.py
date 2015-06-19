
import json
import datetime
import numpy as np
import statsmodels.api as sm
from sklearn.cross_validation import KFold, train_test_split

file_list = ['tweets_#gopatriots','tweets_#gohawks', 'tweets_#nfl', 'tweets_#patriots', 'tweets_#sb49', 'tweets_#superbowl']

for file in file_list:
    filename = '../data_new/'+file+'_features.csv'
    fd = open(filename, 'r')
    list_feature = np.loadtxt(fd, delimiter=',')
    y = list_feature[:,0]
    X = list_feature[:,1:5]

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

    print 'Average error of '+ file+': '+str(sum(total_error)/10)