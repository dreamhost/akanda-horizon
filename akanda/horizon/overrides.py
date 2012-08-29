from horizon.base import Horizon


nova_dashboard = Horizon.get_dashboard('nova')
compute_panel_group = nova_dashboard.get_panel_group('compute')
compute_panel_group.panels.append('networking')
