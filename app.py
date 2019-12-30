import logging
import praw

from .config import conservative_subreddits, liberal_subreddits

def get_conservative_posts(reddit):
    for subreddit_name in conservative_subreddits:
        print(subreddit_name)

def get_liberal_posts(reddit):
    for subreddit_name in liberal_subreddits:
        print(subreddit_name)

def process_posts(conservative_posts, liberal_posts):
    pass

def store_headlines(headlines):
    pass

if __name__ == "__main__":
    logging.info("Running Bifocal News Reddit Scraper")

    reddit = praw.Reddit(client_id='PERSONAL_USE_SCRIPT_14_CHARS', \
                     client_secret='SECRET_KEY_27_CHARS ', \
                     user_agent='YOUR_APP_NAME', \
                     username='YOUR_REDDIT_USER_NAME', \
                     password='YOUR_REDDIT_LOGIN_PASSWORD')

    #get hottest posts from conservative and liberal subreddits
    conservative_posts = get_conservative_posts(reddit)
    liberal_posts = get_liberal_posts(reddit)

    #pull necessary information from posts and label
    formatted_headlines = process_posts(conservative_posts, liberal_posts)

    #store headlines in database
    store_headlines(formatted_headlines)