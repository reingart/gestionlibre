# -*- coding: utf-8 -*-

migrate = True

# Supply Chain Management

# suppliers/providers:
db.define_table('purveyor',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('firmname', type='string', length=50),
    Field('vat', type='integer', default=0), # Argentina's IVA # reference
    Field('tin', type='string', length=20), # Argentina's CUIT
    Field('address', type='string', length=30),
    Field('zipcode', type='string', length=50),
    Field('city', 'reference city'), # reference
    Field('state', 'reference state'),  # reference
    Field('telephone', type='string', length=20),
    Field('fax', type='string', length=50),
    Field('situation', 'reference situation'),  # reference
    Field('ssn', type='string', length=20), # ¿Argentina's DNI?
    Field('observations', type='text'),
    Field('itin', type='string', length=20), # ¿idividual ... Argentina's CUIL?
    Field('identitycard', type='string', length=20),
    Field('birth', type='datetime'),
    Field('nationality', 'reference country'),  # reference country
    Field('jurisdiction', 'reference jurisdiction'),  # reference
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)
    
# collections "Colecciones"
db.define_table('collection',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('fromdate', type='date'),
    Field('todate', type='date'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

# colours (products 1st variant) 
db.define_table('color',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

# sizes (products 2nd variant ) ie. clothes...
db.define_table('size',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('type'),
    Field('ordernumber'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)
    
# warehouses
db.define_table('warehouse',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('address', type='string', length=50),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)
    
# product structure (bill of materials)
db.define_table('productstructure',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('concept', type='integer'),
    Field('product', 'reference product'),
    Field('quantity', type='double', default=0),
    Field('scrap', type='double', default=0),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

# product families/lines grouping
db.define_table('family',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('collection', 'reference collection'), # reference
    Field('amount', type='decimal(10,2)', default=0),
    Field('entry', type='boolean', default=False),
    Field('exit', type='boolean', default=False),
    Field('item', 'reference item'),  # reference
    Field('subitem', 'reference subitem'),  # reference
    Field('purveyor', 'reference purveyor'),  # reference
    Field('suspended', type='boolean', default=False),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

# rates / fare / tariff
db.define_table('rate',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('type', type='string', length=1),  # reference?
    Field('capacity', type='double'),
    Field('measure', type='string', length=1),
    Field('stock', type='integer', default=0),
    Field('indexvalue', type='double', default=0),
    Field('price', type='double', default=0),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

# products inventory (in/out)
db.define_table('stock',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('concept', 'reference concept'),  # reference
    Field('date', type='date', comment='Date of entry'),
    Field('reserved', type='boolean', default=False),
    Field('warehouse', 'reference warehouse'),  # reference
    Field('accumulated', type='boolean', default=False),
    Field('value', type='double', default=0),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

# "Producto". An extension for concept (products can be exposed to customers)
# TODO: clean redundant fields
db.define_table('product',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('unit'),
    Field('size', 'reference size'),
    Field('rate', 'reference rate'),  # reference
    Field('concept', 'reference concept'),  # reference
    Field('text'),
    Field('replica', 'boolean', default=False),
    format='%(description)s',
    migrate=migrate)

# "Pedido"
db.define_table('customerorder',
    Field('code', unique=True, default=new_custom_serial_code),
    Field('description'),
    Field('date', 'date', default=request.now),
    Field('customer', 'reference customer'),
    Field('subcustomer', 'reference subcustomer'),
    Field('salesperson', 'reference salesperson'),
    Field('accepted', 'boolean', default=False),
    Field('user', 'reference auth_user', default=auth.user_id, readable=True, writable=False),
    Field('status', requires=IS_IN_SET({'Canceled':-1, "Pending":0, "Processing":1, "Stopped":2, "Ready":3, "Transport":4, "Delivered":5}), default=0),
    format='%(description)s',
    migrate=migrate)
    
#  "Ítem de pedido"  
db.define_table('customerorderelement',
    Field('code', unique=True, default=new_custom_serial_code),
    Field('description'),
    Field('customerorder', 'reference customerorder'),
    Field('product', 'reference product'),
    Field('accepted', 'boolean', default=True),
    Field('notes', 'text'),
    Field('quantity', 'double', default=0.0),
    format='%(description)s',
    migrate=migrate)
