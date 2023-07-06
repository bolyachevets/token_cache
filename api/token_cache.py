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

app = Flask(__name__)
cache.init_app(app)

@app.route('/api/v1/token', methods=['GET'])
@cache.cached(timeout=10)
def get_token():
    """Generate a service account token."""
    kc_service_id = request.args.get('client')
    kc_secret = request.args.get('secret')
    issuer_url = os.environ['JWT_OIDC_ISSUER']
    token_url = issuer_url + '/protocol/openid-connect/token'
    auth_response = requests.post(token_url, auth=(kc_service_id, kc_secret), headers={
        'Content-Type': 'application/x-www-form-urlencoded'}, data='grant_type=client_credentials')
    auth_response.raise_for_status()
    return auth_response.json().get('access_token')
