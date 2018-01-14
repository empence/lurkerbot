import time
import os
import atexit
import cPickle as pickle

import praw
seen_posts = set()
if os.path.exists("seen.pkl"):
    with open("seen.pkl", "rb") as data_file:
        seen_posts = pickle.load(data_file)

@atexit.register
def save_seen_posts(): 
    with open("seen.pkl", "wb") as f:
        pickle.dump(seen_posts, f)


reddit = praw.Reddit(user_agent="LurkerBot v0.1", client_id="A9j7FoKo5pwa3Q", client_secret="G9EOvmf5bXxzNLvUePLixKQ-NDE", username="downloadablerice", password="bM1xoOr2s09f")
subreddit = reddit.subreddit("makeupexchange")
str_to_find = "the"
for submission in subreddit.stream.submissions():
    if str_to_find in submission.selftext.lower():
        print(submission.title)
        print("-------------------------------")

# subreddit = bot.subreddit("makeupexchange")
# for comment in subreddit.stream.comments():
#     print (comment.body)
#     print(comment.author)

if __name__ == "__main__":
    main()
