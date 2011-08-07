# -*- coding: utf-8 -*-

migrate = True

# Source Document types/categories (grouping ledgers)
# ie.: Invoice, Receipt, Purchase Order, pay stub, voucher, proof., etc. "Comprobantes"
db.define_table('document',
    Field('document_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('point_of_sale_id','reference point_of_sale'), # reference
    Field('abbr', type='string', length=3),
    Field('type', type='string', length=1), # reference?
    Field('tax', type='boolean', default=False), # ¿gravar?
    Field('discriminate', type='boolean', default=False),
    Field('branch'), # ¿sucursal?
    Field('number', type='integer', default=0),
    Field('entry', type='boolean', default=False),
    Field('exit', type='boolean', default=False),
    Field('fiscal', type='boolean', default=False),
    Field('stock', type='boolean', default=False),
    Field('current_account', type='boolean', default=False),
    Field('cash', type='boolean', default=False), # ¿al contado?
    Field('debit', type='boolean', default=False),
    Field('credit', type='boolean', default=False),
    Field('invoices', type='boolean', default=False),
    Field('receipts', type='boolean', default=False),
    Field('packing_slips', type='boolean', default=False), # ¿Remitos?
    Field('orders', type='boolean', default=False), # ¿Pedidos?
    Field('budget', type='boolean', default=False), # ¿Presupuesto?
    Field('countable', type='boolean', default=False),
    Field('printer', type='string', length=50), # reference?
    Field('lines', type='integer', default=0),
    Field('fund_id', 'reference fund'), # reference
    Field('replicate', type='boolean', default=False),
    Field('notes', type='text'),
    Field('observations', type='text'),
    Field('descriptions', type='text'),
    Field('cash_box', type='boolean', default=False), # ¿caja?
    Field('books', type='boolean', default=False), # ¿reservas?
    Field('form', 'string'), # reference?
    Field('down_payment', type='boolean', default=False),
    Field('copies', type='integer'),
    Field('confirm_printing', type='boolean', default=False),
    Field('internal', type='boolean', default=False),
    Field('invert', type='boolean', default=False),
    Field('continuous', type='boolean', default=False),
    Field('multiple_pages', type='boolean', default=False),
    Field('preprinted', type='boolean', default=False),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

# Account reference/detail (lowest level of the Chart of Accounts)
# ie: products/services, payments, income, expenses, etc.
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
    Field('supplier_id', 'reference supplier'), # reference
    Field('customer_id', 'reference customer'), # reference
    Field('account_id', 'reference account'),# reference
    Field('measure', type='string', length=1),
    Field('desired', type='double', default=0), # ¿deseado?
    Field('presentation', type='string', length=100),
    Field('description', type='text'),
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
    format='%(description)s',
    migrate=migrate)

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
    Field('type', type='string', length=1), # reference?
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
    Field('liquidation'), # reference
    Field('user_id', 'reference auth_user'), # reference
    Field('hour', type='datetime'),
    Field('replicated', type='datetime'),
    Field('subcustomer_id', 'reference subcustomer'), # reference
    Field('salesperson_id', 'reference salesperson'), # reference
    Field('printed', type='boolean', default=False),
    Field('jurisdiction_id', 'reference jurisdiction'), # reference
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

# Source document items (posting)
# ie.: "traditional" line items
db.define_table('movement',
    Field('movement_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('operation_id', 'reference operation'), # reference
    Field('concept_id', 'reference concept' ), # reference
    Field('price_id', 'reference price'), # ¿tarifaid? # reference
    Field('quantity', type='double', default=0),
    Field('amount', type='decimal(10,2)', default=0),
    Field('discriminated_id', 'reference tax'), # changed (was integer i.e. 21)
    Field('table_number', type='integer', default=0), # reference?
    Field('detail', type='string', length=255),
    Field('value', type='decimal(10,2)', default=0),
    Field('posted', type='date', default=request.now),
    Field('discount', type='decimal(10,2)'),
    Field('surcharge', type='decimal(10,2)'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

# pricelists
db.define_table('price_list',
    Field('price_list_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('entry', type='boolean', default=False),
    Field('exit', type='boolean', default=False),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

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
    format='%(description)s',
    migrate=migrate)

# points of sale
db.define_table('point_of_sale',
    Field('point_of_sale_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('branch'),
    Field('number', type='integer', default=0),
    Field('authorization_code', type='string', length=50), # Argentina's CAI (invoice printing official number)
    Field('due_date', type='datetime'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)
