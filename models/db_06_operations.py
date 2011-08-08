# -*- coding: utf-8 -*-
# Source Document types/categories (grouping ledgers)
# ie.: Invoice, Receipt, Purchase Order, pay stub, voucher, proof., etc. "Comprobantes"
migrate = True

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
 
