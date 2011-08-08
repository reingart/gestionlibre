# -*- coding: utf-8 -*-

migrate = True

# cost center
db.define_table('cost_center',
    Field('cost_center_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('addition', type='datetime'),
    Field('deletion', type='datetime'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)
 
# banks "Bancos"
db.define_table('bank',
    Field('bank_id', 'id'),
    Field('code', unique = True),
    Field('description', type='string', length=250),
    Field('bank_check'),  # reference
    Field('concept_id', 'integer'),  # reference
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)
