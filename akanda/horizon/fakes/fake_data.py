# Fake data for Port Aliases
# .. attribute:: id
#         Fake implementation detail
#
# .. attribute:: alias_name
#         type: string(free text)??
#
# .. attribute:: protocol
#         type: integer??
#
#         PROTOCOL_CHOICES = (
#             (0, 'TCP'),
#             (1, 'UDP'),
#             (2, 'TCP+UDP'),
#        )
#
# .. attribute:: ports
#         type: list of integers??
#
# Note(rods): we need to define data types in order to write forms' validation
port_aliases_fake_data = {
    'df698e967f554e4284583c10ba326c5b': {
        'id': 'df698e967f554e4284583c10ba326c5b',
        'alias_name': 'FTP',
        'protocol': 0,
        'ports': [21, 22],
    },
    '6269ee9f6dcd4a099b9551fb8ad27a3a': {
        'id': '6269ee9f6dcd4a099b9551fb8ad27a3a',
        'alias_name': 'SSH',
        'protocol': 0,
        'ports': [22]
    },
    'd50abcd19dd04f788ae9ebed3865460e': {
        'id': 'd50abcd19dd04f788ae9ebed3865460e',
        'alias_name': 'SMTP',
        'protocol': 0,
        'ports': [25],
    },
    '13bbcf90c97f4cbdac446ecf8e6b893b': {
        'id': '13bbcf90c97f4cbdac446ecf8e6b893b',
        'alias_name': 'MySQL',
        'protocol': 2,
        'ports': [3306],
    }
}


# Fake instances
instances_fake_data = {
    '015eff2961d8430ba0c7c483fcb2da7a': {
        'id': '015eff2961d8430ba0c7c483fcb2da7a',
        'name': 'Instance 1',
    },
    '7f256428dbfe4bec91e643fac513778e': {
        'id': '7f256428dbfe4bec91e643fac513778e',
        'name': 'Instance 2',
    },
    '7f96521d5e8345878f6924f6d75c2884': {
        'id': '7f96521d5e8345878f6924f6d75c2884',
        'name': 'Instance 3',
    },
    'a5456395a9e3476d96af4aafb6880a3d': {
        'id': 'a5456395a9e3476d96af4aafb6880a3d',
        'name': 'Instance 4',
    }
}


#  Fake data for Host Aliases
# .. attribute:: id
#         Fake implementation detail
#
# .. attribute:: alias_name
#         type: string(free text)??
#
# .. attribute:: instances
#         type: list of instances id??
#
# Note(rods): we need to define data types in order to write forms' validation
host_aliases_fake_data = {
    '8b26e7e8cedd4bdf86e2a8f433bbc0f8': {
        'id': '8b26e7e8cedd4bdf86e2a8f433bbc0f8',
        'alias_name': 'New Host Alias',
        'instances': ['015eff2961d8430ba0c7c483fcb2da7a',
                      '7f256428dbfe4bec91e643fac513778e',
                      '7f96521d5e8345878f6924f6d75c2884']
    },
}


#  Fake data for Host Aliases
# .. attribute:: id
#         Fake implementation detail
#
# .. attribute:: alias_name
#         type: string(free text)??
#
# .. attribute:: cidr
#         type: string??
#
# Note(rods): we need to define data types in order to write forms' validation
network_aliases_fake_data = {
    'cefa80f7f3aa451ba48a3a8b10347a27': {
        'id': 'cefa80f7f3aa451ba48a3a8b10347a27',
        'alias_name': 'Network 1',
        'cidr': '192.168.0.1/12'
    },
    '872bd2fa41df41679a38d01ca50bf754': {
        'id': '872bd2fa41df41679a38d01ca50bf754',
        'alias_name': 'Network 2',
        'cidr': '2001:cdba:0000:0000:0000:0000:3257:9652'
    },
    '1c2b68b81e2c4586a6f091ac565659e1': {
        'id': '1c2b68b81e2c4586a6f091ac565659e1',
        'alias_name': 'Network 3',
        'cidr': '111.120.0.0/14'
    },
    'c8fd91727f6148b28fd11eb54db2a3ad': {
        'id': 'c8fd91727f6148b28fd11eb54db2a3ad',
        'alias_name': 'Network 4',
        'cidr': '122.255.64.0/21'
    },
    'f1f7a93c721f45eba42e8cff5ce7530e': {
        'id': 'f1f7a93c721f45eba42e8cff5ce7530e',
        'alias_name': 'Network 5',
        'cidr': '2001:cdba::3257:9652'
    },
    '1d2c01d7285447cc893107e09c21d427': {
        'id': '1d2c01d7285447cc893107e09c21d427',
        'alias_name': 'Network 6',
        'cidr': '122.198.0.0/28'
    },
    'd462717864fc42ea959ae9f73fb037e5': {
        'id': 'd462717864fc42ea959ae9f73fb037e5',
        'alias_name': 'Network 7',
        'cidr': '69.197.56.16/28'
    },
}

#  Fake data for Firewall Rules
# .. attribute:: id
#         Fake implementation detail
#
# .. attribute:: policy
#         type: integer??
#
#         POLICY_CHOICES = (
#            (0, 'Allow'),
#            (1, 'Deny'),
#         )
#
# .. attribute:: source_network_alias/destination_network_alias
#         The id of the Source/Destination Network Alias
#         type: string??
#
# .. attribute:: source_port_alias/destination_port_alias
#         The id of the Source/Destination Port Alias or some other value if
#         the user select custom and fill in the protocol and public port
#         fields. Right now we are using 'Custom' as value but something like
#         '-1' or '00000000000000000000000000000000' would be better.
#         type: string??
#
# .. attribute:: source_protocol/destination_protocol
#         type: integer??
#
#         PROTOCOL_CHOICES = (
#             (0, 'TCP'),
#             (1, 'UDP'),
#             (2, 'TCP+UDP'),
#        )
#
# .. attribute: source_public_ports/destination_public_ports
#         type: list of integers??
#
# Note(rods): we need to define data types in order to write forms' validation
firewall_rules_fake_data = {
    'b68292e067834ba48e17c2c827b99f31': {
        'id': 'b68292e067834ba48e17c2c827b99f31',
        'policy': 0,
        'source_network_alias': 'cefa80f7f3aa451ba48a3a8b10347a27',
        'source_port_alias': 'Custom',
        'source_protocol': 0,
        'source_public_ports': [24],
        'destination_network_alias': 'cefa80f7f3aa451ba48a3a8b10347a27',
        'destination_port_alias': 'Custom',
        'destination_protocol': 0,
        'destination_public_ports': [80],
    },
    'a39255cfbb0e44c6b542a531a3e5528a': {
        'id': 'a39255cfbb0e44c6b542a531a3e5528a',
        'policy': 1,
        'source_network_alias': '872bd2fa41df41679a38d01ca50bf754',
        'source_port_alias': 'Custom',
        'source_protocol': 0,
        'source_public_ports': [125],
        'destination_network_alias': '872bd2fa41df41679a38d01ca50bf754',
        'destination_port_alias': 'Custom',
        'destination_protocol': 0,
        'destination_public_ports': [2007],
    }
}

#  Fake data for Port Forwarding Rules
# .. attribute:: id
#         Fake implementation detail
#
# .. attribute:: rule_name
#         type: string(free text)??
#
# .. attribute:: instance
#         Instance id
#         type: string??
#
# .. attribute:: public_port_alias/private_port_alias
#         The id of the Public/Private Port Alias or some other value if
#         the user select custom and fill in the protocol and public port
#         fields. Right now we are using 'Custom' as value but something like
#         '-1' or '00000000000000000000000000000000' would be better.
#         type: string??
#
# .. attribute:: public_protocol/private_protocol
#         type: integer??
#
#         PROTOCOL_CHOICES = (
#             (0, 'TCP'),
#             (1, 'UDP'),
#             (2, 'TCP+UDP'),
#        )
#
# .. attribute: public_ports/private_ports
#         type: list of integers??
#
# Note(rods): we need to define data types in order to write forms' validation
portforwarding_rules_fake_data = {
    'fc15f8956de74ec5aa10e8335e5191ee': {
        'id': 'fc15f8956de74ec5aa10e8335e5191ee',
        'rule_name': 'Rule 1',
        'instance': '015eff2961d8430ba0c7c483fcb2da7a',
        'public_port_alias': 'df698e967f554e4284583c10ba326c5b',
        'public_protocol': 0,
        'public_ports': [21, 22],
        'private_port_alias': 'Custom',
        'private_protocol': 2,
        'private_ports': [8000],
    },
    '0b23fe767c1e4160b5b68d82b0f74518': {
        'id': '0b23fe767c1e4160b5b68d82b0f74518',
        'rule_name': 'Rule 2',
        'instance': '015eff2961d8430ba0c7c483fcb2da7a',
        'public_port_alias': 'Custom',
        'public_protocol': 0,
        'public_ports': [125],
        'private_port_alias': 'Custom',
        'private_protocol': 0,
        'private_ports': [2007],
    },
    '68fc216ced5c44b2a5041345d0265f04': {
        'id': '68fc216ced5c44b2a5041345d0265f04',
        'rule_name': 'Rule 3',
        'instance': '7f256428dbfe4bec91e643fac513778e',
        'public_port_alias': 'df698e967f554e4284583c10ba326c5b',
        'public_protocol': 0,
        'public_ports': [21, 22],
        'private_port_alias': 'Custom',
        'private_protocol': 2,
        'private_ports': [8000],
    },
}
