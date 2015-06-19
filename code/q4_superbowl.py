
import json
import datetime
import numpy as np
import matplotlib.pyplot as plt

file_list = ['gopatriots','gohawks', 'nfl', 'patriots', 'sb49', 'superbowl']

for file in file_list:
    filename = '../data_new/tweets_#'+file+'.txt'
    fd = open(filename, 'r')


    linecount = 1

    begin_superbowl = datetime.datetime(2015,2,1, 8, 0)
    superbowl_end = datetime.datetime(2015, 2,1,20,0)
    print begin_superbowl
    print superbowl_end

    file_1 = '../data_new/pre_'+file+'.txt'
    fd1 = open(file_1,'w')
    file_2 = '../data_new/during_'+file+'.txt'
    fd2 = open(file_2,'w')
    file_3 = '../data_new/post_'+file+'.txt'
    fd3 = open(file_3,'w')

    print 'Reading tweets from '+filename+'...'
    for line in fd:
        input_tweet = json.loads(line)
        linecount = linecount + 1
        json_object = json.dumps(input_tweet)
        stime = datetime.datetime.fromtimestamp(input_tweet["firstpost_date"])

        if(stime< begin_superbowl):
            fd1.write(json_object+"\n")
        elif stime>=begin_superbowl and stime<superbowl_end:
            fd2.write(json_object+"\n")
        elif(stime>=superbowl_end):
            fd3.write(json_object+"\n")

        if linecount%10000 == 0:
            print 'Read '+ str(linecount)+' tweets...'