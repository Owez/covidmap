import json
from . import app, db
from .models import Node
from .collecter import csvtojson

def populate_db():
    """Top-level function for getting all csv data from github"""

    db.create_all()
    csv_data = json.loads(csvtojson())

    for country_name in csv_data:
        new_node = Node(country_name, csv_data[country_name])
        
        db.session.add(new_node)
        db.session.commit()
