# -*- coding: utf-8 -*-

migrate = True

# collections "Colecciones"
db.define_table('collection',
    Field('collection_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('starting', type='date'),
    Field('ending', type='date'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

# colours (products 1st variant)
db.define_table('color',
    Field('color_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

# sizes (products 2nd variant ) ie. clothes...
db.define_table('size',
    Field('size_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('type'),
    Field('order_number', 'integer'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

# warehouses
db.define_table('warehouse',
    Field('warehouse_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('address', type='string', length=50),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)
 
# rates / fare / tariff
db.define_table('rate',
    Field('rate_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('type', type='string', length=1),  # reference?
    Field('capacity', type='double'),
    Field('measure', type='string', length=1),
    Field('stock', type='integer', default=0),
    Field('index_value', type='double', default=0),
    Field('price', type='double', default=0),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)
