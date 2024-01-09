# Copyright © 2023 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask, request
import requests
import os
from api.utils.cache import cache

def create_app():
    app = Flask(__name__)
    # cache.init_app(app)
    return app

app = create_app()

@app.route('/api/v1/token', methods=['GET'])
def parse_params():
    client = request.args.get('client')
    secret = request.args.get('secret')
    return get_token(client, secret)

# @cache.cached(timeout=300, query_string=True)
def get_token(kc_service_id, kc_secret):
    """Generate a service account token."""
    issuer_url = os.environ['JWT_OIDC_ISSUER']
    token_url = issuer_url + '/protocol/openid-connect/token'
    auth_response = requests.post(token_url, auth=(kc_service_id, kc_secret), headers={
        'Content-Type': 'application/x-www-form-urlencoded'}, data='grant_type=client_credentials')
    auth_response.raise_for_status()
    return auth_response.json().get('access_token')
