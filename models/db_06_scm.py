# -*- coding: utf-8 -*-

migrate = True

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
 
