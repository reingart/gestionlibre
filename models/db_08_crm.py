# -*- coding: utf-8 -*-

migrate = True

# contacts
db.define_table('contact',
    Field('contact_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('customer_id', 'reference customer'),  # reference
    Field('supplier_id', 'reference supplier'),  # reference
    Field('tax_identification'),  # Argentina's CUIT
    Field('department', type='string', length=50),  # reference?
    Field('telephone', type='string', length=100),
    Field('fax', type='string', length=100),
    Field('email', type='string', length=100),
    Field('schedule', type='string', length=100),
    Field('address', type='string', length=50),
    Field('zip_code', type='string', length=50, comment='Zip code'),
    Field('city_id', 'reference city'),  # reference
    Field('state_id', 'reference state'),  # reference
    Field('observations', type='text'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)
 
