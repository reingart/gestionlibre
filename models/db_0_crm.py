# -*- coding: utf-8 -*-

migrate = True

# Customer Relationship Management

# customers/clients: "Deudores"
db.define_table('customer',
    Field('customer_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('contact_id', 'reference contact'),
    Field('legal_name', type='string', length=50, comment='Customer firm name'),
    Field('address', type='string', length=100, comment='Postal address'),
    Field('zip_code', type='string', length=9),
    Field('city_id', 'reference city'),
    Field('state_id', 'reference state'),
    Field('country_id', 'reference country'),
    Field('fax', type='string', length=20, comment='Fax'),
    Field('telephone', type='string', length=60, comment='Telephone numbers'),
    Field('salesperson_id', 'reference salesperson'), # reference
    Field('price_list_id', 'reference price_list'), # reference
    Field('tax_identification', type='string', length=20, comment='Tax _id'), # similar to Argentina's cuit
    Field('tax_id', 'reference tax'),  # reference
    Field('payment_terms_id', 'reference payment_terms'),  # reference
    Field('invoice', type='string', length=1, comment='Invoice header type'),
    Field('current_account', type='string', length=1, comment='Type of current account'),  # reference?
    Field('situation_id', 'reference situation', comment='Finantial situation'),  # reference
    Field('customer_group_id', 'reference customer_group', comment='Contact Group'),  # reference
    Field('observations', type='text'),
    Field('place_of_delivery', type='text'),
    Field('supplier', 'string'), # no reference (customer entry)
    Field('addition', type='datetime', comment='Customer starting date'),
    Field('deletion', type='datetime', comment='Customer deletion date'),
    Field('replica', type='boolean', default=False),
    Field('current_account_limit', type='double'),
    Field('check_limit', type='double'),
    Field('jurisdiction_id', 'reference jurisdiction'),  # reference
    Field('debt_limit', type='decimal(10,2)'),
    Field('id_number'), # Argentina's DNI
    Field('transport'),
    Field('replica', type='boolean', default=False),
    format='%(legal_name)s',
    migrate=migrate)

# sub-customers ("sub-accounts") "CLIENTES"
db.define_table('subcustomer',
    Field('subcustomer_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('customer_id', 'reference customer'),  # reference
    Field('legal_name', type='string', length=50),
    Field('address', type='string', length=100),
    Field('zip_code', type='string', length=4),
    Field('city_id', 'reference city'),
    Field('state_id', 'reference state'),  # reference
    Field('country_id', 'reference country'), # reference
    Field('fax', type='string', length=20),
    Field('telephone', type='string', length=60),
    Field('tax_id', 'reference tax'),  # reference
    Field('tax_identification'),  # reference
    Field('invoice', type='string', length=1),
    Field('current_account', type='string', length=1),  # reference?
    Field('price_list_id', 'reference price_list'),  # reference
    Field('situation_id', 'reference situation'),  # reference
    Field('customer_group_id', 'reference customer_group'),  # reference
    Field('observations', type='text'),
    Field('place_of_delivery', type='text'),
    Field('supplier', 'string'),  # no reference (subcustomer entry)
    Field('addition', type='datetime'),
    Field('deletion', type='datetime'),
    Field('current_account_limit', type='double'),
    Field('check_limit', type='double'),
    Field('jurisdiction_id', 'reference jurisdiction'), # reference
    Field('sex', type="string", length=1),
    Field('birth', type='date'),
    Field('balance', type='double'),
    Field('replica', type='boolean', default=False),
    format='%(legal_name)s',
    migrate=migrate)

# groups
db.define_table('customer_group',
    Field('customer_group_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

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

# memos messages
db.define_table('memo',
    Field('memo_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('posted', type='date'),
    Field('contact_id', 'reference contact'),  # reference
    Field('subject', type='string', length=50),
    Field('observations', type='text'),
    Field('user_id', 'reference auth_user'),  # reference
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

# many to many referenced user-contact table
db.define_table('contact_user',
    Field('contact_user_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('user_id', 'reference auth_user'),
    Field('contact_id', 'reference contact'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    )
