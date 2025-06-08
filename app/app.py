#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@app.py
"""

from flask import Flask, render_template, request, jsonify, session
import requests
import os
import json
from datetime import timedelta

app = Flask(__name__, template_folder='templates')
app.secret_key = 'secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/index')
def index():
    return render_template('index.html')
    

def post_to_db(query):
    db_env_url = 'http://db-env:7001/app/process_query'
    response = requests.post(db_env_url, json={'query': query})
    return response

def handle_query(query):
    if not query:
        return {'error': 'No query provided'}, 400
    response = post_to_db(query)
    if response.status_code != 200:
        error_info = {
            'error': response.status_code,
            'status_code': response.status_code,
            'response_content': response.content.decode('utf-8')
        }
        return error_info, 500
    response = response.json()
    json_data = json.loads(response)
    return json_data, 200

@app.route('/shorts')
def shorts():
    query = request.args.get('query')
    json_data, status_code = handle_query(query)
    if status_code != 200:
        return render_template('error.html', error_info=json_data), status_cod
    return render_template('shorts2.html', query=query, video_results=json_data['videos'], result_count=len(json_data['videos']))

@app.route('/searchresults', methods=['GET'])
def searchresults():
    query = request.args.get('query')
    json_data, status_code = handle_query(query)
    if status_code != 200:
        return render_template('error.html', error_info=json_data), status_code
    return render_template('searchresults.html', query=query, video_results=json_data['videos'], result_count=len(json_data['videos']))

@app.route('/video')
def video():
    video_id = request.args.get('video_id')
    return render_template('video.html', video_id=video_id)

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/about')
def about():
    return render_template('about.html')

print('starting...')