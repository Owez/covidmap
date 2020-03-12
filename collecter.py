import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
from json import JSONEncoder
import datetime
import os
from shutil import copyfile

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

def csvtojsonfunction(data, name):
    fieldnames = ('Country/Region', 'Last Update', 'Confirmed', 'Deaths', 'Recovered', 'Latitude','Longitude')
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
        name = name.split('.csv')[0]
        datadict[name] = {}
        datadict.update({ country:
                        {
                        'LastUpdate': datetime.datetime.now().utcnow(),
                        'ConfirmedCases': totalconfirmed,
                        'Deaths': totaldeaths,
                        'Recovered': totalrecoveries
                        }
                        })
    with open('global_daily/{}.json'.format(name), 'w') as file:
        file.write(json.dumps(datadict, cls=DateTimeEncoder))

def get_data_from_all_to_json():
    url = 'https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports'
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('table', attrs={'class': 'files js-navigation-container js-active-navigation-container'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    data = []

    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    csvnames = []

    for item in data:
        if item[0] != 'README.md' and item[0] != 'Failed to load latest commit information.' and item[0]!='.gitignore':
            csvnames.append(item[0])
    count = 0
    for name in csvnames:
        dtdict = {}
        print(name)
        lastelementurl = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{}'.format(name)
        recent = requests.get(lastelementurl)
        with open('global_daily/{}'.format(name), 'wb') as file:
            file.write(recent.text.encode("utf-8"))
        pd.set_option('display.max_rows', None)
        df = pd.read_csv('global_daily/{}'.format(name), usecols=['Country/Region', 'Last Update', 'Confirmed', 'Deaths', 'Recovered'])
        df.fillna("0", inplace=True)
        df.to_csv('global_daily/{}'.format(name))
        #print(df)

    csvfiles = os.listdir('global_daily')
    for file in csvfiles:
        df = pd.read_csv('global_daily/{}'.format(name),usecols=['Country/Region', 'Last Update', 'Confirmed', 'Deaths', 'Recovered'])
        print(file)
        csvtojsonfunction(df, file)
    csvfiles = os.listdir('global_daily')
    for csv in csvfiles:
        if csv.endswith('.csv'):
            os.remove('global_daily/{}'.format(csv))
            pass
    jsonfiles = os.listdir('global_daily')
    print('TEST: {}'.format(jsonfiles[0:]))
    with open(f'global_daily/{jsonfiles[0]}', 'r') as jf:
        dct = {**json.load(jf)}

    for file in jsonfiles[0:]:
        with open(f'global_daily/{file}', 'r') as jf:
            contents = json.load(jf)

        for k, v in contents.items():
            dct[k].update(v)
            print(dct)

    with open('globaldaily/totaldata.json', 'w') as f:
        json.dump(dct, f)

mypath = "./global_daily" #Enter your path here
for root, dirs, files in os.walk(mypath):
    for file in files:
        os.remove(os.path.join(root, file))
get_data_from_all_to_json()
