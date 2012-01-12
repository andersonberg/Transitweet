'''
Created on 03/11/2011

@author: Anderson Berg
@author: Saulo
'''

from __future__ import division

import twitter
import sys
from twitter import Status, TwitterError
import time
import csv

def getTweets(user, countLimit=None, since_id=None):
    
    api = twitter.Api()
    user_tweets = []
    statusSequenceList = []

    # TODO - countLimit must be used to limit results fetched by the crawler
    
    resultCount = 0
    statusSequence = []
    i = int(0);
    oldestTweetId = "";
    while i < 150:
        try:
            print "Fetching tweets..."
            statusSequence = api.GetUserTimeline(screen_name=user, since_id=None, count=200, page=i, include_rts=True)
            
            
            if (len(statusSequence) < 1):
                print "No more results."
                break;
            
            else:
                i = i + 1
                resultCount += len(statusSequence)
                print "Success! Current page: " + str(i)
                statusSequenceList.append(statusSequence)
                print "Fetched " + str(resultCount) + " tweets."
                
        except TwitterError, e:
            print "Request failed. Error message: " + str(e)
            time.sleep(30);
            print "Retrying..."
            pass

    filename = user + "-" + str(resultCount) + "_timeline.txt"
    resultFile = open(filename, 'w')
    
    for statusSequence in statusSequenceList:
        for status in statusSequence:
            dateString = str(status.created_at.encode('utf-8') + '\t')
            textString = str(status.text.encode('utf-8') + '\n')
            resultFile.write(dateString + textString)
            user_tweets.append(textString)
            oldestTweetId = str(status.id)

    resultFile.write(oldestTweetId)
    resultFile.close()


def main():
    args = sys.argv[1:]

    if not args:
        print 'usage: python crawler.py username countLimit [id]'
        sys.exit(1)

    user = sys.argv[1]
    countLimit=None
    since_id=None
    if (len(sys.argv) > 2):
        countLimit = sys.argv[2]
    if (len(sys.argv) > 3):
        since_id = sys.argv[3]

    getTweets(user, countLimit, since_id)


if __name__ == '__main__':
    main()