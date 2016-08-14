'''
Python Wrapper for getdrip https://www.getdrip.com/
Nishant Nawarkhede
nishant.nawarkhede@gmail.com
MIT License
'''
from __future__ import unicode_literals
import requests
#from requests.auth import HTTPBasicAuth
import json


class TokenNotFoundException(Exception):
    pass


class AccountIDNotFound(Exception):
    pass


class GetDripAPI(object):
    def __init__(self, token=None, account_id=None, api_key=None):
        #if not token:
        #    raise TokenNotFoundException('Please provide token.')
        if not account_id:
            raise AccountIDNotFound('Please provide account id')
        if api_key:
            self.auth = 'basic'
            self.user_passwd = (api_key, '')
        elif token:
            self.auth = 'auth_header'
            self.token = token
        self.account_id = account_id
        self.api_url = 'https://api.getdrip.com/v2'
        self.headers = {}
        #self.headers['Authorizion'] = 'Bearer %s' % self.token
        #self.headers['User-Agent'] = 'Drip Python'
        self.headers['Content-Type'] = 'application/vnd.api+json'
        #self.headers['Accept'] = 'application/json'
        self.headers['Accept'] = '*/*'

    def api_get(self, url):
        if self.auth == 'auth_header':
            response = requests.get(url, headers=self.headers)
        elif self.auth == 'basic':
            response = requests.get(url, auth=self.user_passwd)
        return response.status_code, response.json()

    def fetch_all_campaign(self):
        url = '%s/%s/campaigns/' % (self.api_url, self.account_id)
        if self.auth == 'auth_header':
            response = requests.get(url, headers=self.headers)
        elif self.auth == 'basic':
            response = requests.get(url, auth=self.user_passwd)
        return response.status_code, response.json()

    def fetch_campaign(self, campaign_id):
        url = '%s/%s/campaigns/%s' % (self.api_url, self.account_id, campaign_id)
        response = requests.get(url, headers=self.headers)
        return response.status_code, response.json()

    def fetch_accounts(self):
        url = '%s/accounts'%(self.api_url)
        response = requests.get(url, headers=self.headers)
        return response.status_code, response.json()

    def create_or_update_subscriber(self, payload):
        url = '%s/%s/subscribers' % (self.api_url, self.account_id)
        print url
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))
        return response.status_code, response.json()

    def create_or_update_subscriber_batch(self, payload):
        url = '%s/%s/subscribers/batches' % (self.api_url, self.account_id)
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))
        return response.status_code, response.json()

    def fetch_subscriber(self, subscriber_id):
        url = '%s/%s/subscribers/%s' % (self.api_url, self.account_id, subscriber_id)
        response = requests.get(url, headers=self.headers)
        return response.status_code, response.json()

    def subscribe_subscriber(self, campaign_id, payload):
        url = '%s/%s/campaigns/%s/subscribers' % (self.api_url, self.account_id, campaign_id)
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))
        return response.status_code, response.json()

    def list_of_all_subscribers(self):
        url = '%s/%s/subscribers' % (self.api_url, self.account_id)
        response = requests.get(url, headers=self.headers)
        return response.status_code, response.json()

    def delete_subscriber(self, subscriber_id):
        url = '%s/%s/subscribers/%s' % (self.api_url, self.account_id, subscriber_id)
        response = requests.delete(url, headers=self.headers)
        return response.status_code

    def activate_campaign(self, campaign_id):
        url = '%s/%s/campaigns/%s/activate' % (self.api_url, self.account_id, campaign_id)
        response = requests.post(url, headers=self.headers)
        return response.status_code

    def pause_campaign(self, campaign_id):
        url = '%s/%s/campaigns/%s/pause' % (self.api_url, self.account_id, campaign_id)
        response = requests.post(url, headers=self.headers)
        return response.status_code

    def fetch_everyone_sucbscribed_to_campaign(self, campaign_id):
        url = '%s/%s/campaigns/%s/subscribers' % (self.api_url, self.account_id, campaign_id)
        response = requests.get(url, headers=self.headers)
        return response.status_code, response.json()

    def tag_a_subscriber(self, payload):
        url = '%s/%s/tags' % (self.api_url, self.account_id)
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))
        return response.status_code, response.json()

    def untag_a_subscriber(self, email, tag):
        url = '%s/%s/subscribers/%s/tags/%s' % (self.api_url, self.account_id, email, tag)
        response = requests.delete(url, headers=self.headers)
        return response.status_code

    def fetch_a_form(self, form_id):
        url = '%s/%s/forms/%s' % (self.api_url, self.account_id, form_id)
        response = requests.get(url, headers=self.headers)
        return response.status_code, response.json()

    def fetch_list_of_goals(self):
        url = '%s/%s/goals' % (self.api_url, self.account_id)
        response = requests.get(url, headers=self.headers)
        return response.status_code, response.json()

    def fetch_goal(self, goal_id):
        url = '%s/%s/goals/%s' % (self.api_url, self.account_id, goal_id)
        response = requests.get(url, headers=self.headers)
        return response.status_code, response.json()
