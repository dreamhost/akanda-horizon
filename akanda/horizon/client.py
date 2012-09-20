# Copyright 2012 New Dream Network, LLC (DreamHost)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# DreamHost Qauntum Extensions
# @author: Murali Raju, New Dream Network, LLC (DreamHost)
# @author: Rosario Disomma, New Dream Network, LLC (DreamHost)

import requests
import json


def portforward_get(request):
    headers = {
        "User-Agent": "python-quantumclient",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Auth-Token": request.user.token.id
    }
    r = requests.get('http://0.0.0.0/v2.0/dhportforward.json', headers=headers)
    r.json


def portforward_post(request, payload):
    headers = {
        "User-Agent": "python-quantumclient",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Auth-Token": request.user.token.id
    }
    r = requests.post('http://0.0.0.0/v2.0/dhportforward.json',
                      headers=headers, data=json.dumps(payload))
    r.json
