import requests
import feedparser

url = "http://export.arxiv.org/api/query?search_query=all:quadrupole&start=0&max_results=10"
feed = feedparser.parse(requests.get(url).text)

for entry in feed.entries:
    print(entry.title)
