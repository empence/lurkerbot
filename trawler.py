from app import db, User, Alert, Subreddit,Phrase
import time
import os
import atexit
import praw


def get_date(submission):
    time = submission.created
    return datetime.datetime.fromtimestamp(time)


def main():
    #getting secrets for connecting to Reddit via environment variable
    CLIENT_ID = os.environ['REDDIT_CLIENT_ID']
    CLIENT_SECRET = os.environ['REDDIT_CLIENT_SECRET']
    REDDIT_USERNAME = os.environ['REDDIT_USERNAME']
    REDDIT_PASSWORD = os.environ['REDDIT_PW']

    reddit = praw.Reddit(user_agent="LurkerBot v0.1", client_id=CLIENT_ID, client_secret=CLIENT_SECRET, username=REDDIT_USERNAME, password=REDDIT_PASSWORD)

    for alert in Alert.query.all():        
        subreddits = '+'.join(Subreddit.query.filter_by(alert=alert).all())
        for submission in reddit.subreddit(subreddits).submissions(start=alert.last_checked):
            for phrase in Phrase.query.filter_by(alert=alert).all():
                if phrase.lower() in submission.selftext.lower():
                    print("Hello " + str(User.query.get(alert.user_id).username) + "! LurkerBot found a mention of the phrase", str(phrase), "and since you set up an alert for that phrase, you're getting a message about it. Take a look:" submission.shortlink())


if __name__ == "__main__":
    main()
