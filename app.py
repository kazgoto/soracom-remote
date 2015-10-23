# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, Response
from functools import wraps
from urllib import urlencode
import os
import httplib2
import json

api_url  = 'https://api.soracom.io/v1'
api_auth = {}
app = Flask(__name__)

# functions
def check_auth(username, password):
    global api_auth
    h = httplib2.Http(".cache")
    data = json.dumps({
        "email"    : username,
        "password" : password
    })
    headers = {
        'Content-Type' : 'application/json',
        'Accept'       : 'application/json'
    }
    resp, content = h.request(api_url + '/auth', 'POST', body=data, headers=headers)
    if resp.status != 200:
        print 'Response is bad: ' + str(resp.status) + ' ' + content
        return False

    api_auth = json.loads(content)
    return True

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def api_call(path, method, params):
    h = httplib2.Http(".cache")
    headers = {
        'X-Soracom-API-Key' : api_auth['apiKey'],
        'X-Soracom-Token'   : api_auth['token'],
        'Content-Type'      : 'application/json'
    }
    resp, content = h.request(api_url + path, method, json.dumps(params), headers=headers)
    # print 'path = {}, method = {}, json = {}'.format(path, method, json.dumps(params))
    err = ''
    if resp.status != 200:
        err = 'Response is bad: ' + str(resp.status) + ' ' + content
        exit

    return err, json.loads(content)

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# routing
@app.route('/')
@requires_auth
def index():
    error, sims = api_call('/subscribers', 'GET', {})
    return render_template('index.html', sims=sims, message='', error=error)

@app.route('/sim/<imsi>/modify', methods=['GET'])
def modify(imsi):
    new_type = request.args.get('new_type')
    old_type = request.args.get('old_type')
    error, sim = api_call('/subscribers/' + imsi + '/update_speed_class', 'POST', { 'speedClass': new_type })
    message = ''
    if error == '':
        message = 'SIM {} のタイプを {} から {} に変更しました。'.format(imsi, old_type, new_type)
    else:
        message = error
    error, sims = api_call('/subscribers', 'GET', {})
    return render_template('index.html', sims=sims, message=unicode(message, 'utf-8'), error=error)


# main
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
