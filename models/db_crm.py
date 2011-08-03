# -*- coding: utf-8 -*-

migrate = True

# Customer Relationship Management

# customers/clients: "Deudores"
db.define_table('customer',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('contact', 'reference contact'),
    Field('firmname', type='string', length=50, comment='Customer firm name'),
    Field('address', type='string', length=100, comment='Postal address'),
    Field('zipcode', type='string', length=9),
    Field('city', type='string', length=20),
    Field('state', type='integer', default=0),
    Field('country', type='string', length=15),
    Field('fax', type='string', length=20, comment='Fax'),
    Field('telephone', type='string', length=60, comment='Telephone numbers'),
    Field('salesperson', 'reference salesperson'), # reference
    Field('pricelist', 'reference pricelist'), # reference
    Field('tin', type='string', length=20, comment='Tax id'), # similar to Argentina's cuit
    Field('vat', 'reference vat'),  # reference
    Field('paymentterms', 'reference paymentterms'),  # reference
    Field('invoice', type='string', length=1, comment='Invoice header type'),
    Field('currentaccount', type='string', length=1, comment='Type of current account'),  # reference?
    Field('situation', 'reference situation', comment='Finantial situation'),  # reference
    Field('contactgroup', 'reference contactgroup', comment='Contact Group'),  # reference
    Field('observations', type='text'),
    Field('placeofdelivery', type='text'),
    Field('purveyor', 'reference purveyor'), # reference
    Field('addition', type='datetime', comment='Customer starting date'),
    Field('deletion', type='datetime', comment='Customer deletion date'),
    Field('replica', type='boolean', default=False),
    Field('currentaccountlimit', type='double'),
    Field('checklimit', type='double'),
    Field('jurisdiction', 'reference jurisdiction'),  # reference
    Field('debtlimit', type='decimal(10,2)'),
    Field('ssn'), # Argentina's DNI
    Field('transport'),
    Field('replica', type='boolean', default=False),
    format='%(firmname)s',        
    migrate=migrate)

# sub-customers ("sub-accounts") "CLIENTES"
db.define_table('subcustomer',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('customer', 'reference customer'),  # reference
    Field('firmname', type='string', length=50),
    Field('address', type='string', length=100),
    Field('zipcode', type='string', length=4),
    Field('city', 'reference city'),
    Field('state', 'reference state'),  # reference
    Field('country', 'reference country'), # reference
    Field('fax', type='string', length=20),
    Field('telephone', type='string', length=60),
    Field('tin', type='string', length=20),
    Field('vat', type='integer'),  # reference
    Field('invoice', type='string', length=1),
    Field('currentaccount', type='string', length=1),  # reference?
    Field('pricelist', type='integer'),  # reference
    Field('situation', 'reference situation'),  # reference
    Field('contactgroup', 'reference contactgroup'),  # reference
    Field('observations', type='text'),
    Field('placeofdelivery', type='text'),
    Field('purveyor', 'reference purveyor'),  # reference
    Field('addition', type='datetime'),
    Field('deletion', type='datetime'),
    Field('currentaccountlimit', type='double'),
    Field('checklimit', type='double'),
    Field('jurisdiction', 'reference jurisdiction'), # reference
    Field('sex', type="string", length=1),
    Field('birth', type='date'),
    Field('balance', type='double'),
    Field('replica', type='boolean', default=False),
    format='%(firmname)s',        
    migrate=migrate)

# groups
db.define_table('contactgroup',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',        
    migrate=migrate)

# contacts
db.define_table('contact',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('customer', 'reference customer'),  # reference
    Field('purveyor', 'reference purveyor'),  # reference
    Field('tin'),  # Argentina's CUIT
    Field('department', type='string', length=50),  # reference?
    Field('telephone', type='string', length=100),
    Field('fax', type='string', length=100),
    Field('email', type='string', length=100),
    Field('schedule', type='string', length=100),
    Field('address', type='string', length=50),
    Field('zipcode', type='string', length=50, comment='Zip code'),
    Field('city', 'reference city'),  # reference
    Field('state', 'reference state'),  # reference
    Field('observations', type='text'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',        
    migrate=migrate)
    
# memos messages
db.define_table('memo',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('date', type='date'),
    Field('contact', 'reference contact'),  # reference
    Field('subject', type='string', length=50),
    Field('observations', type='text'),
    Field('user', 'reference auth_user'),  # reference
    Field('replica', type='boolean', default=False),
    format='%(description)s',        
    migrate=migrate)

# status (active, unactive, prospect, etc.)
db.define_table('situation',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',        
    migrate=migrate)

# salesman
db.define_table('salesperson',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('staff', 'reference staff'),
    Field('commission', type='double'),
    Field('telephone', type='string', length=50),
    Field('address', type='string', length=50),
    Field('state', 'reference state'),  # reference
    Field('city', 'reference city'),  # reference
    Field('notes', type='text'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',        
    migrate=migrate)

# many to many referenced user-contact table
db.define_table('contactuser',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('user', 'reference auth_user'),
    Field('contact', 'reference contact'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    )
