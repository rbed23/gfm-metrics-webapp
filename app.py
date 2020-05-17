'''
running the GFM Metrics back-end script for GFM Metrics App Webpage
'''
# standard libraries
from collections import Counter
from datetime import datetime
import json
import re
import operator
import os

# 3rd party liraries
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from requests import get, exceptions as rx
import nltk
from rq import Queue
from rq.job import Job
from validators import url as vurl

# locals
from modules import app_manager
from worker import conn


app = Flask(__name__, template_folder='gfm-site-templates/')
app.config.from_object(os.environ['APP_SETTINGS'])

db = SQLAlchemy(app)        # instatiate DB from app

q = Queue(connection=conn)  # instantiate worker Q


def worker_task(url):
    '''
    takes website url and gets donations data

    <type url> str
    <desc url> webpage url

    <<type result>> Result
    <<desc result>> relevant information from webpage scrape
    '''
            
    resp, data = app_manager.url_manager(url)

    if not resp:
        return db_put(url, errors=data)
    else:
        return db_put(url, results=data)


def db_put(url, results=None, errors=None):
    
    # save the results
    try:
        from models import Result
        if errors:
            result = Result(
                url=url,
                datetime=f"{datetime.utcnow()} (UTC)",
                errors=errors
            )        
        else:
            result = Result(
                url=url,
                datetime=f"{datetime.utcnow()} (UTC)",
                results=results
            )
        db.session.add(result)
        db.session.commit()
        return result.id
    except Exception as err:
        errors.append(
            f"Unable to add item to database:{str(err)}"
        )
        return {"errors": errors}



@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/start', methods=['POST'])
def load_worker():
    # this import solves a rq bug which currently exists
    from app import worker_task

    # get url from webform entry
    data = json.loads(request.data.decode())
    url = data['url']

    if not url[:8].startswith(('https://', 'http://')):
        url = 'http://' + url

    # throw job to worker
    job = q.enqueue_call(
        func=worker_task,
        args=(url,),
        result_ttl=5000
    )

    return job.get_id()


@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):

    job = Job.fetch(job_key, connection=conn)

    if job.is_finished:
        from models import Result
        result = Result.query.filter_by(id=job.result).first()
        
        response = ["", []]
        if not result.errors:
            # of type <dict>
            response[0] = "res"
            response[1] = sorted(
                result.results.items(),
                reverse=True
            )
        else:
            # of type <list>
            response[0] = "err"
            response[1] = sorted(
                result.errors
            )
        return jsonify(response), 200
    else:
        return "Working...", 202


@app.route('/<name>')
def hello(name):
    return f"Hello {name}!"


if __name__ == '__main__':
    app.run()
