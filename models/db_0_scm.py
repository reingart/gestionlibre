## -*- coding: utf-8 -*-

migrate = True

# Supply Chain Management

# suppliers/providers:
db.define_table('supplier',
    Field('supplier_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('legal_name', type='string', length=50),
    Field('tax_id', 'reference tax', default=0), # Argentina's IVA # reference
    Field('tax_identification', type='string', length=20), # Argentina's CUIT
    Field('address', type='string', length=30),
    Field('zip_code', type='string', length=50),
    Field('city_id', 'reference city'), # reference
    Field('state_id', 'reference state'),  # reference
    Field('telephone', type='string', length=20),
    Field('fax', type='string', length=50),
    Field('situation_id', 'reference situation'),  # reference
    Field('id_number', type='string', length=20), # ¿Argentina's DNI?
    Field('observations', type='text'),
    Field('identity_card', type='string', length=20),
    Field('birth', type='datetime'),
    Field('nationality_id', 'reference country'),  # reference country
    Field('jurisdiction_id', 'reference jurisdiction'),  # reference
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

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

# product structure (bill of materials)
db.define_table('product_structure',
    Field('product_structure_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('concept_id', 'reference concept'),
    Field('quantity', type='double', default=0),
    Field('scrap', type='double', default=0),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

# product families/lines grouping
db.define_table('family',
    Field('family_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('collection_id', 'reference collection'), # reference
    Field('amount', type='decimal(10,2)', default=0),
    Field('entry', type='boolean', default=False),
    Field('exit', type='boolean', default=False),
    Field('category_id', 'reference category'),  # reference
    Field('subcategory_id', 'reference subcategory'),  # reference
    Field('supplier_id', 'reference supplier'),  # reference
    Field('suspended', type='boolean', default=False),
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

# products inventory (in/out)
db.define_table('stock',
    Field('stock_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('concept_id', 'reference concept'),  # reference
    Field('posted', type='date', comment='Date of entry'),
    Field('reserved', type='boolean', default=False),
    Field('warehouse_id', 'reference warehouse'),  # reference
    Field('accumulated', type='boolean', default=False),
    Field('value', type='double', default=0),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)
