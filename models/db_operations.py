# -*- coding: utf-8 -*-

migrate = True

# Source Document types/categories (grouping ledgers)
# ie.: Invoice, Receipt, Purchase Order, pay stub, voucher, proof., etc. "Comprobantes"
db.define_table('documenttype',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('pointofsale','reference pointofsale'), # reference
    Field('abbr', type='string', length=3),
    Field('type', type='string', length=1), # reference?
    Field('tax', type='boolean', default=False), # ¿gravar?
    Field('discriminate', type='boolean', default=False),
    Field('branch', 'reference branch'), # ¿sucursal? # reference
    Field('number', type='integer', default=0),
    Field('entry', type='boolean', default=False),
    Field('exit', type='boolean', default=False),
    Field('fiscal', type='boolean', default=False),
    Field('stock', type='boolean', default=False),
    Field('currentaccount', type='boolean', default=False),
    Field('cash', type='boolean', default=False), # ¿al contado?
    Field('debit', type='boolean', default=False),
    Field('credit', type='boolean', default=False),
    Field('invoices', type='boolean', default=False),
    Field('receipts', type='boolean', default=False),
    Field('packingslips', type='boolean', default=False), # ¿Remitos?
    Field('orders', type='boolean', default=False),
    Field('countable', type='boolean', default=False),
    Field('printer', type='string', length=50), # reference?
    Field('lines', type='integer', default=0),
    Field('fund', 'reference fund'), # reference
    Field('replicate', type='boolean', default=False),
    Field('notes', type='text'),
    Field('observations', type='text'),
    Field('descriptions', type='text'),
    Field('cashbox', type='boolean', default=False), # ¿caja?
    Field('books', type='boolean', default=False), # ¿reservas?
    Field('form', 'string'), # reference?
    Field('budget', type='boolean', default=False),
    Field('downpayment', type='boolean', default=False),
    Field('copies', type='integer'),
    Field('confirmprinting', type='boolean', default=False),
    Field('internal', type='boolean', default=False),
    Field('invert', type='boolean', default=False),
    Field('continuous', type='boolean', default=False),
    Field('multiplepages', type='boolean', default=False),
    Field('preprinted', type='boolean', default=False),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

# Account reference/detail (lowest level of the Chart of Accounts)
# ie: products/services, payments, income, expenses, etc.
db.define_table('concept',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('item', 'reference item'), # reference
    Field('subitem', 'reference subitem'), # reference
    Field('family', 'reference family'), # reference
    Field('color', 'reference color'),# reference
    Field('size', 'reference size'), # reference
    Field('quantity', type='integer', default=0),
    Field('amount', type='double', default=0),
    Field('addition', type='date'),
    Field('deletion', type='date'),
    Field('vat'), # reference
    Field('purveyor', 'reference purveyor'), # reference
    Field('customer', 'reference customer'), # reference
    Field('account', 'reference account'),# reference
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
    Field('paymentmethod', type='boolean', default=False),
    Field('tax', type='boolean', default=False),
    Field('currentaccount', type='boolean', default=False),
    Field('cashbox', type='boolean', default=False),
    Field('extra', type='boolean', default=False),
    Field('cash', type='boolean', default=False),
    Field('banks', type='boolean', default=False),
    Field('receipt', type='string', length=50),
    Field('statement', type='string', length=50), # ¿resumen?
    Field('abbr', type='string', length=50),
    Field('stockquantity', type='double'),
    Field('collection', 'reference collection'), # reference
    Field('floor', type='double'), # ¿mínimo?
    Field('suspended', type='boolean', default=False),
    Field('discounts', type='boolean', default=False),
    Field('surcharges', type='boolean', default=False),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

# Source Document (transactions records)
db.define_table('transactionrecord',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('customer', 'reference customer'), # reference
    Field('purveyor', 'reference purveyor'), # reference
    Field('detail', type='string', length=60, comment='Observations'),
    Field('paymentterms', type='integer', comment='Terms of payment'), # reference
    Field('term', type='string', length=50),
    Field('amount', type='double'),
    Field('balance', type='double'),
    Field('date', type='datetime'),
    Field('issue', type='datetime'),
    Field('documenttype', 'reference documenttype', comment='Points to order / invoice / packingslips'), # reference
    Field('branch', 'reference branch'), # reference
    Field('number', type='integer', default=0),
    Field('duedate', type='datetime'),
    Field('type', type='string', length=1), # reference?
    Field('canceled', type='boolean', default=False, comment='False if deferred payment (df), True if paid with cash, ch (check) or current account'),
    Field('processed', type='boolean', default=False),
    Field('voided', type='boolean', default=False), # ¿anulado?
    Field('fund', 'reference fund'), # reference
    Field('costcenter', 'reference costcenter'), # reference
    Field('module', type='integer', default=0, comment='Referenced table'), # reference?
    Field('observations', type='string', length=50),
    Field('cancellation', type='boolean', default=False),
    Field('avoidance', type='boolean', default=False), # ¿anulación?
    Field('file', 'reference file'), # ¿legajo? # reference
    Field('liquidation', 'reference liquidation'), # reference
    Field('user', 'reference auth_user'), # reference
    Field('hour', type='datetime'),
    Field('replicated', type='datetime'),
    Field('subcustomer', 'reference subcustomer'), # reference
    Field('salesperson', 'reference salesperson'), # reference
    Field('printed', type='boolean', default=False),
    Field('jurisdiction', 'reference jurisdiction'), # reference
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

# Source document items (posting)
# ie.: "traditional" line items
db.define_table('activity',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('transactionrecord', 'reference transactionrecord'), # reference
    Field('concept', 'reference concept' ), # reference
    Field('price', 'reference price'), # ¿tarifaid? # reference
    Field('quantity', type='double', default=0),
    Field('amount', type='decimal(10,2)', default=0),
    Field('discriminated', 'reference vat'), # changed (was integer i.e. 21)
    Field('tablenumber', type='integer', default=0), # reference?
    Field('detail', type='string', length=255),
    Field('value', type='decimal(10,2)', default=0),
    Field('start', type='date'),
    Field('discount', type='decimal(10,2)'),
    Field('surcharge', type='decimal(10,2)'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

# pricelists
db.define_table('pricelist',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('entry', type='boolean', default=False),
    Field('exit', type='boolean', default=False),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

# price "engine":
db.define_table('price',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('concept', 'reference concept'), # reference
    Field('item', 'reference item'), # reference
    Field('salesperson', 'reference salesperson'), # reference
    Field('customer', 'reference customer'), # reference
    Field('purveyor', 'reference purveyor'), # reference
    Field('contactgroup', 'reference contactgroup'), # reference
    Field('situation', 'reference situation'), # reference
    Field('fund', 'reference fund'), # reference
    Field('rate', 'reference rate', comment='Container type'), # ¿tarifaid? # reference
    Field('paymentmethod', 'reference paymentmethod', comment='Method of payment'), # reference
    Field('documenttype', 'reference documenttype', comment='Document type'), # reference
    Field('pricelist', 'reference pricelist'), # reference
    Field('taxed', type='boolean', default=False),
    Field('vat', 'reference vat'), # reference
    Field('type', type='string', length=1), # reference?
    Field('value', type='double', default=0, comment='Insert a value to calculate'),
    Field('calculate', type='string', length=1),
    Field('operation'), # reference
    Field('source', type='string', length=1, comment='Field on wich operations will be performed'),
    Field('condition', type='string', length=2),
    Field('quantity1', type='double'),
    Field('quantity2', type='double'),
    Field('discriminate', type='boolean', default=False),
    Field('priority', type='integer'),
    Field('formula', type='text'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

# points of sale
db.define_table('pointofsale',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('branch', 'reference branch'), # reference
    Field('number', type='integer', default=0),
    Field('pac', type='string', length=50), # Argentina's CAI (invoice printing official number)
    Field('duedate', type='datetime'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

db.define_table('branch',
    Field('name'),
    Field('code', default=new_custom_serial_code),
    Field('description'),
    Field('address'),
    Field('city', 'reference city'),
    Field('state', 'reference state'),
    Field('country', 'reference country'),
    format='%(name)s',
    migrate=migrate)

# the documents "Comprobante"
db.define_table('document',
    Field('code', unique=True, default=new_custom_serial_code),
    Field('description'),
    Field('documenttype', 'reference documenttype'),
    Field('branch', 'reference branch'),
    Field('pointofsale', 'reference pointofsale'),
    Field('time', 'datetime', default=request.now),
    Field('notes', 'text'),
    Field('replica', 'boolean', default=True),    
    format = '%(description)s',
    migrate=migrate)
    
# The detail of a document
db.define_table('documentelement',
    Field('code', unique=True, default=new_custom_serial_code),
    Field('description'),
    Field('concept', 'reference concept'),
    Field('product', 'reference product'),
    Field('transactionrecord', 'reference transactionrecord'),
    Field('quantity', 'double'),
    Field('replica', 'boolean', default=True),
    format = '%(description)s',
    migrate=migrate,
    )
