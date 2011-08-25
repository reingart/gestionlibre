# -*- coding: utf-8 -*-

migrate = True

def operation_format(r):
    try:
        of = "%s %s" % (db.document[r.document_id].description, r.operation_id)
    except (AttributeError, KeyError, ValueError, TypeError):
        of = "Format error: operation %s" % r.operation_id
    return of

# Source Document (transactions records)
db.define_table('operation',
    Field('operation_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('customer_id', 'reference customer'), # reference
    Field('supplier_id', 'reference supplier'), # reference
    Field('detail', type='string', length=60, comment='Observations'),
    Field('payment_terms_id', 'reference payment_terms', comment='Terms of payment'), # reference
    Field('term', type='string', length=50),
    Field('amount', type='double'),
    Field('balance', type='double'),
    Field('posted', type='datetime', default = request.now),
    Field('issue', type='datetime'),
    Field('document_id', 'reference document', comment='Points to order / invoice / packingslips'), # reference
    Field('branch'),
    Field('number', type='integer', default=0),
    Field('due_date', type='datetime'),
    Field('type', type='string', length=1, requires=IS_IN_SET({'T': 'Stock','S': 'Sales','P': 'Purchases'})), # reference? types: T: Stock, S: Sales, P: Purchases
    Field('canceled', type='boolean', default=False, comment='False if deferred payment (df), True if paid with cash, ch (check) or current account'),
    Field('processed', type='boolean', default=False),
    Field('voided', type='boolean', default=False), # ¿anulado?
    Field('fund_id', 'reference fund'), # reference
    Field('cost_center_id', 'reference cost_center'), # reference
    Field('module', type='integer', default=0, comment='Referenced table'), # reference?
    Field('observations', type='string', length=50),
    Field('cancellation', type='boolean', default=False),
    Field('avoidance', type='boolean', default=False), # ¿anulación?
    Field('file_id', 'reference file'), # ¿legajo? # reference
    Field('payroll_id', 'reference payroll'), # reference
    Field('user_id', 'reference auth_user'), # reference
    Field('hour', type='datetime'),
    Field('replicated', type='datetime'),
    Field('subcustomer_id', 'reference subcustomer'), # reference
    Field('salesperson_id', 'reference salesperson'), # reference
    Field('printed', type='boolean', default=False),
    Field('jurisdiction_id', 'reference jurisdiction'), # reference
    Field('replica', type='boolean', default=False),
    format=operation_format,
    migrate=migrate)

def price_format(price):
    try:
        r = "%s - %s" % (price.concept_id.description, price.price_list_id.description)
    except (ValueError, KeyError, AttributeError, IndexError, RuntimeError):
        r = "Format error. price index " + str(price.price_id)
    return r

# price "engine":
db.define_table('price',
    Field('price_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('concept_id', 'reference concept'), # reference
    Field('category_id', 'reference category'), # reference
    Field('salesperson_id', 'reference salesperson'), # reference
    Field('customer_id', 'reference customer'), # reference
    Field('supplier_id', 'reference supplier'), # reference
    Field('customer_group_id', 'reference customer_group'), # reference
    Field('situation_id', 'reference situation'), # reference
    Field('fund_id', 'reference fund'), # reference
    Field('rate_id', 'reference rate', comment='Container type'), # ¿tarifaid? # reference
    Field('payment_method_id', 'reference payment_method', comment='Method of payment'), # reference
    Field('document_id', 'reference document', comment='Document type'), # reference
    Field('price_list_id', 'reference price_list'), # reference
    Field('taxed', type='boolean', default=False),
    Field('tax_id', 'reference tax'), # reference
    Field('type', type='string', length=1), # reference?
    Field('value', type='double', default=0, comment='Insert a value to calculate'),
    Field('calculate', type='string', length=1),
    Field('operation'), # reference?
    Field('source', type='string', length=1, comment='Field on wich operations will be performed'),
    Field('condition', type='string', length=2),
    Field('quantity_1', type='double'),
    Field('quantity_2', type='double'),
    Field('discriminate', type='boolean', default=False),
    Field('priority', type='integer'),
    Field('formula', type='text'),
    Field('replica', type='boolean', default=False),
    format=price_format,
    migrate=migrate)
