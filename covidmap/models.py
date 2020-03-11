from . import db

class Node(db.Model):
    """A single datapoint (usually a countries data)"""

    __tablename__ = "nodes"

    id = db.Column(db.String(), primary_key=True)
    confirmed = db.Column(db.Integer)
    recovered = db.Column(db.Integer)
    deceased = db.Column(db.Integer)
    updated = db.Column(db.String())

    def __init__(self, id: str, confirmed: int, recovered: int, deceased: int, updated: str):
        self.id = id
        self.confirmed = confirmed
        self.recovered = recovered
        self.deceased = deceased
        self.updated = updated
