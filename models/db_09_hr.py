# -*- coding: utf-8 -*-

migrate = True

# column
db.define_table('payroll_column',
    Field('payroll_column_id', 'id'),
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
