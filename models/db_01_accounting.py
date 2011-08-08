# -*- coding: utf-8 -*-

migrate = True

# Account (higher level of Chart of Accounts) "Cuentas"
db.define_table('account',
    Field('account_id', 'id'),
    Field('code', unique = True),
    Field('description', type='string', length=50),
    Field('receives', type='boolean', default=False),
    Field('customer_group_id', 'reference customer_group'), # reference
    Field('bank_id', 'reference bank'), # reference
    Field('tax', type='boolean', default=False),
    Field('gross_receipts', type='boolean', default=False), # ¿iibb?
    Field('collections', type='boolean', default=False), # ¿percepciones?
    Field('retentions', type='boolean', default=False),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

# Journal entry "Asientos"
db.define_table('journal_entry',
    Field('journal_entry_id', 'id'),
    Field('code', unique = True),
    Field('description', type='string', length=50, comment='Description'),
    Field('number', type='integer', default=0),
    Field('posted', type='datetime'),
    Field('source'),
    Field('valuation', type='datetime'),
    Field('type', type='string', length=1), # reference?
    Field('draft', type='boolean', default=False),
    Field('accounting_period_id', 'reference accounting_period'), # reference
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)
 
