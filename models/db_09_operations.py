# -*- coding: utf-8 -*-
# Source document items (posting)

migrate = True

# ie.: "traditional" line items
db.define_table('movement',
    Field('movement_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('operation_id', 'reference operation'), # reference
    Field('concept_id', 'reference concept' ), # reference
    Field('price_id', 'reference price'), # ¿tarifaid? # reference
    Field('quantity', type='double', default=0),
    Field('amount', type='decimal(10,2)', default=0),
    Field('discriminated_id', 'reference tax'), # changed (was integer i.e. 21)
    Field('table_number', type='integer', default=0), # reference?
    Field('detail', type='string', length=255),
    Field('value', type='decimal(10,2)', default=0),
    Field('posted', type='date', default=request.now),
    Field('discount', type='decimal(10,2)'),
    Field('surcharge', type='decimal(10,2)'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)
 
