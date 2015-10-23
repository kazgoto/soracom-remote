# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from urllib import urlencode
import os
import httplib2
import json

api_url = 'https://api.soracom.io/v1'
auth    = {}

app = Flask(__name__)

@app.route('/')
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

# function
def api_call(path, method, params):
    h = httplib2.Http(".cache")
    headers = {
        'X-Soracom-API-Key' : auth['apiKey'],
        'X-Soracom-Token'   : auth['token'],
        'Content-Type'      : 'application/json'
    }
    resp, content = h.request(api_url + path, method, json.dumps(params), headers=headers)
    print 'path = {}, method = {}, json = {}'.format(path, method, json.dumps(params))
    err = ''
    if resp.status != 200:
        print 'Response is bad: ' + str(resp.status) + ' ' + content
        err = 'Response is bad: ' + str(resp.status) + ' ' + content
        exit
    # print content;
    return err, json.loads(content)

# main
if __name__ == '__main__':
    h = httplib2.Http(".cache")
    data = json.dumps({
        "email"    : os.environ['SORACOM_EMAIL'],
        "password" : os.environ['SORACOM_PASSWORD']
    })
    headers = {
        'Content-Type' : 'application/json',
        'Accept'       : 'application/json'
    }
    resp, content = h.request(api_url + '/auth', 'POST', body=data, headers=headers)
    if resp.status != 200:
        print 'Response is bad: ' + str(resp.status) + ' ' + content
        exit

    auth = json.loads(content)
    app.run(host='0.0.0.0')
