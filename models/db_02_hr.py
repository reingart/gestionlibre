# -*- coding: utf-8 -*-
migrate = True

db.define_table('file',
    Field('file_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('staff_id', 'reference staff'),  # reference
    Field('extra_hours', type='double'),
    Field('presenteesm', type='double', comment='Presenteesm amount'), # ¿presentismo?
    Field('goberment_increase', type='double', comment='salary extra by statal dispositions (divided by months)'),
    Field('sick_days', type='integer', default=0, comment='Number of sick days'),
    Field('presenteesm_discount', type='double'),
    Field('failure', type='double', comment='Failure discount'),
    Field('contribution_discount', type='double'),
    Field('seniority', type='double'),
    Field('per_diem', type='double', comment='Per diem amount'),
    Field('profit_percentage', type='double'),
    Field('schooling', type='integer', default=0, comment='Schooling help: number of children'),
    Field('allowance', type='integer', default=0, comment='Number of children for annual allowance'),
    Field('paid_vacation', type='double'),
    Field('half_bonus', type='double', comment='Importe del Medio Aguinaldo'),
    Field('prenatal', type='integer', default=0),
    Field('staff_category_id', 'reference staff_category'),  # reference
    Field('healthcare_id', 'reference healthcare'),  # reference
    Field('labor_union_id', 'reference labor_union'),  # reference
    Field('pension_id', 'reference pension', default=0, comment='(pension id)'),  # reference
    Field('cost_center_id', 'reference cost_center'),  # reference
    Field('entry', type='datetime'),
    Field('exit', type='datetime'),
    Field('salary', type='double', comment='Base salary (monthly)'),
    Field('seniority_years', type='integer'),
    Field('spouse', type='boolean', default=False),
    Field('seniority_months', type='integer'),
    Field('large_family', type='boolean', default=False),
    Field('department_id', 'reference department'),  # reference
    Field('role_id', 'reference role'),  # reference
    Field('plant_id', 'reference plant'),  # reference
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)
 
db.define_table('relative',
    Field('relative_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('name', type='string', length=100),
    Field('staff_id', 'reference staff'),  # reference
    Field('kinship', type='string', length=1),
    Field('tax_identification', type='string', length=13),
    Field('allowance', type='boolean', default=False),
    Field('disabled', type='boolean', default=False),
    Field('schooling', type='boolean', default=False),
    Field('nationality_id', 'reference country'),  # reference country
    Field('birth', type='datetime', comment='Fec.Nac.'),
    Field('marital_status', type='string', length=1, comment='marital status'),
    Field('address', type='string', length=25),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)
