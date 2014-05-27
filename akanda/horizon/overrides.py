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


from horizon.base import Horizon


nova_dashboard = Horizon.get_dashboard('project')
compute_panel_group = nova_dashboard.get_panel_group('network')
compute_panel_group.panels.append('networking')

#
# Manually override the definition of the router detail view method
# to properly look up port data w/ akanda. May God have mercy on my soul.
#
from openstack_dashboard.dashboards.project.routers import views
from akanda.horizon.routers.views import get_interfaces_data
views.DetailView.get_interfaces_data = get_interfaces_data
