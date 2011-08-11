# -*- coding: utf-8 -*-

migrate = True

# new "Noticia"
db.define_table('payroll_new',
    Field('payroll_new_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('file_id', 'reference file'),  # reference
    Field('concept_id', 'reference concept'),  # reference
    Field('datum', type='double', default=0),
    Field('payroll_id', 'reference payroll'),  # reference
    Field('addition', type='date'),
    Field('deletion', type='date'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

db.define_table('salary',
    Field('salary_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('payroll_id', 'reference payroll'),
    Field('cost_center_id', 'reference cost_center'),  # reference
    Field('staff_category_id', 'reference staff_category'),  # reference
    Field('file_id', 'reference file'), # reference
    Field('concept_id', 'reference concept'), # reference
    Field('liquidation'),  # reference?
    Field('type', type='string', length=1),  # reference?
    Field('half_bonus', type='boolean', default=False),
    Field('quantity', type='double'),
    Field('amount', type='double'),
    Field('starting', type='datetime'),
    Field('ending', type='datetime'),
    Field('fixed', type='boolean', default=False),
    Field('liquidated', type='boolean', default=False),
    Field('format', type='string', length=1),
    Field('text', type='string', length=255),
    Field('agreement_id', 'reference agreement'),  # reference
    Field('department_id', 'reference department'), # reference
    Field('role_id', 'reference role'),
    Field('plant_id', 'reference plant'), # reference
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)
