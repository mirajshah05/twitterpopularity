import json
import datetime
import numpy as np
import statsmodels.api as sm

file_list = ['tweets_#gopatriots.txt','tweets_#gohawks.txt', 'tweets_#nfl.txt', 'tweets_#patriots.txt', 'tweets_#sb49.txt', 'tweets_#superbowl.txt']

for filename in file_list:
    filename = '../data_new/'+filename
    fd = open(filename, 'r')

    timestats = {};
    user_followers = {};
    num_retweet = {};

    hourgap = datetime.timedelta(hours=1)
    hourno = 1

    ftweet = json.loads(fd.next())
    fhour = datetime.datetime.fromtimestamp(ftweet["firstpost_date"])
    time_ahead = datetime.timedelta(minutes=fhour.minute, seconds=fhour.second)
    fhour = fhour-time_ahead


    timestats[hourno] = 1
    user_followers[ftweet['tweet']['user']['id']] = ftweet['tweet']['user']['followers_count']
    num_retweet[ftweet['tweet']['id']] = ftweet['tweet']['retweet_count']
    next_hour = fhour
    first_no = fhour.hour

    list_feature1 = np.matrix([1,ftweet['tweet']['user']['followers_count'] , ftweet['tweet']['retweet_count'], ftweet['tweet']['user']['followers_count'], fhour.hour])
    linecount = 1
    sum_followers = sum_retweet = 0
    max_followers = 0

    print '\nReading tweets from '+filename+'...'
    for line in fd:
        tweet = json.loads(line)
        linecount = linecount + 1

        timestamp_val = datetime.datetime.fromtimestamp(tweet["firstpost_date"])
        user_id = tweet['tweet']['user']['id']
        no_of_followers = tweet['tweet']['user']['followers_count']
        tweet_id = tweet['tweet']['id']
        rt_count = tweet['tweet']['retweet_count']

        if(next_hour+hourgap>timestamp_val):
            timestats[hourno] = timestats[hourno] + 1
            sum_followers = sum_followers + no_of_followers
            sum_retweet = sum_retweet + rt_count
            if no_of_followers > max_followers:
                max_followers = no_of_followers
            list_feature1[hourno-1] = np.matrix([timestats[hourno],sum_followers, sum_retweet, max_followers, (first_no + (hourno-1))%24])

        else:
            while(next_hour+hourgap<timestamp_val):
                hourno = hourno+1
                timestats[hourno] = 0
                sum_followers = sum_retweet = 0
                max_followers = 0
                next_hour = next_hour + hourgap
                list_feature1 = np.concatenate([list_feature1, np.matrix([timestats[hourno],sum_followers, sum_retweet, max_followers, (first_no + (hourno-1))%24 ])])

            timestats[hourno] = timestats[hourno]+ 1
            list_feature1[hourno-1] = np.matrix([timestats[hourno], sum_followers, sum_retweet, max_followers,(first_no + (hourno-1))%24])

        if not user_followers.has_key(user_id):
            user_followers[user_id] = no_of_followers
        num_retweet[tweet_id] = rt_count

        if linecount%10000 == 0:
            print 'Read '+ str(linecount)+' tweets...'

    y = list_feature1[:,0]
    X = list_feature1[:,1:5]
    X = sm.add_constant(X)
    mod = sm.OLS(y,X)
    res = mod.fit()
    print res.summary()
    print res.pvalues

