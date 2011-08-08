# -*- coding: utf-8 -*-

migrate = True

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

db.define_table('healthcare',
    Field('healthcare_id', 'id'),
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

db.define_table('agreement',
    Field('agreement_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('text', type='text'),
    Field('amount', type='double'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)
