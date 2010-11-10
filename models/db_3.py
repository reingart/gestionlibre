# coding: utf8

# Source Document types/categories (grouping ledgers)
# ie.: Invoice, Receipt, Purchase Order, pay stub, voucher, proof., etc.
db.define_table('document',
    Field('id', type='id', default=0),
    Field('name', type='string', length=50),
    #Field('talonarioid', type='integer', default=0),
    Field('code', type='string', length=3),
    #Field('tipo', type='string', length=1),
    #Field('gravar', type='boolean', default=False),
    #Field('discriminar', type='boolean', default=False),
    Field('prefix', type='integer', default=0, comment='Punto de venta / sucursal'),
    Field('number', type='integer', default=0, comment='Próximo número'),
    Field('sell', type='boolean', default=False),
    Field('buy', type='boolean', default=False),
    Field('fiscal', type='boolean', default=False),
    Field('stock', type='boolean', default=False),
    Field('charge_account', type='boolean', default=False),
    #Field('contado', type='boolean', default=False),
    Field('debit', type='boolean', default=False),
    Field('credit', type='boolean', default=False),
    Field('invoice', type='boolean', default=False),
    Field('receipt', type='boolean', default=False),
    Field('shipping', type='boolean', default=False,),
    Field('order_', type='boolean', default=False),
    ##Field('budget', type='boolean', default=False),
    ##Field('señas', type='boolean', default=False),
    Field('accountable', type='boolean', default=False),
    #Field('printer', type='string', length=50),
    #Field('lines', type='integer', default=0),
    #Field('fondoid', type='integer', default=0),
    #Field('notas', type='text'),
    #Field('observaciones', type='text'),
    #Field('descripcion', type='text'),
    ##Field('caja', type='boolean', default=False),
    ##Field('reservas', type='boolean', default=False),
    ##Field('pdf_template_id', type='integer'),
    ##Field('copias', type='integer'),
    ##Field('confirmarimpresion', type='boolean', default=False),
    Field('internal', type='boolean', default=False),
    Field('inverted', type='boolean', default=False),
    ##Field('continuo', type='boolean', default=False),
    ##Field('multipleshojas', type='boolean', default=False),
    ##Field('preimpreso', type='boolean', default=False),
    format="%(name)s",
    migrate=migrate)
