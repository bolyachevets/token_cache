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

cache_servers = os.environ.get('CACHE_MEMCACHED_SERVERS')

if not cache_servers == None:
    cache = Cache(config={  'CACHE_TYPE': 'MemcachedCache',
                        'CACHE_MEMCACHED_SERVERS': cache_servers.split(',') })
else:

    redis_host = os.environ.get('CACHE_REDIS_HOST')
    redis_port = os.environ.get('CACHE_REDIS_PORT')

    if not redis_host == None and not redis_port == None:
        cache = Cache(config={  'CACHE_TYPE': 'RedisCache',
                        'CACHE_REDIS_HOST': redis_host,
                        'CACHE_REDIS_PORT': redis_port })

    else:
        cache = Cache(config={'CACHE_TYPE': 'simple'})  # pylint: disable=invalid-name
