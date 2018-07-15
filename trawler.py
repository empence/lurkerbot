from app import db, User, Alert, Subreddit,Phrase
import time
import os
import praw
from datetime import datetime

def main():
    CLIENT_ID = os.environ['REDDIT_CLIENT_ID']
    CLIENT_SECRET = os.environ['REDDIT_CLIENT_SECRET']
    REDDIT_USERNAME = os.environ['REDDIT_USERNAME']
    REDDIT_PASSWORD = os.environ['REDDIT_PW']
    reddit = praw.Reddit(user_agent="LurkerBot v0.1", client_id=CLIENT_ID, client_secret=CLIENT_SECRET, username=REDDIT_USERNAME, password=REDDIT_PASSWORD)
    now = int(datetime.utcnow().timestamp())
    #iterate through all the alerts that we have
    for alert in Alert.query.all():        
        for subreddit in Subreddit.query.filter_by(alert=alert.id): 
            for phrase in Phrase.query.filter_by(alert=alert.id).all():
                """ 
                 There is a correctness issue here: if a user makes a query for 
                 which there are more than 1000 results for a single subreddit 
                 in the last hour, then the 1000st and upward items will just...
                 not show up. This is, however, really unlikely, as when I 
                 searched "the" in r/all over the last hour, there were only 
                 ~300 results. 
                 Doing only one subreddit at a time helps prevent this, unlikely
                 as it is. 
                """
                i = 0
                for submission in reddit.subreddit(subreddit.subreddit).search(query=phrase.phrase,sort='new', limit=None):
                    if i == 1: 
                        last_seen = submission.fullname
                    i+=1
                    if submission.fullname != alert.last_seen: 
                        reddit.redditor(User.query.get(alert.user_id).username)
                        print("Hello " + str(User.query.get(alert.user_id).username) + "! LurkerBot found a mention of the phrase", str(phrase.phrase), "and since you set up an alert for that phrase, you're getting a message about it. Take a look:", submission.shortlink)
                    else: 
                    # we've gone backward into posts we've already looked at, 
                    # we should stop and move onto the next phrase. 
                        break
                alert.last_seen = last_seen
    db.session.commit()
if __name__ == "__main__":
    main()
