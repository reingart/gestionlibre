# -*- coding: utf-8 -*-
migrate = True

# customers/clients: "Deudores"
db.define_table('customer',
    Field('customer_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('contact'),
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
 
