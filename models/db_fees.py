# coding: utf8

# Fees, installments, quotes

db.define_table('aranceles',
    Field('arancelid', type='integer', default=0),
    Field('arancel', type='string', length=50),
    Field('vencimiento', type='date'),
    Field('numero', type='integer', default=0),
    Field('mes', type='integer', default=0),
    Field('anio', type='integer', default=0),
    Field('altas', type='boolean', default=False),
    Field('codigo', type='string', length=50),
    Field('comprobanteid', type='integer', default=0),
    Field('extras', type='boolean', default=False),
    Field('boleta', type='boolean', default=False),
    Field('separar', type='boolean', default=False),
    Field('desde', type='date'),
    Field('hasta', type='date'),
    migrate=migrate)
    
db.define_table('planes',
    Field('planid', type='id'),
    Field('deudorid', type='integer', default=-1),
    Field('acreedorid', type='integer', default=-1, comment='Beneficiario'),
    Field('subdeudorid', type='integer', default=0),
    Field('arancelid', type='integer', default=0),
    Field('monto', type='double', comment='Monto Neto'),
    Field('descuento', type='double'),
    Field('pagado', type='double'),
    Field('cuotas', type='integer', default=0, comment='Cantidad de Cuotas'),
    Field('intereses', type='double', default=0, comment='Intereses Cedidos'),
    Field('mora', type='double', default=0, comment='Recargos Punitorios por D\xc3\xada'),
    Field('importe', type='double', comment='Importe Mensual'),
    Field('pagadas', type='integer', default=0),
    Field('desde', type='integer', default=0, comment='CuotaID'),
    Field('hasta', type='integer', default=0, comment='CuotaID'),
    Field('inicio', type='datetime'),
    Field('vencimiento1', type='datetime', comment='x dias del mes'),
    Field('vencimiento2', type='datetime', comment='y dias del mes'),
    Field('observaciones', type='string', length=50),
    Field('cancelado', type='boolean', default=False),
    Field('replica', type='boolean', default=False),
    Field('cobrado', type='double'),
    migrate=migrate)
    
db.define_table('cuotas',
    Field('cuotaid', type='id'),
    Field('planid', type='integer', default=0),
    Field('arancelid', type='integer', default=0),
    Field('importe', type='double'),
    Field('recargo', type='double'),
    Field('descuento', type='double'),
    Field('pagado', type='double'),
    Field('vencimiento', type='datetime'),
    Field('entrada', type='integer', default=0),
    Field('salida', type='integer', default=0),
    Field('cancelado', type='boolean', default=False),
    Field('replica', type='boolean', default=False),
    Field('cobrado', type='double'),
    Field('extra', type='boolean', default=False),
    migrate=migrate)
