# -*- coding: utf-8 -*-
# import libraries
import urllib2
from bs4 import BeautifulSoup
import datetime
import pandas as pd

# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def get_dates(start, end):
    dates = []
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
    for date in date_generated:
        dates.append(date.strftime("%m%d%Y"))
    return dates

def get_title_abstrct(text):
    t = text.splitlines()
    title = t[0]
    abstract = " ".join(t[1:])
    return title, abstract

def scrap(url):
    # query the website and return the html to the variable ‘page’
    articles = []
    page = urllib2.urlopen(url)

    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(page, 'html.parser')

    # Take out the <div> of all feature articles and get its value
    text_box = soup.findAll('div', attrs={"class": "feature"})
    for t in text_box:
        text = t.text.strip()
        articles.append(text)
    return articles


companies = ['GS.A'] #['AMZN.OQ', 'FB.OQ', 'TSLA.OQ', 'GE.A', 'GS.A']
start = datetime.datetime.strptime("03-03-2014", "%m-%d-%Y")
end = datetime.datetime.strptime("03-02-2019", "%m-%d-%Y")
dates = get_dates(start, end)

for company in companies:
    df = pd.DataFrame(columns=['date', 'title', 'abstract'])
    for date in dates:
        url = 'https://www.reuters.com/finance/stocks/company-news/'+company+'?date='+date
        articles = scrap(url)
        if articles:
            for article in articles:
                title, abstract = get_title_abstrct(article)
                new_date = date[4:] + '-' + date[:2] + '-' + date[2:4]
                new_row = pd.Series([new_date, title, abstract], index=['date', 'title', 'abstract'])
                df = pd.concat([df, new_row.to_frame().T])
    df.to_csv('News/'+company+'.csv', index = False)

