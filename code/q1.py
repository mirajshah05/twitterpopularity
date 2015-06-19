
import json
import datetime
import numpy as np
import matplotlib.pyplot as plt

file_list = ['tweets_#gopatriots.txt','tweets_#gohawks.txt', 'tweets_#nfl.txt', 'tweets_#patriots.txt', 'tweets_#sb49.txt', 'tweets_#superbowl.txt']

for filename in file_list:

    filename = '../data_new/'+filename
    fd = open(filename, 'r')

    stats_hr = {};
    stats_followers = {};
    stats_retweet = {};

    hourgap = datetime.timedelta(hours=1)
    hour_number = 1


    ftweet = json.loads(fd.next())
    first_hour = datetime.datetime.fromtimestamp(ftweet["firstpost_date"])
    time_ahead = datetime.timedelta(minutes=first_hour.minute, seconds=first_hour.second)
    fhour = fhour-time_ahead

    stats_hr[hour_number] = 1
    stats_followers[ftweet['tweet']['user']['id']] = ftweet['tweet']['user']['followers_count']
    next_hour = fhour

    linecount = 1

    print '\nReading tweets from '+filename+'...'
    for line in fd:
        tweet = json.loads(line)
        linecount = linecount + 1

        timestamp_val = datetime.datetime.fromtimestamp(tweet["firstpost_date"])
        user_id = tweet['tweet']['user']['id']
        no_of_followers = tweet['tweet']['user']['followers_count']

        if(next_hour+hourgap>timestamp_val):
            stats_hr[hour_number] = stats_hr[hour_number] + 1
        else:
            while(next_hour+hourgap<timestamp_val):
                hour_number = hour_number+1
                stats_hr[hour_number] = 0
                next_hour = next_hour + hourgap
            stats_hr[hour_number] = stats_hr[hour_number]+ 1

        if not stats_followers.has_key(user_id):
            stats_followers[user_id] = no_of_followers

        stats_retweet[tweet['tweet']['id']] = tweet['tweet']['retweet_count']
        if linecount%10000 == 0:
            print 'Read '+ str(linecount)+' tweets...'

    sum=count=0
    for key in stats_hr:
        sum = sum+ stats_hr[key]
        count=count+1
    print '\nAverage no. of tweets per hour: '+str(float(sum)/float(count))


    sum=count=0
    for user in stats_followers:
        sum=sum+stats_followers[user]
        count=count+1
    print 'Average no. of followers/user: '+str(float(sum)/float(count))


    sum=count=0
    for tweet in stats_retweet:
        sum = sum+stats_retweet[tweet]
        count=count+1
    print 'Average no. of retweets/tweet: '+str(float(sum)/float(count))


    tweetcount = np.array(stats_hr.values())
    tweethours = np.array(stats_hr.keys())
    plt.bar(tweethours,tweetcount)
    plt.xlabel('Hour')
    plt.ylabel('No. of tweets ')
    plt.title('No. of tweets per hour')
    plt.show()

