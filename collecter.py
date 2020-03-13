import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
from json import JSONEncoder
import os
import datetime
from collections import defaultdict
from pprint import pprint as pp
from pathlib import Path


class DateTimeEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


def delglobal():
    mypath = "./data/global_daily"
    for root, dirs, files in os.walk(mypath):
        for file in files:
            os.remove(os.path.join(root, file))


def get_most_recent():
    url = "https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find(
        "table",
        attrs={"class": "files js-navigation-container js-active-navigation-container"},
    )
    table_body = table.find("tbody")
    rows = table_body.find_all("tr")
    data = []
    for row in rows:
        cols = row.find_all("td")
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    lastelement = data[-2][0]
    lastelementurl = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{}".format(
        lastelement
    )
    recent = requests.get(lastelementurl)
    # print(recent.text)
    return recent.text


def returncsv():
    with open("data/data.csv", "w") as file:
        file.write(get_most_recent())
    pd.set_option("display.max_rows", None)
    df = pd.read_csv(
        "data/data.csv",
        usecols=["Province/State",
            "Country/Region",
            "Last Update",
            "Confirmed",
            "Deaths",
            "Recovered",
            "Latitude",
            "Longitude",
        ],
    )
    return df


def csvtojson():
    fieldnames = (
        "Country/Region",
        "Last Update",
        "Confirmed",
        "Deaths",
        "Recovered",
        "Latitude",
        "Longitude",
    )
    data = returncsv()
    countries = []
    for i in data["Country/Region"]:
        if i not in countries:
            countries.append(i)
    datadict = {}
    for country in countries:
        confirmed = data[data["Country/Region"] == country]["Confirmed"]
        totalconfirmed = 0
        for conf in confirmed:
            totalconfirmed += conf
        deaths = data[data["Country/Region"] == country]["Deaths"]
        totaldeaths = 0
        for death in deaths:
            totaldeaths += death
        recoveries = data[data["Country/Region"] == country]["Recovered"]
        totalrecoveries = 0
        for recovery in recoveries:
            totalrecoveries += recovery
        latitudelist = data[data["Country/Region"] == country]["Latitude"]
        count = 0
        totallatitudes = 0
        for latitude in latitudelist:
            count += 1
            totallatitudes += latitude
        avlatitude = float(totallatitudes / count)
        longitudelist = data[data["Country/Region"] == country]["Longitude"]
        count = 0
        totallongitudes = 0
        for longitude in longitudelist:
            count += 1
            totallongitudes += longitude
        avtotallongitudes = float(totallongitudes / count)

        datadict[country] = {
            "LastUpdate": datetime.datetime.now().utcnow(),
            "ConfirmedCases": totalconfirmed,
            "Deaths": totaldeaths,
            "Recovered": totalrecoveries,
        }
    with open("data/data.json", "w") as file:
        file.write(json.dumps(datadict, cls=DateTimeEncoder))

    data = json.dumps(datadict, cls=DateTimeEncoder)
    return data


def csvtojsonfunction(data, name):
    fieldnames = (
        "Country/Region",
        "Last Update",
        "Confirmed",
        "Deaths",
        "Recovered",
        "Latitude",
        "Longitude",
    )
    countries = []
    for i in data["Country/Region"]:
        if i not in countries:
            countries.append(i)
    datadict = {}
    name = name.split(".csv")[0]
    datadict[name] = {}
    for country in countries:
        confirmed = data[data["Country/Region"] == country]["Confirmed"]
        totalconfirmed = 0
        for conf in confirmed:
            totalconfirmed += conf
        deaths = data[data["Country/Region"] == country]["Deaths"]
        totaldeaths = 0
        for death in deaths:
            totaldeaths += death
        recoveries = data[data["Country/Region"] == country]["Recovered"]
        totalrecoveries = 0
        for recovery in recoveries:
            totalrecoveries += recovery
        datadict[name].update(
            {
                country: {
                    "ConfirmedCases": int(totalconfirmed),
                    "Deaths": int(totaldeaths),
                    "Recovered": int(totalrecoveries),
                }
            }
        )
    with open("data/global_daily/{}.json".format(name), "w") as file:
        file.write(json.dumps(datadict, cls=DateTimeEncoder))


def get_data_from_all_to_json():
    try:
        os.makedirs('data/global_daily')
    except FileExistsError:
        pass
    delglobal()
    if os.path.exists("data/graphdata.json"):
        os.remove("data/graphdata.json")
    url = "https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find(
        "table",
        attrs={"class": "files js-navigation-container js-active-navigation-container"},
    )

    if table is None:
        raise Exception("Something is wrong with BeautifulSoup in 'table'!")

    table_body = table.find("tbody")
    rows = table_body.find_all("tr")
    data = []

    for row in rows:
        cols = row.find_all("td")
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    csvnames = []

    for item in data:
        if (
            item[0] != "README.md"
            and item[0] != "Failed to load latest commit information."
            and item[0] != ".gitignore"
        ):
            csvnames.append(item[0])
    count = 0
    for name in csvnames:
        dtdict = {}
        print(name)
        lastelementurl = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{}".format(
            name
        )
        recent = requests.get(lastelementurl)
        with open("data/global_daily/{}".format(name), "wb") as file:
            file.write(recent.text.encode("utf-8"))
        pd.set_option("display.max_rows", None)
        df = pd.read_csv(
            "data/global_daily/{}".format(name),
            usecols=[
                "Country/Region",
                "Last Update",
                "Confirmed",
                "Deaths",
                "Recovered",
            ],
        )
        df.fillna("0", inplace=True)
        df.to_csv("data/global_daily/{}".format(name), index=False)
        # print(df)

    csvfiles = os.listdir("data/global_daily")
    print(csvfiles)
    for file in csvfiles:
        df = pd.read_csv(
            f"data/global_daily/{file}",
            usecols=[
                "Country/Region",
                "Last Update",
                "Confirmed",
                "Deaths",
                "Recovered",
            ],
        )
        print(f"Converting: {file} to json")
        csvtojsonfunction(df, file)
    csvfiles = os.listdir("data/global_daily")
    for csv in csvfiles:
        if csv.endswith(".csv"):
            os.remove("data/global_daily/{}".format(csv))

    global_daily = Path("./data/global_daily/")

    list_of_dicts = []
    for file in global_daily.glob("*.json"):
        with file.open() as fd:
            list_of_dicts.append(json.load(fd))

    master = defaultdict(list)

    for d in list_of_dicts:
        for key, value in d.items():
            master[key].append(value)

    with open("data/graphdata.json", "w") as file:
        file.write(json.dumps(master))
    delglobal()

def returnpartialcsv():
    with open("data/data.csv", "w") as file:
        file.write(get_most_recent())
    pd.set_option("display.max_rows", None)
    df = pd.read_csv(
        "data/data.csv",
        usecols=["Province/State",
            'Country/Region',
            "Confirmed",
            "Latitude",
            "Longitude",
        ],
    )
    return df
def daily_province():
    get_most_recent()
    data = returnpartialcsv()
    data.to_json('data/daily_province.json', orient='table')
    provincedict = {}
    with open('data/daily_province.json', 'r') as jf:
        jf = json.load(jf)
        for country in jf['data']:
            if not(country['Province/State']):
                country['Province/State'] = country['Country/Region']
                provincedict[country['Province/State']] = {'latitude': country['Latitude'], 'longitude': country['Longitude'], 'confirmed': country['Confirmed']}
    with open('data/daily_province.json', 'w') as jf:
        jf.write(json.dumps(provincedict))

