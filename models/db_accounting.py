# -*- coding: utf-8 -*-
migrate = True

# Account (higher level of Chart of Accounts) "Cuentas"
db.define_table('account',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description', type='string', length=50),
    Field('receives', type='boolean', default=False),
    Field('contactgroup', 'reference contactgroup'), # reference
    Field('bank', 'reference bank'), # reference
    Field('vat', type='boolean', default=False),
    Field('grossreceipts', type='boolean', default=False), # ¿iibb?
    Field('collections', type='boolean', default=False), # ¿percepciones?
    Field('retentions', type='boolean', default=False),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)
    
# Accounting period, fiscal year (FY) "Ejercicios"
db.define_table('accountingperiod',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description', type='string', length=50),
    Field('fromdate', type='date'),
    Field('todate', type='date'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',    
    migrate=migrate)
    
# Journal entry "Asientos"
db.define_table('journalentry',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description', type='string', length=50, comment='Description'),
    Field('number', type='integer', default=0),    
    Field('date', type='datetime'),
    Field('source'),
    Field('valuation', type='datetime'),
    Field('type', type='string', length=1), # reference?
    Field('draft', type='boolean', default=False),
    Field('accountingperiod', 'reference accountingperiod'), # reference
    Field('replica', type='boolean', default=False),
    format='%(description)s',    
    migrate=migrate)
    
# entry item (posting) "Partidas"
db.define_table('accountingentry',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description', type='string', length=50),
    Field('journalentry', 'reference journalentry'), # reference
    Field('account', 'reference account'), # reference
    Field('type', type='string', length=1), # reference?
    Field('amount', type='double'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',    
    migrate=migrate)
