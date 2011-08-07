# -*- coding: utf-8 -*-

migrate = True

# Fees, installments, quotes

db.define_table('fee',
    Field('fee_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('due_date', type='date'),
    Field('number', type='integer', default=0),
    Field('month', type='integer', default=0),
    Field('year', type='integer', default=0),
    Field('additions', type='boolean', default=False),
    Field('document_id', 'reference document'), # reference
    Field('extras', type='boolean', default=False),
    Field('ticket', type='boolean', default=False),
    Field('separate', type='boolean', default=False),
    Field('starting', type='date'),
    Field('ending', type='date'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

db.define_table('installment',
    Field('installment_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('customer_id', 'reference customer'), # reference
    Field('supplier_id', 'reference supplier', comment='Wich supplier to pay to'), # reference
    Field('subcustomer_id', 'reference subcustomer'), # reference
    Field('fee_id', 'reference fee'), # reference
    Field('net', type='double', comment='Net amount'),
    Field('discount', type='double'),
    Field('paid', type='double'),
    Field('fees', type='integer', default=0, comment='number of fees'),
    Field('interests', type='double', default=0, comment='Transferred interests'),
    Field('late_payment', type='double', default=0, comment='Late payment fees'),
    Field('monthly_amount', type='double'),
    Field('paid_fees', type='integer', default=0),
    Field('starting_fee_id', 'reference fee', comment='fee_id'),
    Field('ending_fee_id', 'reference fee', default=0, comment='fee_id'),
    Field('starting', type='datetime'),
    Field('first_due', type='datetime', comment='x days of month'),
    Field('second_due', type='datetime', comment='y days of month'),
    Field('observations', type='string', length=50),
    Field('canceled', type='boolean', default=False),
    Field('collected', type='double'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

db.define_table('quota',
    Field('quota_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('fee_id', 'reference fee'), # reference
    Field('amount', type='double'),
    Field('surcharge', type='double'),
    Field('discount', type='double'),
    Field('paid', type='double'),
    Field('due_date', type='datetime'),
    Field('entry', type='integer', default=0), # reference?
    Field('exit', type='integer', default=0), # reference?
    Field('canceled', type='boolean', default=False),
    Field('collected', type='double'),
    Field('extra', type='boolean', default=False),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)
