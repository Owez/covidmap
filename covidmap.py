import os
import json
import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from collecter import csvtojson
import requests
# CONFIG #

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///covidmap.db'

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


# ROUTES #

@app.route("/")
def index():
    return render_template("index.html")

#dummy route

@app.route('/data', methods=['GET'])
def passdata():
    try:
        response = {'Success':'Data has been successfully obtained', 'Data': data_formatting()}
        return response, 200
    except:
        response = {'Error':'An error has occured.'}
        return response, 400

@app.route('/totaldata', methods=['GET'])
def totaldata():
    with open('totaldata.json', 'r') as file:
        jsfile = json.load(file)
        response = {'Success':'Data has been successfully obtained', 'Data': jsfile}
    return response, 200


@app.route('/coords', methods=['GET'])
def passkey():
    with open('cords.json', 'r') as file:
        response = {'Data': json.loads(file.read())}
        return response, 200

@app.route('/accesskey', methods=['GET'])
def accesskey():
    #print(os.getenv('access_key'))
    return {'key': os.environ['access_key']}

# UTILS #

def populate_db():
    """Top-level function for getting all csv data from github"""

    print("Populating database..")
    if os.path.exists("covidmap.db"):
        print("Database is already populated!")
        return

    db.create_all()
    csv_data = json.loads(csvtojson())
    for country_name in csv_data:
        new_node = Node(country_name, csv_data[country_name])
        db.session.add(new_node)
        db.session.commit()


def data_formatting():
    data = Node.query.all()
    countries = []
    datadict = {}
    for row in data:
        if row.country_name not in countries:
            countries.append(row.country_name)
    for country in countries:
        for row in data:
            if row.country_name==country:
                datadict[country]= {
                    'confirmed': row.confirmed,
                    'deaths': row.deceased,
                    'recovered': row.recovered
                }
               # print(datadict[country]['recovered'])
    return datadict

def get_coords():
    if os.path.exists("cords.json"):
        print('Coords have already been gathered')
    else:
        data = Node.query.all()
        countries = []
        cordsdict = {}
        for row in data:
            if row.country_name not in countries:
                countries.append(row.country_name)
        for country in countries:
            if country == 'Mainland China':
                countryname = 'China'
            elif country == 'occupied Palestinian territory':
                countryname = 'Palestine'
            else:
                countryname = country
            response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={}&key=AIzaSyB-2lC7PWWHcDvc6T6mtVdmXCzfGf_p0kA'.format(countryname))
            dt = json.loads(response.text)
            #print(dt)
            #print(country)
            cordsdict[country] = {'Latitude': dt['results'][0]['geometry']['location']['lat'], 'Longitude': dt['results'][0]['geometry']['location']['lng']}
            #print('Country: {}'.format(country) + str(dt['results'][0]['geometry']['location']))
            #print(cordsdict)
            with open('cords.json', 'w') as file:
                file.write(json.dumps(cordsdict))

    data = Node.query.all()
    countries = []
    cordsdict = {}
    for row in data:
        if row.country_name not in countries:
            countries.append(row.country_name)
    for country in countries:
        if country == 'Mainland China':
            countryname = 'China'
        elif country == 'occupied Palestinian territory':
            countryname = 'Palestine'
        response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={}&key=AIzaSyB-2lC7PWWHcDvc6T6mtVdmXCzfGf_p0kA'.format(countryname))
        dt = json.loads(response.text)
        #print(dt)
        #print(country)
        cordsdict[country] = {'Latitude': dt['results'][0]['geometry']['location']['lat'], 'Longitude': dt['results'][0]['geometry']['location']['lng']}
        #print('Country: {}'.format(country) + str(dt['results'][0]['geometry']['location']))
    #print(cordsdict)




if __name__ == "__main__":
    populate_db()
    get_coords()
    app.run(debug=True)
