import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
from json import JSONEncoder
import datetime

class DateTimeEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


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
    lastelement = data[-2][0]
    lastelementurl = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{}'.format(lastelement)
    recent = requests.get(lastelementurl)
    #print(recent.text)
    return recent.text


def returncsv():
    with open('data.csv', 'w') as file:
        file.write(get_most_recent())
    pd.set_option('display.max_rows', None)
    df = pd.read_csv('./data.csv',usecols=['Country/Region', 'Last Update', 'Confirmed', 'Deaths', 'Recovered', 'Latitude','Longitude'])
    return df

def csvtojson():
    fieldnames = ('Country/Region', 'Last Update', 'Confirmed', 'Deaths', 'Recovered', 'Latitude','Longitude')
    data = returncsv()
    countries = []
    for i in data['Country/Region']:
        if i not in countries:
            countries.append(i)
    datadict = {}
    for country in countries:
        confirmed = data[data['Country/Region'] ==  country]['Confirmed']
        totalconfirmed = 0
        for conf in confirmed:
            totalconfirmed += conf
        deaths = data[data['Country/Region'] == country]['Deaths']
        totaldeaths = 0
        for death in deaths:
            totaldeaths += death
        recoveries = data[data['Country/Region'] == country]['Recovered']
        totalrecoveries = 0
        for recovery in recoveries:
            totalrecoveries += recovery
        latitudelist = data[data['Country/Region'] == country]['Latitude']
        count = 0
        totallatitudes = 0
        for latitude in latitudelist:
            count += 1
            totallatitudes += latitude
        avlatitude = float(totallatitudes/count)
        longitudelist = data[data['Country/Region'] == country]['Longitude']
        count = 0
        totallongitudes = 0
        for longitude in longitudelist:
            count += 1
            totallongitudes += longitude
        avtotallongitudes = float(totallongitudes/count)

        datadict[country] = {
                     'LastUpdate': datetime.datetime.now().utcnow(),
                     'ConfirmedCases': totalconfirmed,
                     'Deaths': totaldeaths,
                     'Recovered': totalrecoveries
                     }
    with open('data.json', 'w') as file:
        file.write(json.dumps(datadict, cls=DateTimeEncoder))

    data = json.dumps(datadict, cls=DateTimeEncoder)
    return data


def fulldatatojson():
    fieldnames = ('Province State', 'Country/Region', 'Last Update', 'Confirmed', 'Deaths', 'Recovered', 'Latitude','Longitude')
    data = returncsv()
    countries = []
    for i in data['Country/Region']:
        if i not in countries:
            countries.append(i)
    datadict = {}
    for country in countries:
        confirmed = data[data['Country/Region'] ==  country]['Confirmed']
        totalconfirmed = 0
        for conf in confirmed:
            totalconfirmed += conf
        deaths = data[data['Country/Region'] == country]['Deaths']
        totaldeaths = 0
        for death in deaths:
            totaldeaths += death
        recoveries = data[data['Country/Region'] == country]['Recovered']
        totalrecoveries = 0
        for recovery in recoveries:
            totalrecoveries += recovery
        latitudelist = data[data['Country/Region'] == country]['Latitude']

        datadict[country] = {
                     'LastUpdate': datetime.datetime.now().utcnow(),
                     'ConfirmedCases': totalconfirmed,
                     'Deaths': totaldeaths,
                     'Recovered': totalrecoveries
                     }
    with open('data.json', 'w') as file:
        file.write(json.dumps(datadict, cls=DateTimeEncoder))

    data = json.dumps(datadict, cls=DateTimeEncoder)
    return data
