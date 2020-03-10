import pandas as pd
from bs4 import BeautifulSoup
import requests
from lxml import html

def get_most_recent():
    url = 'https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports'
    page = requests.get(url)
    soup=BeautifulSoup(page.content,'html.parser')
    table = soup.find('table', attrs={'class': 'files js-navigation-container js-active-navigation-container'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    data=[]
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    lastelement = data[-2]
    lastelementurl = 'https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_daily_reports/{}'.format(lastelement)
    return lastelementurl
        

print(get_most_recent())

