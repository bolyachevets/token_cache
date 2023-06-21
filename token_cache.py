from flask import Flask, request
import requests
from datetime import datetime, timedelta
import os

app = Flask(__name__)

service_token_cache = {}


@app.route('/api/v1/token', methods=['GET'])
def get_token():
    """Generate a service account token."""
    kc_service_id = request.args.get('client')
    kc_secret = request.args.get('secret')
    if kc_service_id in service_token_cache and _token_not_expired(service_token_cache[kc_service_id][1]):
        return service_token_cache[kc_service_id][0]
    else:
        issuer_url = os.environ['JWT_OIDC_ISSUER']
        token_url = issuer_url + '/protocol/openid-connect/token'
        auth_response = requests.post(token_url, auth=(kc_service_id, kc_secret), headers={
            'Content-Type': 'application/x-www-form-urlencoded'}, data='grant_type=client_credentials')
        auth_response.raise_for_status()
        service_token_cache[kc_service_id] = (auth_response.json().get('access_token'), datetime.now())
        return auth_response.json().get('access_token')

def _token_not_expired(creation_date)-> bool:
    span = os.environ['TOKEN_LIFESPAN']
    margin = os.environ['TOKEN_EXPIRY_MARGIN_IN_MINS']
    kc_token_lifespan = int(span) - int(margin)
    return datetime.now() - creation_date < timedelta(minutes=kc_token_lifespan)
