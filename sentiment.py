from aiat_utils import tryread, errexit
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import sys
import csv

analyzer = SentimentIntensityAnalyzer()

def sentiment_analyze(sentence):
    return analyzer.polarity_scores(sentence)

if __name__ == "__main__":
    if len(sys.argv) != 2: errexit("Usage: sentiment.py [news.csv]", 1)
    
    data = tryread(sys.argv[1])

    if data.pop(0) != ["date", "title", "abstract"]:
        errexit("Wrong headers", -2)

    # date, title, abstract, neg, neu, pos, compound
    data = list(map(lambda r: r + list(sentiment_analyze(r[2]).values()), data))

    writer = csv.writer(sys.stdout)
    writer.writerow("date,title,abstract,neg,neu,pos,compound".split(","))
    for r in data: writer.writerow(r)
