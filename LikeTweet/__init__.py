import datetime
import logging
import tweepy

import azure.functions as func
import os


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
    auth = tweepy.OAuthHandler(os.environ["TWITTER_CONSUMER_KEY"], os.environ["TWITTER_CONSUMER_SECRET"])
    auth.set_access_token(os.environ["TWITTER_ACCESS_TOKEN"], os.environ["TWITTER_ACCESS_TOKEN_SECRET"])

    api = tweepy.API(auth)

    brandontweets = api.user_timeline("gopher4lyfe", count = 10)

    notart = 0
    for tweet in brandontweets:
        if not (tweet.text[0:2] == 'RT' or tweet.text[0:1] == '@'):
            try:
                api.create_favorite(tweet.id)
                notart +=1
            except:
                logging.info("already favorited")
    logging.info('%d tweets favorited', notart)