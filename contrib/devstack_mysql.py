# -*- coding: utf-8 -*-
"""
[murraju] This is an ugly hack to generate an ipallocations id
and populate the portforwards, addressbook, filterrule tables for
GET/POST requests. This is only for devstack or development purposes.
"""

import uuid

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import MetaData


def get_ipallocations_id():
    """Get the ipallocations_id to be used as fixed_id
    """

    try:
        engine = create_engine('mysql://root:openstack@localhost')
        metadata = MetaData(bind=engine)
    except Exception, e:
        raise e
    engine.execute("USE ovs_quantum")
    subnets = engine.execute('select * from subnets limit 1')
    #engine.execute("USE ovs_quantum")
    networks = engine.execute('select * from networks limit 1')

    #Select subnet id (Foreign Key)

    for row in subnets:
        print "using subnet id: ", row['id']
        subnet_id = row['id']

    #Select network id (Foreign Key)
    for row in networks:
        print "using network id: ", row['id']
        network_id = row['id']

    ipallocations_id = uuid.uuid1()
    ipallocations_table = sqlalchemy.Table("ipallocations",
                                           metadata, autoload=True)
    insert_ipallocations_sql = ipallocations_table.insert()
    insert_ipallocations_sql.execute(id=ipallocations_id, port_id=None,
                                     subnet_id=subnet_id,
                                     network_id=network_id,
                                     ip_address='172.16.20.1')
    print ''
    print "Created ipallocations id: ", ipallocations_id
    print ''
    print "Use %s as the fixed_id field for portforward" % ipallocations_id

    return ipallocations_id


def get_tenant_id():
    """get_tenant_id"""
    try:
        engine = create_engine('mysql://root:openstack@localhost')
    except Exception, e:
        raise e

    return ipallocations_id


def get_tenant_id():
    """get_tenant_id"""
    try:
        engine = create_engine('mysql://root:openstack@localhost')
    except Exception, e:
        raise e

    #Select tenant ID for later use
    #Reopen the DB connection to get the tenant_id
    engine.execute("USE keystone")
    tenants = engine.execute(
        'select * from tenant where name=\'admin\' limit 1')
    for row in tenants:
        print "Using tenant id: ", row['id']
        tenant_id = row['id']

    return tenant_id


def populate_portforwards_table(ipallocations_id, tenant_id):
    """Populating sample portforwards.

    """
    try:
        engine = create_engine('mysql://root:openstack@localhost')
        metadata = MetaData(bind=engine)
    except Exception, e:
        raise e

    engine.execute("USE ovs_quantum")
    portforwards_table = sqlalchemy.Table("portforwards",
                                          metadata, autoload=True)
    insert_portfowards_sql = portforwards_table.insert()
    insert_portfowards_sql.execute(
        [
            {'tenant_id': tenant_id, 'id': uuid.uuid4(), 'name': 'foobar1',
             'public_port': '80', 'instance_id': uuid.uuid4(),
             'private_port': '800', 'fixed_id': ipallocations_id,
             'protocol': 'tcp'},
            {'tenant_id': tenant_id, 'id': uuid.uuid4(), 'name': 'foobar2',
             'public_port': '90', 'instance_id': uuid.uuid4(),
             'private_port': '900', 'fixed_id': ipallocations_id,
             'protocol': 'tcp'},
            {'tenant_id': tenant_id, 'id': uuid.uuid4(), 'name': 'foobar3',
             'public_port': '100', 'instance_id': uuid.uuid4(),
             'private_port': '1000', 'fixed_id': ipallocations_id,
              'protocol': 'udp'},

        ])

    print ''
    print "Populating the portforwards table...have fun!"
    print ''


def populate_addressbook_stuff(ipallocations_id, tenant_id):
    """Populating sample portforwards.

    """
    try:
        engine = create_engine('mysql://root:openstack@localhost')
        metadata = MetaData(bind=engine)
    except Exception, e:
        raise e

    #IDs to be used later
    addressbook_group_id = uuid.uuid4()
    addressbook_entries_id = uuid.uuid4()
    addressbooks_id = uuid.uuid4()

    engine.execute("USE ovs_quantum")
    addressbookgroups_table = sqlalchemy.Table("addressbookgroups",
                                          metadata, autoload=True)
    insert_addressbookgroups_sql = addressbookgroups_table.insert()
    insert_addressbookgroups_sql.execute(
        [
            {'tenant_id': tenant_id, 'id': addressbook_group_id,
             'name': 'foobar1', 'table_id': addressbooks_id}

        ])



    print ''
    print "Populating addressbooks...have fun!"
    print ''


def populate_db():
    """populate_db"""
    ipallocations_id = get_ipallocations_id()
    tenant_id = get_tenant_id()
    populate_portforwards_table(ipallocations_id, tenant_id)


populate_db()
