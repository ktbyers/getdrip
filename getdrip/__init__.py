'''
Python Wrapper for getdrip https://www.getdrip.com/
MIT License
'''
from __future__ import unicode_literals
from __future__ import print_function
import requests
import json

__version__ = '1.3.0'


class TokenNotFoundException(Exception):
    pass


class AccountIDNotFound(Exception):
    pass


class GetDripAPI(object):
    def __init__(self, token=None, account_id=None, api_key=None):
        if not account_id:
            raise AccountIDNotFound('Please provide account id')
        self.headers = {}
        self.account_id = account_id
        self.api_url = 'https://api.getdrip.com/v2'
        if api_key:
            self.auth = 'basic'
            self.user_passwd = (api_key, '')
        elif token:
            self.auth = 'auth_header'
            self.token = token
            self.headers['Authorizion'] = 'Bearer %s' % self.token
        self.headers['User-Agent'] = 'getdrip Python'
        self.headers['Content-Type'] = 'application/vnd.api+json'
        self.headers['Accept'] = '*/*'

    def api_get(self, url):
        if self.auth == 'auth_header':
            response = requests.get(url, headers=self.headers)
        elif self.auth == 'basic':
            response = requests.get(url, headers=self.headers, auth=self.user_passwd)
        return response.status_code, response.json()

    def api_post(self, url, payload=None):
        if self.auth == 'auth_header':
            if payload:
                response = requests.post(url, headers=self.headers, data=json.dumps(payload))
            else:
                response = requests.post(url, headers=self.headers)
        elif self.auth == 'basic':
            if payload:
                response = requests.post(url, headers=self.headers, auth=self.user_passwd,
                                         data=json.dumps(payload))
            else:
                response = requests.post(url, headers=self.headers, auth=self.user_passwd)
        return response.status_code, response.json()

    def api_delete(self, url):
        if self.auth == 'auth_header':
            response = requests.delete(url, headers=self.headers)
        elif self.auth == 'basic':
            response = requests.delete(url, headers=self.headers, auth=self.user_passwd)
        return response.status_code

    def fetch_all_campaign(self):
        """List campaigns."""
        url = '%s/%s/campaigns/' % (self.api_url, self.account_id)
        return self.api_get(url)

    def fetch_campaign(self, campaign_id):
        url = '%s/%s/campaigns/%s' % (self.api_url, self.account_id, campaign_id)
        return self.api_get(url)

    def fetch_accounts(self):
        url = '%s/accounts' % (self.api_url)
        return self.api_get(url)

    def create_or_update_subscriber(self, payload):
        url = '%s/%s/subscribers' % (self.api_url, self.account_id)
        return self.api_post(url, payload=payload)

    def create_or_update_subscriber_batch(self, payload):
        url = '%s/%s/subscribers/batches' % (self.api_url, self.account_id)
        return self.api_post(url, payload=payload)

    def fetch_subscriber(self, subscriber_id):
        url = '%s/%s/subscribers/%s' % (self.api_url, self.account_id, subscriber_id)
        return self.api_get(url)

    def subscribe_subscriber(self, campaign_id, payload):
        """Subscribe a subscriber to a campaign."""
        url = '%s/%s/campaigns/%s/subscribers' % (self.api_url, self.account_id, campaign_id)
        return self.api_post(url, payload=payload)

    def list_of_all_subscribers(self, page=None):
        if not page:
            url = '%s/%s/subscribers' % (self.api_url, self.account_id)
        else:
            url = '%s/%s/subscribers?page=%s' % (self.api_url, self.account_id, str(page))
        return self.api_get(url)

    def delete_subscriber(self, subscriber_id):
        url = '%s/%s/subscribers/%s' % (self.api_url, self.account_id, subscriber_id)
        return self.api_delete(url)

    def campaign_subscriber(self, subscriber_id):
        """GET /:account_id/subscribers/:subscriber_id/campaign_subscriptions"""
        url = '%s/%s/subscribers/%s/campaign_subscriptions' % (self.api_url, self.account_id,
                                                               subscriber_id)
        return self.api_get(url)

    def activate_campaign(self, campaign_id):
        url = '%s/%s/campaigns/%s/activate' % (self.api_url, self.account_id, campaign_id)
        status_code, _ = self.api_post(url)
        return status_code

    def pause_campaign(self, campaign_id):
        url = '%s/%s/campaigns/%s/pause' % (self.api_url, self.account_id, campaign_id)
        status_code, _ = self.api_post(url)
        return status_code

    def fetch_everyone_subscribed_to_campaign(self, campaign_id):
        url = '%s/%s/campaigns/%s/subscribers' % (self.api_url, self.account_id, campaign_id)
        return self.api_get(url)

    def tag_a_subscriber(self, payload):
        url = '%s/%s/tags' % (self.api_url, self.account_id)
        return self.api_post(url, payload=payload)

    def untag_a_subscriber(self, email, tag):
        url = '%s/%s/subscribers/%s/tags/%s' % (self.api_url, self.account_id, email, tag)
        return self.api_delete(url)

    def fetch_a_form(self, form_id):
        url = '%s/%s/forms/%s' % (self.api_url, self.account_id, form_id)
        return self.api_get(url)

    def fetch_list_of_goals(self):
        url = '%s/%s/goals' % (self.api_url, self.account_id)
        return self.api_get(url)

    def fetch_goal(self, goal_id):
        url = '%s/%s/goals/%s' % (self.api_url, self.account_id, goal_id)
        return self.api_get(url)
