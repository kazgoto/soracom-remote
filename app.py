# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, make_response, session, url_for
from urllib import urlencode
import os
import httplib2
import json

api_url  = 'https://api.soracom.io/v1'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SORACOM Remote'

# functions
def _call_api(path, method, params):
    h = httplib2.Http(".cache")
    headers = {
        'X-Soracom-API-Key' : session['apiKey'],
        'X-Soracom-Token'   : session['token'],
        'Content-Type'      : 'application/json'
    }
    resp, content = h.request(api_url + path, method, json.dumps(params), headers=headers)
    error = ''
    if resp.status != 200:
        error = 'Response is bad: ' + str(resp.status) + ' ' + content
        exit

    return error, json.loads(content)

def _is_authorized():
    username = request.form['username']
    password = request.form['password']
    if username is None or password is None:
        return False
    h = httplib2.Http(".cache")
    data = json.dumps({
        "email"    : request.form.get('username'),
        "password" : request.form.get('password')
    })
    headers = {
        'Content-Type' : 'application/json',
        'Accept'       : 'application/json'
    }
    resp, content = h.request(api_url + '/auth',  'POST', body=data, headers=headers)
    if resp.status != 200:
        return False

    resp_json = json.loads(content)
    session['apiKey'] = resp_json['apiKey']
    session['token']  = resp_json['token']
    return True

# routing
@app.before_request
def before_request():
    if session.get('apiKey') is not None:
        return
    if request.path == '/login':
        return
    return redirect('/login')

@app.route('/', methods=['GET'])
def index():
    error, sims = _call_api('/subscribers', 'GET', {})
    return render_template('index.html', sims=sims, message='', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and _is_authorized():
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('apiKey', None)
    session.pop('token', None)
    return redirect(url_for('login'))

@app.route('/sim/<imsi>/modify', methods=['GET'])
def modify(imsi):
    new_type = request.args.get('new_type')
    old_type = request.args.get('old_type')
    error, sim = _call_api('/subscribers/' + imsi + '/update_speed_class', 'POST', { 'speedClass': new_type })
    message = ''
    if error == '':
        message = 'SIM {} のタイプを {} から {} に変更しました。'.format(imsi, old_type, new_type)
    error, sims = _call_api('/subscribers', 'GET', {})
    return render_template('index.html', sims=sims, message=unicode(message, 'utf-8'), error=error)

@app.route('/sim/<imsi>/activate', methods=['GET'])
def activate(imsi):
    error, sim = _call_api('/subscribers/' + imsi + '/activate', 'POST', {})
    message = ''
    if error == '':
        message = 'SIM {} を利用可能にしました。'.format(imsi)
    error, sims = _call_api('/subscribers', 'GET', {})
    return render_template('index.html', sims=sims, message=unicode(message, 'utf-8'), error=error)

@app.route('/sim/<imsi>/deactivate', methods=['GET'])
def deactivate(imsi):
    error, sim = _call_api('/subscribers/' + imsi + '/deactivate', 'POST', {})
    message = ''
    if error == '':
        message = 'SIM {} を利用可能にしました。'.format(imsi)
    error, sims = _call_api('/subscribers', 'GET', {})
    return render_template('index.html', sims=sims, message=unicode(message, 'utf-8'), error=error)

# main
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
