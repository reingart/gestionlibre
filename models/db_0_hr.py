# -*- coding: utf-8 -*-

migrate = True

# Human Resources management

db.define_table('staff',
    Field('staff_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('name', type='string', length=40),
    Field('addres', type='string', length=40),
    Field('city_id', 'reference city'), # reference
    Field('zip_code', type='string', length=4),
    Field('state_id', 'reference state'),  # reference
    Field('telephone', type='string', length=12),
    Field('birth', type='datetime'),
    Field('id_number', type='string', length=15), # (Argentina's DNI)
    Field('nationality_id', 'reference country'), # reference country
    Field('tax_identification', type='string', length=13), # ¿cuil? (note: taxid != CUIT)
    Field('sex', type='string', length=1),
    Field('marital_status', type='string', length=1),
    Field('addition', type='datetime'),
    Field('deletion', type='datetime'),
    Field('replica', type='boolean', default=False),
    format='%(name)s',
    migrate=migrate)

db.define_table('plant',
    Field('plant_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

db.define_table('department',
    Field('department_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

db.define_table('labor_union',
    Field('labor_union_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('percentage', type='integer', default=0, comment='Personal percentage for the union'),
    Field('patronal', type='integer', default=0, comment='Employer percentage for the union'),
    Field('voluntary', type='integer', default=0, comment='Voluntary contribution'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

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
    Field('health_care_id', 'reference health_care'),  # reference
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
    Field('code', type='string', length=20),
    Field('department_id', 'reference department'),  # reference
    Field('role_id', 'reference role'),  # reference
    Field('plant_id', 'reference plant'),  # reference
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

db.define_table('payroll',
    Field('payroll_id', 'id'),
    Field('code', unique = True),
    Field('description', comment='Type and period'),
    Field('type', type='string', length=1),  # reference?
    Field('half_bonus', type='boolean', default=False),
    Field('vacations', type='boolean', default=False),
    Field('starting', type='datetime'),
    Field('ending', type='datetime'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

# new "Noticia"
db.define_table('payroll_new',
    Field('new_id', 'id'),
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

db.define_table('healt_hcare',
    Field('health_care_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('percentage', type='integer', default=0, comment='Contribution percentage'),
    Field('patronal', type='integer', default=0, comment='Patronal contribution'),
    Field('voluntary', type='integer', default=0, comment='Voluntary contribution'),
    Field('adherent', type='integer', default=0, comment='Aporte por Adherente'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

db.define_table('pension',
    Field('pension_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('percentage', type='double', comment='Personal contribution'),
    Field('contribution', type='integer', default=0, comment='Employer contribution'),
    Field('social_services', type='integer', default=0), # Argentina: law number 19032
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

db.define_table('role',
    Field('role_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

db.define_table('staff_category',
    Field('staff_category_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('salary', type='double'),
    Field('hourly', type='double'),
    Field('type', type='string', length=1),  # reference?
    Field('journalized', type='boolean', default=False),
    Field('addition', type='datetime'),
    Field('deletion', type='datetime'),
    Field('agreement_id', 'reference agreement'),  # reference
    Field('plant_id', 'reference plant'),  # reference
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

# column
db.define_table('column',
    Field('column_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('abbr', type='string', length=50),
    Field('order_number', type='integer', default=0), # order
    Field('receipt', type='boolean', default=False),
    Field('remunerative', type='boolean', default=False),
    Field('operation_id', 'reference operation'), # ¿operación?  # reference
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

db.define_table('formula',
    Field('formula_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('name', type='string', length=50),
    Field('quantity', type='text'),
    Field('amount', type='double'),
    Field('datum', type='double'),
    Field('format', type='string', length=1),  # reference?
    Field('text', type='text'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)


db.define_table('salary',
    Field('salary_id', 'id'),
    Field('code', unique = True),
    Field('description'),
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

db.define_table('agreement',
    Field('agreement_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('text', type='text'),
    Field('amount', type='double'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)
