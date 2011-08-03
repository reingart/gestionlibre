# -*- coding: utf-8 -*-

migrate = True

# cash management

# funds types (available, imprest/fixed/office fund): "Fondos"
db.define_table('fund',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('type', type='integer', default=0), # reference?
    Field('upperlimit', type='decimal(10,2)', default=0),
    Field('balance', type='decimal(10,2)', default=0),
    Field('closed', type='boolean', default=False),
    Field('currentaccount', type='boolean', default=False),
    Field('bankchecks', type='boolean', default=False),
    Field('concept', 'reference concept'),  # reference
    Field('account', 'reference account'), # reference
    Field('replica', type='boolean', default=False),    
    format='%(description)s',    
    migrate=migrate)

# banks "Bancos"
db.define_table('bank',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('description', type='string', length=250),
    Field('bankcheck', 'reference bankcheck'),  # reference
    Field('concept', 'reference concept'),  # reference
    Field('replica', type='boolean', default=False),
    format='%(description)s',        
    migrate=migrate)

# bank reconciliation "Conciliación"
db.define_table('reconciliation',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('concept', 'reference concept'),  # reference
    Field('date', type='date'),
    Field('amount', type='decimal(10,2)'),
    Field('activity', type='integer'), # ¿movimiento?  # reference
    Field('addition', type='date'),
    Field('deletion', type='date'),
    Field('detail', type='text'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',        
    migrate=migrate)

# cash balance "Cierres"
db.define_table('cashbalance',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('date', type='date'),
    Field('balance', type='decimal(10,2)', default=0),
    Field('canceled', type='boolean', default=False), # ¿anulado?
    Field('balanced', type='boolean', default=False),
    Field('prints', type='integer', default=0),
    Field('transactionrecord1', 'reference transactionrecord'),  # reference
    Field('transactionrecord2', 'reference transactionrecord'),  # reference
    Field('pages', type='integer', default=0),
    Field('cash', type='integer', default=0),
    Field('fund', 'reference fund'),  # reference
    Field('replica', type='boolean', default=False),
    format='%(description)s',        
    migrate=migrate)

# payment terms "CondicionesPago"
db.define_table('paymentterms',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('canceled', type='boolean', default=False),
    Field('concept', 'reference concept'),  # reference
    Field('currentaccount', type='boolean', default=False),
    Field('replica', type='boolean', default=False),
    format='%(description)s',        
    migrate=migrate)

# paymenttermsdays
db.define_table('paymenttermsdays', 
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('paymentterms', 'reference paymentterms'),
    Field('days', 'integer'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',        
    migrate=migrate)

# payment methods
db.define_table('paymentmethod',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('concept', 'reference concept'),  # reference
    Field('coupons', 'integer'),    
    Field('replica', type='boolean', default=False),
    format='%(description)s',        
    migrate=migrate)

# paymentmethodcoefficient
db.define_table('paymentmethodcoefficient',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('paymentmethod', 'reference paymentmethod'),
    Field('coefficient', type='double'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',        
    migrate=migrate)

# paymentmethodquota
db.define_table('paymentmethodquota',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('paymentmethod', 'reference paymentmethod'),
    Field('quota', type='integer'),  # reference?
    Field('replica', type='boolean', default=False),
    format='%(description)s',        
    migrate=migrate)

# paymentmethoddays
db.define_table('paymentmethoddays',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('paymentmethod', 'reference paymentmethod'),
    Field('days', type='integer'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',        
    migrate=migrate)

# paymentmethodexpenditure
db.define_table('paymentmethodexpenditure',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('paymentmethod', 'reference paymentmethod'),
    Field('expenditure', type='decimal(10,2)'), # ¿gasto?
    Field('replica', type='boolean', default=False),
    format='%(description)s',        
    migrate=migrate)

# cost center
db.define_table('costcenter',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('addition', type='datetime'),
    Field('deletion', type='datetime'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',        
    migrate=migrate)

# checkbook
db.define_table('checkbook',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('account', 'reference account'),  # reference
    Field('concept', 'reference concept'),  # reference
    Field('fromdate', type='datetime', default=0),
    Field('todate', type='datetime', default=0),
    Field('next', type='integer', default=0),  # reference?
    Field('replica', type='boolean', default=False),
    format='%(description)s',        
    migrate=migrate)
    
# check
db.define_table('bankcheck',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('customer', 'reference customer'), # reference
    Field('purveyor', 'reference purveyor'), # reference
    Field('number', type='string', length=50),
    Field('bank', 'reference bank'),  # reference
    Field('amount', type='double'),
    Field('addition', type='datetime'),
    Field('duedate', type='datetime'),
    Field('deletion', type='datetime'),
    Field('paid', type='datetime'),
    Field('exchanged', type='boolean', default=False),
    Field('bouncer', type='boolean', default=False),
    Field('transactionrecord', 'reference transactionrecord'),  # reference
    Field('id1', type='integer'),
    Field('exit', type='integer'),
    Field('rejection', type='integer'),
    Field('concept', 'reference concept'),  # reference
    Field('detail', type='string', length=50),
    Field('bd', type='integer'),
    Field('own', type='boolean', default=False),
    Field('balance', type='double'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',        
    migrate=migrate)

# credit card coupons
db.define_table('creditcardcoupon',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('concept', 'reference concept'),  # reference
    Field('number', type='string', length=20),
    Field('lot', type='string', length=20),
    Field('fees', type='integer'),
    Field('amount', type='double'),
    Field('addition', type='date'),
    Field('deletion', type='date'),
    Field('duedate', type='date'),
    Field('presentation', type='date'),
    Field('payment', type='date'),
    Field('activity', 'reference activity'), # ¿movimiento?  # reference
    Field('replica', type='boolean', default=False),
    format='%(description)s',        
    migrate=migrate)
