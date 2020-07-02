# Bifocal News Reddit Scraper
Bifocal News is a website that takes liberal and conservative Reddit communities and compares what each other are talking about. This Reddit scraper pulls popular articles from each community and identifies important keywords. The article metadata and keywords are stored in a database to be retreived by the Bifocal News dashboard.

The Bifocal News scraper is open source in order to be totally transparent with its users about how data is collected. This repository can be cloned and ran to pull your own data for analysis and display.

## Keyword Identification Algorithm
The goal of this algorithm is to derive important keywords from an article posted to a subreddit. User posts can be misleading, trolling, and unneccessarily biased so this algorithm only cares about keywords found in the actual article. Below are the general steps:

    - Clean article content by removing useless words and making everything lower case
    - Identify names of individuals, places, and organizations in the content of the article
        - If those names appear in the title of the article, they are keywords
    - Identify non-name keywords from the content of the article
        - If the keyword is in the title, it is a significant keyword

Parsing the title itself for keywords using NLP is often difficult because titles do not need to be complete sentences and identifying significant words becomes much more difficult and inaccurate.

## Database Schema
The schema is simple and contains a table for keywords, a table for news articles, and a table to link the two together.

## Running the Script

    pip3 install -r requirements.txt
    python app.py