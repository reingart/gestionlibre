# -*- coding: utf-8 -*-
migrate = True

# Accounting period, fiscal year (FY) "Ejercicios"
db.define_table('accounting_period',
    Field('accounting_period_id', 'id'),
    Field('code', unique = True),
    Field('description', type='string', length=50),
    Field('starting', type='date'),
    Field('ending', type='date'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)
