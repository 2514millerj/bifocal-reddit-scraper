import logging
import praw
import json

from config import conservative_subreddits, liberal_subreddits
from analysis import extract_keywords
from database import store_submissions

def get_submissions(reddit):
    submissions = []
    for subreddit_name in conservative_subreddits:
        subreddit = reddit.subreddit(subreddit_name)
        hot_submissions = subreddit.hot(limit=5)
        hot_submissions = [('conservative', x) for x in hot_submissions]
        submissions += hot_submissions

    for subreddit_name in liberal_subreddits:
        subreddit = reddit.subreddit(subreddit_name)
        hot_submissions = subreddit.hot(limit=5)
        hot_submissions = [('liberal', x) for x in hot_submissions]
        submissions += hot_submissions
    
    return submissions

def process_submissions(submissions):
    formatted_submissions = []
    for submission in submissions:
        data = submission[1]
        label = submission[0]

        if data.permalink not in data.url:
            keywords = extract_keywords(data.url)
        else:
            continue

        formatted_data = {
            "label": label,
            "url": data.url,
            "upvote_ratio": data.upvote_ratio,
            "title": data.title,
            "upvotes": data.score,
            "permalink": data.permalink,
            "keywords": keywords
        }
        formatted_submissions.append(formatted_data)

    return formatted_submissions
            

def store_headlines(headlines):
    pass

if __name__ == "__main__":
    logging.info("Running Bifocal News Reddit Scraper")

    reddit = praw.Reddit()

    #get hottest posts from conservative and liberal subreddits
    submissions = get_submissions(reddit)

    #pull necessary information from posts and label
    formatted_submissions = process_submissions(submissions)

    #store headlines in database
    store_submissions(formatted_submissions)