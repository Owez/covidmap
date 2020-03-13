import os
import json
import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from collecter import csvtojson, get_data_from_all_to_json, daily_province
import requests

print("Loading graph data")
get_data_from_all_to_json()


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


class Country(db.Model):
    """A single datapoint (usually a countries data)"""

    __tablename__ = "countries"

    id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String())
    confirmed = db.Column(db.Integer)  # not used atm
    recovered = db.Column(db.Integer)  # not used atm
    deceased = db.Column(db.Integer)  # not used atm
    provinces = db.relationship("Province", backref="country", lazy=True)
    created = db.Column(db.DateTime)

    def __init__(self, country_name: str, items: dict):
        self.country_name = country_name
        self.confirmed = items["ConfirmedCases"]
        self.recovered = items["Recovered"]
        self.deceased = items["Deaths"]
        self.created = datetime.datetime.utcnow()


class Province(db.Model):
    """A single province inside of a country"""

    __tablename__ = "provinces"

    id = db.Column(db.Integer, primary_key=True)
    province_name = db.Column(db.String())
    confirmed = db.Column(db.Integer)
    lat_coord = db.Column(db.String(64))
    long_coord = db.Column(db.String(64))
    created = db.Column(db.DateTime)
    country_id = db.Column(db.Integer, db.ForeignKey("country.id"), nullable=False)

    def __init__(self, province_name: str, confirmed: int, coords: (str, str)):
        self.province_name = province_name
        self.confirmed = confirmed
        self.lat_coord = coords[0]
        self.long_coord = coords[1]
        self.created = datetime.datetime.utcnow()


class Newslet(db.Model):
    """A single found article"""

    id = db.Column(db.String(), primary_key=True)
    title = db.Column(db.String())
    lead_paragraph = db.Column(db.String())
    created = db.Column(db.DateTime)

    def __init__(self, id: str, title: str, lead_paragraph: str):
        self.id = id
        self.title = title
        self.lead_paragraph = lead_paragraph
        self.created = datetime.datetime.now()


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
    with open("data/graphdata.json", "r") as file:
        response = {
            "Success": "Data has been successfully obtained",
            "Data": json.load(file),
        }
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


def pull_nytimes() -> int:
    """Adds new nytimes stuff to database and returns status code"""

    search = "https://api.nytimes.com/svc/search/v2/articlesearch.json?q=coronavirus&api-key={config.NYTIMES_KEY}"
    resp = requests.get(search)

    if resp.status_code != 200:
        return resp.status_code

    for newslet in resp.json()["response"]["docs"]:
        if Newslet.query.filter_by(id=newslet["web_url"]).first() is None:
            new_newslet = Newslet(
                newslet["web_url"], newslet["snippet"], newslet["lead_paragraph"]
            )

            db.session.add(new_newslet)
            db.session.commit()

    return resp.status_code


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
        new_country = Country(country_name, csv_data[country_name])
        db.session.add(new_country)
        db.session.commit()

    print("Getting coords for map..")
    get_coords()

    print("Adding newslets..")

    nytimes_respcode = pull_nytimes()
    if nytimes_respcode != 200:
        print("Failed to add newslets, error code: '{nytimes_respcode}'!")


def data_formatting():
    data = Country.query.all()
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
    return datadict


def get_coords():
    if os.path.exists("data/cords.json"):
        print("Coords have already been gathered, no need to fetch!")
    else:
        data = Country.query.all()
        countries = []
        cordsdict = {}
        for row in data:
            if row.country_name not in countries:
                countries.append(row.country_name)
        for country in countries:
            countryname = country

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
            cordsdict[country] = {
                "Latitude": dt["results"][0]["geometry"]["location"]["lat"],
                "Longitude": dt["results"][0]["geometry"]["location"]["lng"],
            }
            with open("data/cords.json", "w") as file:
                file.write(json.dumps(cordsdict))

    data = country.query.all()
    countries = []
    cordsdict = {}
    for row in data:
        if row.country_name not in countries:
            countries.append(row.country_name)
    for country in countries:
        countryname = country
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
        cordsdict[country] = {
            "Latitude": dt["results"][0]["geometry"]["location"]["lat"],
            "Longitude": dt["results"][0]["geometry"]["location"]["lng"],
        }


def province_to_db():
    daily_province()
    with open("data/daily_province.json", "r") as jf:
        data = json.load(jf)
        for province in data:
            new_province = Province(
                province,
                province["confirmed"],
                (province["latitude"], province["longitude"]),
            )


if __name__ == "__main__":
    populate_db()

    app.run(debug=True)
