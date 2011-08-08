# -*- coding: utf-8 -*-
migrate = True

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
 
