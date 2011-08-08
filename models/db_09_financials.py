# -*- coding: utf-8 -*-

migrate = True

# check
db.define_table('bank_check',
    Field('bank_check_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('customer_id', 'reference customer'), # reference
    Field('supplier_id', 'reference supplier'), # reference
    Field('number', type='string', length=50),
    Field('bank_id', 'reference bank'),  # reference
    Field('amount', type='double'),
    Field('addition', type='datetime'),
    Field('due_date', type='datetime'),
    Field('deletion', type='datetime'),
    Field('paid', type='datetime'),
    Field('exchanged', type='boolean', default=False),
    Field('bouncer', type='boolean', default=False),
    Field('operation_id', 'reference operation'),  # reference
    Field('id_1', type='integer'),
    Field('exit', type='integer'),
    Field('rejection', type='integer'),
    Field('concept_id', 'reference concept'),  # reference
    Field('detail', type='string', length=50),
    Field('bd', type='integer'),
    Field('own', type='boolean', default=False),
    Field('balance', type='double'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

# cash balance "Cierres"
db.define_table('cash_balance',
    Field('cash_balance_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('posted', type='date'),
    Field('balance', type='decimal(10,2)', default=0),
    Field('canceled', type='boolean', default=False), # ¿anulado?
    Field('balanced', type='boolean', default=False),
    Field('prints', type='integer', default=0),
    Field('operation_1_id', 'reference operation'),  # reference
    Field('operation_2_id', 'reference operation'),  # reference
    Field('pages', type='integer', default=0),
    Field('cash', type='integer', default=0),
    Field('fund_id', 'reference fund'),  # reference
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)
