# -*- coding: utf-8 -*-

migrate = True

# pricelists
db.define_table('price_list',
    Field('price_list_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('entry', type='boolean', default=False),
    Field('exit', type='boolean', default=False),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

# points of sale
db.define_table('point_of_sale',
    Field('point_of_sale_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('branch'),
    Field('number', type='integer', default=0),
    Field('authorization_code', type='string', length=50), # Argentina's CAI (invoice printing official number)
    Field('due_date', type='datetime'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)


