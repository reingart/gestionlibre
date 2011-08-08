# -*- coding: utf-8 -*-
migrate = True

# groups
db.define_table('customer_group',
    Field('customer_group_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)
 
# status (active, unactive, prospect, etc.)
db.define_table('situation',
    Field('situation_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

