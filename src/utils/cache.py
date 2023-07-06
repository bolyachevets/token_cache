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


"""Bring in the common cache."""
from flask_caching import Cache
import os

cache_servers = os.environ.get('MEMCACHIER_SERVERS')
if cache_servers == None:
    # lower case name as used by convention in most Flask apps
    cache = Cache(config={'CACHE_TYPE': 'simple'})  # pylint: disable=invalid-name
else:
    cache_user = os.environ.get('MEMCACHIER_USERNAME') or ''
    cache_pass = os.environ.get('MEMCACHIER_PASSWORD') or ''
    cache = Cache(config={  'CACHE_TYPE': 'memcached',
                            'CACHE_MEMCACHED_SERVERS': cache_servers.split(','),
                            'CACHE_MEMCACHED_USERNAME': cache_user,
                            'CACHE_MEMCACHED_PASSWORD': cache_pass,
                            'CACHE_OPTIONS': { 'behaviors': {
                                # Faster IO
                                'tcp_nodelay': True,
                                # Keep connection alive
                                'tcp_keepalive': True,
                                # Timeout for set/get requests
                                'connect_timeout': 2000, # ms
                                'send_timeout': 750 * 1000, # us
                                'receive_timeout': 750 * 1000, # us
                                '_poll_timeout': 2000, # ms
                                # Better failover
                                'ketama': True,
                                'remove_failed': 1,
                                'retry_timeout': 2,
                                'dead_timeout': 30}}
                        }
            )
