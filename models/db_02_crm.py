# -*- coding: utf-8 -*-
migrate = True

# salesman
db.define_table('salesperson',
    Field('salesperson_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('staff_id', 'reference staff'), # reference
    Field('commission', type='double'),
    Field('telephone', type='string', length=50),
    Field('address', type='string', length=50),
    Field('state_id', 'reference state'),  # reference
    Field('city_id', 'reference city'),  # reference
    Field('notes', type='text'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)
 
