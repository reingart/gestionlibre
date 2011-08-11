# -*- coding: utf-8 -*-

migrate = True

# funds types (available, imprest/fixed/office fund): "Fondos"
db.define_table('fund',
    Field('fund_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('type', type='integer', default=0), # reference?
    Field('upper_limit', type='decimal(10,2)', default=0),
    Field('balance', type='decimal(10,2)', default=0),
    Field('closed', type='boolean', default=False),
    Field('current_account', type='boolean', default=False),
    Field('bank_checks', type='boolean', default=False),
    Field('concept_id', 'reference concept'),  # reference
    Field('account_id', 'reference account'), # reference
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

# payment terms "CondicionesPago"
db.define_table('payment_terms',
    Field('payment_terms_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('canceled', type='boolean', default=False),
    Field('concept_id', 'reference concept'),  # reference
    Field('current_account', type='boolean', default=False),
    Field('days_1', 'integer'),
    Field('days_2', 'integer'),
    Field('days_3', 'integer'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

# payment methods
db.define_table('payment_method',
    Field('payment_method_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('concept_id', 'reference concept'),  # reference
    Field('coupons', 'integer'),

    Field('coefficient_01', type='double'),
    Field('coefficient_02', type='double'),
    Field('coefficient_03', type='double'),
    Field('coefficient_04', type='double'),
    Field('coefficient_05', type='double'),
    Field('coefficient_06', type='double'),
    Field('coefficient_07', type='double'),
    Field('coefficient_08', type='double'),
    Field('coefficient_09', type='double'),
    Field('coefficient_10', type='double'),
    Field('coefficient_11', type='double'),
    Field('coefficient_12', type='double'),
    Field('coefficient_13', type='double'),
    Field('coefficient_14', type='double'),
    Field('coefficient_15', type='double'),
    Field('coefficient_16', type='double'),
    Field('coefficient_17', type='double'),
    Field('coefficient_18', type='double'),
    Field('coefficient_19', type='double'),
    Field('coefficient_20', type='double'),
    Field('coefficient_21', type='double'),
    Field('coefficient_22', type='double'),
    Field('coefficient_23', type='double'),
    Field('coefficient_24', type='double'),

    Field('quota_01', type='integer'),  # reference?
    Field('quota_02', type='integer'),  # reference?
    Field('quota_03', type='integer'),  # reference?
    Field('quota_04', type='integer'),  # reference?
    Field('quota_05', type='integer'),  # reference?
    Field('quota_06', type='integer'),  # reference?
    Field('quota_07', type='integer'),  # reference?
    Field('quota_08', type='integer'),  # reference?
    Field('quota_09', type='integer'),  # reference?
    Field('quota_10', type='integer'),  # reference?
    Field('quota_11', type='integer'),  # reference?
    Field('quota_12', type='integer'),  # reference?
    Field('quota_13', type='integer'),  # reference?
    Field('quota_14', type='integer'),  # reference?
    Field('quota_15', type='integer'),  # reference?
    Field('quota_16', type='integer'),  # reference?
    Field('quota_17', type='integer'),  # reference?
    Field('quota_18', type='integer'),  # reference?
    Field('quota_19', type='integer'),  # reference?
    Field('quota_20', type='integer'),  # reference?
    Field('quota_21', type='integer'),  # reference?
    Field('quota_22', type='integer'),  # reference?
    Field('quota_23', type='integer'),  # reference?
    Field('quota_24', type='integer'),  # reference?

    Field('days_01', type='integer'),
    Field('days_02', type='integer'),
    Field('days_03', type='integer'),
    Field('days_04', type='integer'),
    Field('days_05', type='integer'),
    Field('days_06', type='integer'),
    Field('days_07', type='integer'),
    Field('days_08', type='integer'),
    Field('days_09', type='integer'),
    Field('days_10', type='integer'),
    Field('days_11', type='integer'),
    Field('days_12', type='integer'),
    Field('days_13', type='integer'),
    Field('days_14', type='integer'),
    Field('days_15', type='integer'),
    Field('days_16', type='integer'),
    Field('days_17', type='integer'),
    Field('days_18', type='integer'),
    Field('days_19', type='integer'),
    Field('days_20', type='integer'),
    Field('days_21', type='integer'),
    Field('days_22', type='integer'),
    Field('days_23', type='integer'),
    Field('days_24', type='integer'),

    Field('expenditure_01', type='decimal(10,2)'), # ¿gasto?
    Field('expenditure_02', type='decimal(10,2)'), # ¿gasto?
    Field('expenditure_03', type='decimal(10,2)'), # ¿gasto?
    Field('expenditure_04', type='decimal(10,2)'), # ¿gasto?
    Field('expenditure_05', type='decimal(10,2)'), # ¿gasto?
    Field('expenditure_06', type='decimal(10,2)'), # ¿gasto?
    Field('expenditure_07', type='decimal(10,2)'), # ¿gasto?
    Field('expenditure_08', type='decimal(10,2)'), # ¿gasto?
    Field('expenditure_09', type='decimal(10,2)'), # ¿gasto?
    Field('expenditure_10', type='decimal(10,2)'), # ¿gasto?
    Field('expenditure_11', type='decimal(10,2)'), # ¿gasto?
    Field('expenditure_12', type='decimal(10,2)'), # ¿gasto?
    Field('expenditure_13', type='decimal(10,2)'), # ¿gasto?
    Field('expenditure_14', type='decimal(10,2)'), # ¿gasto?
    Field('expenditure_15', type='decimal(10,2)'), # ¿gasto?
    Field('expenditure_16', type='decimal(10,2)'), # ¿gasto?
    Field('expenditure_17', type='decimal(10,2)'), # ¿gasto?
    Field('expenditure_18', type='decimal(10,2)'), # ¿gasto?
    Field('expenditure_19', type='decimal(10,2)'), # ¿gasto?
    Field('expenditure_20', type='decimal(10,2)'), # ¿gasto?
    Field('expenditure_21', type='decimal(10,2)'), # ¿gasto?
    Field('expenditure_22', type='decimal(10,2)'), # ¿gasto?
    Field('expenditure_23', type='decimal(10,2)'), # ¿gasto?
    Field('expenditure_24', type='decimal(10,2)'), # ¿gasto?

    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

# checkbook
db.define_table('checkbook',
    Field('checkbook_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('account_id', 'reference account'),  # reference
    Field('concept_id', 'reference concept'),  # reference
    Field('starting', type='datetime', default=0),
    Field('ending', type='datetime', default=0),
    Field('next', type='integer', default=0),  # reference?
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)
