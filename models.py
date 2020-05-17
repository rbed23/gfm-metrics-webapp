'''
Construct DB Models module
'''
from sqlalchemy.dialects.postgresql import JSON

from app import db


class Result(db.Model):
    __tablename__ = 'gfm_site_results'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    datetime = db.Column(db.String())
    results = db.Column(JSON)
    errors = db.Column(JSON)


    def __init__(self, url, datetime, results=None, errors=None):
        self.url = url
        self.datetime = datetime
        self.results = results
        self.errors = errors


    def __repr__(self):
        return f"<id {self.id}>"
