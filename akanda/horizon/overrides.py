from horizon.base import Horizon


nova_dashboard = Horizon.get_dashboard('project')
compute_panel_group = nova_dashboard.get_panel_group('network')
compute_panel_group.panels.append('networking')
