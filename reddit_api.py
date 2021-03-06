import os
import praw

clientId = 0
clientSecret = ""
userAgent = ""
try:
    clientId = os.environ["CLIENT_ID"]
    clientSecret = os.environ["CLIENT_SECRET"]
    userAgent = os.environ["USER_AGENT"]
except KeyError:
    print("Sem variáveis de ambiente CLIENT_ID, CLIENT_SECRET e USER_AGENT")


reddit = praw.Reddit(client_id = clientId,
                    client_secret = clientSecret,
                    user_agent = userAgent)

def get_random_submission(subName):
    submission = reddit.subreddit(subName).random()
    return submission