# Copyright 2012 OpenStack LLC.
# Copyright 2012 New Dream Network, LLC (DreamHost)
# All Rights Reserved
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# DreamHost Python Quantum Client additions
# to consume DreamHost Quantum extensions
# @author: Murali Raju, New Dream Network, LLC (DreamHost)


import logging
import argparse

from cliff import lister
from cliff import show

from quantumclient.common import utils
from quantumclient.quantum.v2_0 import QuantumCommand
from quantumclient.quantum.v2_0 import CreateCommand
from quantumclient.quantum.v2_0 import DeleteCommand
from quantumclient.quantum.v2_0 import ListCommand
from quantumclient.quantum.v2_0 import UpdateCommand


class ListPortforward(ListCommand):
    """List portfowards that belong to a given tenant."""

    api = 'network'
    resource = 'dhportforward'
    log = logging.getLogger(__name__ + '.ListPortforward')
    _formatters = {}
    # Listing the table is not working. Use --verbose for JSON output.
    # list_columns = ['id', 'name', 'public_port',
    #                 'instance_id', 'private_port',
    #                 'fixed_id', 'op_status']

    def get_parser(self, prog_name):
        parser = super(ListPortforward, self).get_parser(prog_name)
        return parser

    def get_data(self, parsed_args):
        self.log.debug('get_data(%s)' % parsed_args)
        quantum_client = self.get_client()
        search_opts = {}
        quantum_client.format = parsed_args.request_format
        obj_lister = getattr(quantum_client,
                             "list_%ss" % self.resource)
        data = obj_lister(**search_opts)
        info = []
        collection = self.resource + "s"
        if collection in data:
            info = data[collection]
        _columns = len(info) > 0 and sorted(info[0].keys()) or []
        return (_columns, (utils.get_item_properties(s, _columns)
                for s in info))


class CreatePortforward(CreateCommand):
    """Create a portforward for a given tenant."""

    api = 'network'
    resource = 'dhportforward'
    log = logging.getLogger(__name__ + '.CreatePortforward')
    _formatters = None

    def get_parser(self, prog_name):
        parser = super(CreatePortforward, self).get_parser(prog_name)
        return parser

    def get_data(self, parsed_args):
        self.log.debug('get_data(%s)' % parsed_args)
        quantum_client = self.get_client()
        search_opts = {}
        quantum_client.format = parsed_args.request_format
        obj_lister = getattr(quantum_client,
                             "list_%ss" % self.resource)
        data = obj_lister(**search_opts)
        info = []
        collection = self.resource + "s"
        if collection in data:
            info = data[collection]
        _columns = len(info) > 0 and sorted(info[0].keys()) or []
        return (_columns, (utils.get_item_properties(s, _columns)
                for s in info))

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--op-status', metavar='op_status',
            help='Operational Status')
        parser.add_argument(
            '--name', metavar='name',
            help='Name of portforward to create')
        parser.add_argument(
            '--public-port', metavar='public_port',
            help='Public port to create')
        parser.add_argument(
            '--instance-id', metavar='instance_id',
            help='Instance ID to use')
        parser.add_argument(
            '--private-port', metavar='private_port',
            help='Private port to create')
        parser.add_argument(
            '--fixed-id', metavar='fixed_id',
            help='IPAllocations ID to use')

    def args2body(self, parsed_args):
        body = {'portforward': {
            'name': parsed_args.name,
            'public_port': parsed_args.public_port,
            'instance_id': parsed_args.instance_id,
            'private_port': parsed_args.private_port,
            'fixed_id': parsed_args.fixed_id,
            'op_status': parsed_args.op_status}, }
        if parsed_args.tenant_id:
            body['portforward'].update({'tenant_id': parsed_args.tenant_id})
        return body
