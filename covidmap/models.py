import datetime
from . import db

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
