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


from horizon import tabs

from akanda.horizon.tabs import NetworkingTabs


class IndexView(tabs.TabbedTableView):
    template_name = 'akanda/index.html'
    tab_group_class = NetworkingTabs

    def get(self, request, *args, **kwargs):
        return super(IndexView, self).get(request, *args, **kwargs)
