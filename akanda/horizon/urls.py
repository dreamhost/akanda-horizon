# Copyright 2014 DreamHost, LLC 
#
# Author: DreamHost, LLC 
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


from django.conf.urls.defaults import patterns, url, include

from .views import IndexView

from akanda.horizon.alias import urls as alias_urls
from akanda.horizon.firewall import urls as firewall_urls
from akanda.horizon.portforwarding import urls as forwarding_rules
from akanda.horizon.network_topology import urls as topology_urls

urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'alias/', include(alias_urls, namespace='alias'),),
    url(r'firewall/', include(firewall_urls, namespace='firewall'),),
    url(r'forwarding/', include(forwarding_rules, namespace='forwarding'),),
    url(r'topology/', include(topology_urls, namespace='topology'),),
)
