# -*- coding: utf-8 -*-

# import libraries
import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import sys
import tqdm
import time

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

def article_time_scrap(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	
	dt = soup.find('div', class_='ArticleHeader_date')
	if dt is None: dt = soup.find('div', class_='HeroArticleHeader_date')
	
	return dt.text.split('/')[1].strip()

def scrap(url, remove_el='div', remove_class='actionButton', 
  text_class=lambda s: s in ["feature", "topStory"]):
    # query the website and return the html to the variable ‘page’
    page = requests.get(url)

    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(page.content, 'html.parser')

    for i in soup.findAll(remove_el, class_=remove_class): i.extract()
	
    # Take out the <div> of all articles and get its value
    text_box = soup.findAll('div', class_=text_class)[::-1]
	
    for t in text_box:
        link = t.a['href']
		
        if link in ["/article/lendingclub-website/corrected-lending-club-website-goes-down-cites-data-center-outage-idUSL1N19100U"]: 
            continue
		
        flag = True
        while flag:
            flag = False
            try:
                hhmm = article_time_scrap(f"https://www.reuters.com{link}")
            except AttributeError:
                print("\n\n**"+url+"    "+str(t))
                print(f"https://www.reuters.com{link} **\n\n")
                flag = True
                print("Waiting for 60s...")
                time.sleep(60)

        text = t.text.strip().replace("\u200b", "").replace("\u200d", "").replace("\uff0c", ", ")
        yield (hhmm, text)

def process_date(date):
    df = pd.DataFrame(columns=['date', 'time', 'title', 'abstract'])

    #url = f"https://www.reuters.com/finance/stocks/company-news/{company}?date={date}"
    url = f"https://www.reuters.com/finance/markets/us?date={date}"
    articles = scrap(url, remove_el='time', remove_class='article-time', text_class='story-content')
    if articles:
        for time, article in articles:
            title, abstract = get_title_abstrct(article)
            new_date = date[4:] + '-' + date[:2] + '-' + date[2:4]
            new_row = pd.Series([new_date, time, title, abstract], index=['date', 'time', 'title', 'abstract'])
            #print(new_row.to_frame().T.to_csv(index=False))
            df = pd.concat([df, new_row.to_frame().T])
	
    return df

if __name__ == '__main__':
    company = 'US' #['AMZN.OQ', 'FB.OQ', 'TSLA.OQ', 'GE.A', 'GS.A']
    #start = datetime.datetime.strptime("03-03-2014", "%m-%d-%Y")
    start = datetime.datetime.strptime("02-05-2018", "%m-%d-%Y")
    end = datetime.datetime.strptime("03-02-2019", "%m-%d-%Y")
    dates = get_dates(start, end)
	
    f = open(f"News/{company}.csv", "a+")
	
    #print("date,time,title,abstract", file=f)
	
    for d in tqdm.tqdm(map(process_date, dates), total=len(dates)):
        print(d.to_csv(index=False), file=f)