
import json
import datetime
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

file_list = ['tweets_#gopatriots','tweets_#gohawks', 'tweets_#nfl', 'tweets_#patriots', 'tweets_#sb49', 'tweets_#superbowl']
#file_list = ['pre_gopatriots','during_gopatriots', 'post_gopatriots', 'pre_gohawks', 'during_gohawks', 'post_gohawks','pre_nfl', 'during_nfl', 'post_nfl', 'pre_patriots', 'during_patriots', 'post_patriots','pre_sb49', 'during_sb49', 'post_sb49', 'pre_superbowl', 'during_superbowl', 'post_superbowl']
#file_list = ['sample1_period1','sample2_period2','sample3_period3','sample4_period1','sample5_period1', 'sample6_period2',
             #'sample7_period3', 'sample8_period1','sample9_period2','sample10_period3']
for file in file_list:
    filename = '../data_new/'+file+'.txt'
    fd = open(filename, 'r')


    interval = datetime.timedelta(hours=1)

    stats_hr = {};
    hourno = 1

    ftweet = json.loads(fd.next())
    fhour = datetime.datetime.fromtimestamp(ftweet["firstpost_date"])
    ahead_time = datetime.timedelta(minutes=fhour.minute, seconds=fhour.second)
    fhour = fhour-ahead_time


    stats_hr[hourno] = 1
    next_hour = fhour
    first_no = fhour.hour

    feature_array = np.matrix([1,len(ftweet['tweet']['entities']['user_mentions']) , ftweet['tweet']['user']['statuses_count'], ftweet['tweet']['user']['followers_count'], ftweet['tweet']['retweet_count']])
    linecount = 1
    total_follow = sum_statuses = sum_retweets = sum_mentions = 0

    print 'Reading tweets...'
    for line in fd:
        tweet = json.loads(line)
        linecount = linecount + 1

        stime = datetime.datetime.fromtimestamp(tweet["firstpost_date"])
        num_retweets = tweet['tweet']['retweet_count']
        num_mentions = len(tweet['tweet']['entities']['user_mentions'])
        num_statuses = tweet['tweet']['user']['statuses_count']
        num_followers = tweet['tweet']['user']['followers_count']

        if(next_hour+interval>stime):
            stats_hr[hourno] = stats_hr[hourno] + 1
            sum_retweets = sum_retweets + num_retweets
            sum_mentions = sum_mentions + num_mentions
            sum_statuses = sum_statuses + num_statuses
            total_follow = total_follow + num_followers

            feature_array[hourno-1] = np.matrix([stats_hr[hourno],sum_mentions,  sum_statuses, total_follow, sum_retweets])

        else:
            while(next_hour+interval<stime):
                hourno = hourno+1
                stats_hr[hourno] = 0
                sum_mentions = sum_retweets = sum_statuses = total_follow = 0
                next_hour = next_hour + interval
                feature_array = np.concatenate([feature_array, np.matrix([stats_hr[hourno], sum_mentions,  sum_statuses, total_follow, sum_retweets])])

            stats_hr[hourno] = stats_hr[hourno]+ 1
            feature_array[hourno-1] = np.matrix([stats_hr[hourno], sum_mentions,  sum_statuses, total_follow, sum_retweets])

        if linecount%10000 == 0:
            print 'Read '+ str(linecount)+' tweets...'

    output_file = '../data_new/'+file+'_features.csv'
    np.savetxt(output_file, feature_array, delimiter=',')
    y = feature_array[:,0]
    X = feature_array[:,1:5]
    X = sm.add_constant(X)
    mod = sm.OLS(y, X)
    res = mod.fit()
    print res.summary()
    print '\nP values :'+str(res.pvalues)
    print 'R squared value = ' + str(res.rsquared)

    #ScatterPlot - 1
    plt.scatter(feature_array[:,1], feature_array[:,0], marker='*')
    plt.xlabel('Total no. of mentions per hour')
    plt.ylabel('No. of tweets per hour')
    plt.title('No. of tweets per hour vs Total no. mentions per hour')
    plt.show()

    #ScatterPlot - 2
    plt.scatter(feature_array[:,2], feature_array[:,0], color='green', marker='*')
    plt.xlabel('Total tweets of user per hour')
    plt.ylabel('No. of tweets per hour')
    plt.title('No. of tweets per hour vs Total tweets of user per hour')
    plt.show()

    #ScatterPlot - 3
    plt.scatter(feature_array[:,3], feature_array[:,0], color='red', marker='*')
    plt.xlabel('Total no. of followers per hour')
    plt.ylabel('No. of tweets per hour')
    plt.title('No. of tweets per hour vs Total no. of followers per hour')
    plt.show()
