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
