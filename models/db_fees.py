# -*- coding: utf-8 -*-

migrate = True

# Fees, installments, quotes

db.define_table('fee',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('duedate', type='date'),
    Field('number', type='integer', default=0),
    Field('month', type='integer', default=0),
    Field('year', type='integer', default=0),
    Field('additions', type='boolean', default=False),
    Field('documenttype', 'reference documenttype'), # reference
    Field('extras', type='boolean', default=False),
    Field('ticket', type='boolean', default=False),
    Field('separate', type='boolean', default=False),
    Field('fromdate', type='date'),
    Field('todate', type='date'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',        
    migrate=migrate)
    
db.define_table('installment',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('customer', 'reference customer'), # reference
    Field('purveyor', 'reference purveyor', comment='Wich purveyor to pay to'), # reference
    Field('subcustomer', 'reference subcustomer'), # reference
    Field('fee', 'reference fee'), # reference
    Field('net', type='double', comment='Net amount'),
    Field('discount', type='double'),
    Field('paid', type='double'),
    Field('fees', type='integer', default=0, comment='number of fees'),
    Field('interests', type='double', default=0, comment='Transferred interests'),
    Field('latepayment', type='double', default=0, comment='Late payment fees'),
    Field('monthlyamount', type='double'),
    Field('paidfees', type='integer', default=0),
    Field('fromdate', type='integer', default=0, comment='feeid'),
    Field('todate', type='integer', default=0, comment='feeid'),
    Field('start', type='datetime'),
    Field('firstdue', type='datetime', comment='x days of month'),
    Field('seconddue', type='datetime', comment='y days of month'),
    Field('observations', type='string', length=50),
    Field('canceled', type='boolean', default=False),
    Field('collected', type='double'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',        
    migrate=migrate)
    
db.define_table('quota',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('fee', 'reference fee'), # reference
    Field('amount', type='double'),
    Field('surcharge', type='double'),
    Field('discount', type='double'),
    Field('paid', type='double'),
    Field('duedate', type='datetime'),
    Field('entry', type='integer', default=0), # reference?
    Field('exit', type='integer', default=0), # reference?
    Field('canceled', type='boolean', default=False),
    Field('replica', type='boolean', default=False),
    Field('collected', type='double'),
    Field('extra', type='boolean', default=False),
    Field('replica', type='boolean', default=False),
    format='%(description)s',        
    migrate=migrate)
