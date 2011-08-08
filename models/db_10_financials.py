# -*- coding: utf-8 -*-

migrate = True

# bank reconciliation "Conciliación"
db.define_table('reconciliation',
    Field('reconciliation_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('concept_id', 'reference concept'),  # reference
    Field('posted', type='date'),
    Field('amount', type='decimal(10,2)'),
    Field('movement_id', 'reference movement'), # ¿movimiento?  # reference
    Field('addition', type='date'),
    Field('deletion', type='date'),
    Field('detail', type='text'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)


# credit card coupons
db.define_table('credit_card_coupon',
    Field('credit_card_coupon_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('concept_id', 'reference concept'),  # reference
    Field('number', type='string', length=20),
    Field('lot', type='string', length=20),
    Field('fees', type='integer'),
    Field('amount', type='double'),
    Field('addition', type='date'),
    Field('deletion', type='date'),
    Field('due_date', type='date'),
    Field('presentation', type='date'),
    Field('payment', type='date'),
    Field('movement_id', 'reference movement'), # ¿movimiento?  # reference
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)
 
