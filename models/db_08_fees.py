# -*- coding: utf-8 -*-
migrate = True

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
    Field('quotas', type='integer', default=0, comment='number of quotas'),
    Field('interests', type='double', default=0, comment='Transferred interests'),
    Field('late_payment', type='double', default=0, comment='Late payment fees'),
    Field('monthly_amount', type='double'),
    Field('paid_quotas', type='integer', default=0),
    Field('starting_quota_id', 'integer', comment='quota_id'), # reference
    Field('ending_quota_id', 'integer', default=0, comment='quota_id'), # reference
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
    Field('installment_id', 'reference installment'),
    Field('number', 'integer'), # TODO: computed field: index number in quotas ordered set +1 (order by id)
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
