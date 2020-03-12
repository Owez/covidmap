import os
import json
import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from collecter import csvtojson, get_data_from_all_to_json
import requests


# CONFIG #


class Config:
    """Configuration class for easy storage of useful metadata including API keys"""

    def __init__(self):
        self.SECRET_KEY = self._get_env("SECRET_KEY")
        self.NYTIMES_KEY = self._get_env("NYTIMES_KEY")

    def _get_env(self, env: str, fallback: str = None) -> str:
        """Gets env var (boilerplate interchangable)"""

        if fallback:
            try:
                return os.environ[env]
            except:
                return fallback

        return os.environ[env]


app = Flask(__name__)
config = Config()

app.config["SECRET_KEY"] = config.SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///covidmap.db"

db = SQLAlchemy(app)

# MODELS #


class Node(db.Model):
    """A single datapoint (usually a countries data)"""

    __tablename__ = "nodes"

    id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String())
    confirmed = db.Column(db.Integer)
    recovered = db.Column(db.Integer)
    deceased = db.Column(db.Integer)
    created = db.Column(db.String())

    def __init__(self, country_name: str, items: dict):
        self.country_name = country_name
        self.confirmed = items["ConfirmedCases"]
        self.recovered = items["Recovered"]
        self.deceased = items["Deaths"]
        self.created = datetime.datetime.utcnow()


# class Newslet(db.Model):
#     """A single found article"""
#
#     id = db.Column(db.String(), primary_key=True)
#     title = db.Column(db.String())
#     lead_paragraph = db.Column(db.String())
#     created = db.Column(db.DateTime)
#
#     def __init__(self, id: str, title: str, lead_paragraph: str):
#         self.id = id
#         self.title = title
#         self.lead_paragraph = lead_paragraph
#         self.created = datetime.datetime.now()


# ROUTES #


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/data", methods=["GET"])
def passdata():
    try:
        response = {
            "Success": "Data has been successfully obtained",
            "Data": data_formatting(),
        }
        return response, 200
    except:
        response = {"Error": "An error has occured."}
        return response, 400


@app.route("/graphdata", methods=["GET"])
def graphdata():
    response = {"Success": "Data has been successfully obtained", "Data": graphdatajson}
    return response, 200


@app.route("/coords", methods=["GET"])
def passkey():
    with open("cords.json", "r") as file:
        response = {"Data": json.loads(file.read())}
        return response, 200


@app.route("/accesskey", methods=["GET"])
def accesskey():
    # print(os.getenv("access_key"))
    return {"key": os.environ["access_key"]}


# UTILS #

def setup_graph_data():
    """Makes graphdata.json and sets as global"""
    
    get_data_from_all_to_json() # gens graphdata.json

    with open("graphdata.json", "r") as file:
        global graphdatajson
        graphdatajson = json.load(file)

def pull_nytimes() -> bool:
    """Adds new nytimes stuff to database and returns if it was successful"""

    search = "https://api.nytimes.com/svc/search/v2/articlesearch.json?q=coronavirus&api-key={config.NYTIMES_KEY}"
    resp = requests.get(search)

    if resp.status_code != 200:
        return False

    for newslet in resp.json()["response"]["docs"]:
        if Newslet.query.filter_by(id=newslet["web_url"]).first() is None:
            new_newslet = Newslet(
                newslet["web_url"], newslet["snippet"], newslet["lead_paragraph"]
            )

            db.session.add(new_newslet)
            db.session.commit()

    return True


def populate_db():
    """Top-level function for getting all csv data from github"""

    print("Populating database..")
    if os.path.exists("covidmap.db"):
        print("Database is already populated!")
        return

    print("Adding stats..")
    db.create_all()
    csv_data = json.loads(csvtojson())
    for country_name in csv_data:
        new_node = Node(country_name, csv_data[country_name])
        db.session.add(new_node)
        db.session.commit()

    print("Adding newslets..")

    if not pull_nytimes():
        print("Failed to add newslets!")


def data_formatting():
    data = Node.query.all()
    countries = []
    datadict = {}
    for row in data:
        if row.country_name not in countries:
            countries.append(row.country_name)
    for country in countries:
        for row in data:
            if row.country_name == country:
                datadict[country] = {
                    "confirmed": row.confirmed,
                    "deaths": row.deceased,
                    "recovered": row.recovered,
                }
            # print(datadict[country]["recovered"])
    return datadict


def get_coords():
    if os.path.exists("cords.json"):
        print("Coords have already been gathered")
    else:
        data = Node.query.all()
        countries = []
        cordsdict = {}
        for row in data:
            if row.country_name not in countries:
                countries.append(row.country_name)
        for country in countries:
            if country == "Mainland China":
                countryname = "China"
            elif country == "occupied Palestinian territory":
                countryname = "Palestine"
            else:
                countryname = country
            response = requests.get(
                "https://maps.googleapis.com/maps/api/geocode/json?address={}&key=AIzaSyB-2lC7PWWHcDvc6T6mtVdmXCzfGf_p0kA".format(
                    countryname
                )
            )
            dt = json.loads(response.text)
            # print(dt)
            # print(country)
            cordsdict[country] = {
                "Latitude": dt["results"][0]["geometry"]["location"]["lat"],
                "Longitude": dt["results"][0]["geometry"]["location"]["lng"],
            }
            # print("Country: {}".format(country) + str(dt["results"][0]["geometry"]["location"]))
            # print(cordsdict)
            with open("cords.json", "w") as file:
                file.write(json.dumps(cordsdict))

    data = Node.query.all()
    countries = []
    cordsdict = {}
    for row in data:
        if row.country_name not in countries:
            countries.append(row.country_name)
    for country in countries:
        if country == "Mainland China":
            countryname = "China"
        elif country == "occupied Palestinian territory":
            countryname = "Palestine"
        response = requests.get(
            "https://maps.googleapis.com/maps/api/geocode/json?address={}&key=AIzaSyB-2lC7PWWHcDvc6T6mtVdmXCzfGf_p0kA".format(
                countryname
            )
        )
        dt = json.loads(response.text)
        # print(dt)
        # print(country)
        cordsdict[country] = {
            "Latitude": dt["results"][0]["geometry"]["location"]["lat"],
            "Longitude": dt["results"][0]["geometry"]["location"]["lng"],
        }
        # print("Country: {}".format(country) + str(dt["results"][0]["geometry"]["location"]))
    # print(cordsdict)


if __name__ == "__main__":
    setup_graph_data()
    populate_db()
    get_coords()

    app.run(debug=True)
