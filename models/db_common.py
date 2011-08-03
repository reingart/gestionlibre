# -*- coding: utf-8 -*-

migrate = True

# tables used both in sales, purchases, etc.

# tax category
db.define_table('vat',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('percentage', type='double'),
    Field('aliquot', type='double'),
    Field('category'), # vat type
    Field('abbr', type='string', length=3),
    Field('discriminate', type='boolean', default=False),
    Field('documentsales', 'reference documenttype'),  # reference
    Field('documentpurchases', 'reference documenttype'),  # reference
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

# Al parecer en inglés contable rubro es item, pero es confuso para
# el hispanoparlante, y más confuso si se usa otra palabra como category

# product main category
db.define_table('item',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description', type='string', length=20),
    Field('products', type='boolean', default=False),
    Field('units', type='boolean', default=False), # ¿unidades?
    Field('times', type='boolean', default=False), # ¿tiempos?
    Field('replica', type='boolean', default=False),
    format='%(description)s',    
    migrate=migrate)

# product sub category
db.define_table('subitem',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description', type='string', length=50),
    Field('item', 'reference item'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',    
    migrate=migrate)

# states/province/district
db.define_table('state',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',    
    migrate=migrate)

db.define_table('jurisdiction',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description', type='string', length=50),
    Field('replica', type='boolean', default=False),
    format='%(description)s',    
    migrate=migrate)
    
# country?
db.define_table('country',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',    
    migrate=migrate)

# city?
db.define_table('city',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('city', type='string', length=50),
    Field('replica', type='boolean', default=False),
    format='%(description)s',    
    migrate=migrate)

# Address?
db.define_table('address',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('street', type='string'),
    Field('number', type='string', length=50),
    Field('other', type='string', length=200), # whatever else comes here
    Field('zipcode', type='string', length=9), # Argentina's CPA
    Field('replica', type='boolean', default=False),
    format='%(description)s',    
    migrate=migrate)

# custom serial code table for validation purposes
db.define_table('customserialcode',
    Field('serialcode', unique=True),
    Field('replica', 'boolean', default=True),
    format='%(serialcode)s',
    migrate=migrate)
    