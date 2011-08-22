# -*- coding: utf-8 -*-
migrate = True

# tables used both in sales, purchases, etc.

# product main category
db.define_table('category',
    Field('category_id', 'id'),
    Field('code', unique = True),
    Field('description', type='string', length=20),
    Field('products', type='boolean', default=False),
    Field('units', type='boolean', default=False), # ¿unidades?
    Field('times', type='boolean', default=False), # ¿tiempos?
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

# product sub category
db.define_table('subcategory',
    Field('subcategory_id', 'id'),
    Field('code', unique = True),
    Field('description', type='string', length=50),
    Field('category_id', 'reference category'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

db.define_table('jurisdiction',
    Field('jurisdiction_id', 'id'),
    Field('code', unique = True),
    Field('description', type='string', length=50),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

# country?
db.define_table('country',
    Field('country_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

# states/province/district
db.define_table('state',
    Field('state_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('country_id', 'reference country'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

# city?
db.define_table('city',
    Field('city_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('city', type='string', length=50),
    Field('state_id', 'reference state'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

# Address?
db.define_table('address',
    Field('address_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('street', type='string'),
    Field('number', type='string', length=50),
    Field('other', type='string', length=200), # whatever else comes here
    Field('zip_code', type='string', length=9), # Argentina's CPA
    Field('city_id', 'reference city'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

# tax category
db.define_table('tax',
    Field('tax_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('tax', 'boolean'), # Argentina's CUIT (yes/no)
    Field('percentage', type='double'),
    Field('aliquot', type='double'),
    Field('category'), # vat type
    Field('abbr', type='string', length=3),
    Field('discriminate', type='boolean', default=False),
    Field('document_sales_id', 'integer'),  # reference
    Field('document_purchases_id', 'integer'),  # reference
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)


# custom serial code table for validation purposes
db.define_table('custom_serial_code',
    Field('custom_serial_code_id', 'id'),
    Field('code', unique=True),
    Field('replica', 'boolean', default=True),
    format='%(code)s',
    migrate=migrate)

# debugging entries
db.define_table('debugging',
    Field('debugging_id', 'id'),
    Field('msg', 'text'),
    format='%(msg)s',
    migrate=migrate)

# gestionlibre options
db.define_table('option',
    Field('option_id', 'id'),
    Field('name', unique=True, requires=IS_NOT_EMPTY()), # "option_1"
    Field('description'),
    Field('type', requires=IS_NOT_EMPTY(), default = 'string'), # a valid dal field type
    Field('represent'),
    Field('requires'),
    Field('value', 'text'),
    format='%(name)s',
    migrate=migrate)
