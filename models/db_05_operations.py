# -*- coding: utf-8 -*-
# Account reference/detail (lowest level of the Chart of Accounts)
# ie: products/services, payments, income, expenses, etc.

migrate = True

db.define_table('concept',
    Field('concept_id', 'id'),
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('category_id', 'reference category'), # reference
    Field('subcategory_id', 'reference subcategory'), # reference
    Field('family_id', 'reference family'), # reference
    Field('color_id', 'reference color'),# reference
    Field('size_id', 'reference size'), # reference
    Field('quantity', type='integer', default=0),
    Field('amount', type='double', default=0),
    Field('addition', type='date'),
    Field('deletion', type='date'),
    Field('tax_id', 'reference tax'), # reference
    Field('supplier_id', 'integer'), # reference
    Field('customer_id', 'integer'), # reference
    Field('account_id', 'reference account'),# reference
    Field('measure', type='string', length=1),
    Field('desired', type='double', default=0), # ¿deseado?
    Field('presentation', type='string', length=100),
    Field('entry', type='boolean', default=False),
    Field('exit', type='boolean', default=False),
    Field('taxed', type='boolean', default=False), #  ¿gravado?
    Field('stock', type='boolean', default=False),
    Field('unitary', type='boolean', default=False),
    Field('internal', type='boolean', default=False),
    Field('payment_method', type='boolean', default=False),
    Field('tax', type='boolean', default=False),
    Field('current_account', type='boolean', default=False),
    Field('cash_box', type='boolean', default=False),
    Field('extra', type='boolean', default=False),
    Field('cash', type='boolean', default=False),
    Field('banks', type='boolean', default=False),
    Field('receipt', type='string', length=50),
    Field('statement', type='string', length=50), # ¿resumen?
    Field('abbr', type='string', length=50),
    Field('stock_quantity', type='double'),
    Field('collection_id', 'reference collection'), # reference
    Field('floor', type='double'), # ¿mínimo?
    Field('suspended', type='boolean', default=False),
    Field('discounts', type='boolean', default=False),
    Field('surcharges', type='boolean', default=False),
    Field('replica', type='boolean', default=False),
    Field('orderable', 'boolean', default=False), # can be ordered/bought, do not use, filter concepts by internal property
    format='%(description)s',
    migrate=migrate)
