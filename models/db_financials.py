# coding: utf8

# cash management

# funds types (available, imprest/fixed/office fund):
db.define_table('fondos',
    Field('fondoid', type='id'),
    Field('fondo', type='string', length=50),
    Field('tipo', type='integer', default=0),
    Field('tope', type='decimal(10,None)', default=0),
    Field('saldo', type='decimal(10,None)', default=0),
    Field('cerrado', type='boolean', default=False),
    Field('ctasctes', type='boolean', default=False),
    Field('cheques', type='boolean', default=False),
    Field('conceptoid', type='integer'),
    Field('cuentaid', type='integer'),
    migrate=migrate)

# banks
db.define_table('bancos',
    Field('bancoid', type='integer', default=0),
    Field('id', type='integer'),
    Field('banco', type='string', length=250),
    Field('chequeid', type='integer', default=0),
    Field('conceptoid1', type='integer', default=0),
    primarykey=['bancoid'],
    migrate=migrate)

# bank reconciliation
db.define_table('conciliaciones',
    Field('conciliacionid', type='id'),
    Field('conceptoid', type='integer'),
    Field('fecha', type='date'),
    Field('importe', type='decimal(10,None)'),
    Field('movimientoid', type='integer'),
    Field('alta', type='date'),
    Field('baja', type='date'),
    Field('detalle', type='text'),
    migrate=migrate)

# cash balance
db.define_table('cierres',
    Field('cierreid', type='id'),
    Field('fecha', type='date'),
    Field('saldo', type='decimal(10,None)', default=0),
    Field('anulado', type='boolean', default=False),
    Field('balanceado', type='boolean', default=False),
    Field('impresiones', type='integer', default=0),
    Field('operacionid1', type='integer', default=0),
    Field('operacionid2', type='integer', default=0),
    Field('paginas', type='integer', default=0),
    Field('caja', type='integer', default=0),
    Field('fondoid', type='integer', default=0),
    migrate=migrate)

# payment terms
db.define_table('condicionespago',
    Field('condicionpagoid', type='integer', default=0),
    Field('condicionpago', type='string', length=50),
    Field('dias', type='integer', default=0),
    Field('dias2', type='integer', default=0),
    Field('dias3', type='integer', default=0),
    Field('cancelado', type='boolean', default=False),
    Field('conceptoid', type='integer', default=0),
    Field('ctasctes', type='boolean', default=False),
    primarykey=['condicionpagoid'],
    migrate=migrate)

# payment methods
db.define_table('formaspago',
    Field('formapagoid', type='id'),
    Field('formapago', type='string', length=50),
    Field('conceptoid', type='integer', default=0),
    Field('coeficiente1', type='double', default=0),
    Field('coeficiente2', type='double', default=0),
    Field('coeficiente3', type='double', default=0),
    Field('coeficiente4', type='double', default=0),
    Field('coeficiente5', type='double', default=0),
    Field('coeficiente6', type='double', default=0),
    Field('coeficiente7', type='double', default=0),
    Field('coeficiente8', type='double', default=0),
    Field('coeficiente9', type='double', default=0),
    Field('coeficiente10', type='double', default=0),
    Field('coeficiente11', type='double', default=0),
    Field('coeficiente12', type='double', default=0),
    Field('coeficiente13', type='double'),
    Field('coeficiente14', type='double'),
    Field('coeficiente16', type='double'),
    Field('coeficiente17', type='double'),
    Field('coeficiente18', type='double'),
    Field('coeficiente19', type='double'),
    Field('coeficiente20', type='double'),
    Field('coeficiente21', type='double'),
    Field('coeficiente22', type='double'),
    Field('coeficiente23', type='double'),
    Field('coeficiente24', type='double'),
    Field('cuota1', type='integer'),
    Field('cuota2', type='integer'),
    Field('cuota3', type='integer'),
    Field('cuota4', type='integer'),
    Field('cuota5', type='integer'),
    Field('cuota6', type='integer'),
    Field('cuota7', type='integer'),
    Field('cuota8', type='integer'),
    Field('cuota9', type='integer'),
    Field('cuota10', type='integer'),
    Field('cuota11', type='integer'),
    Field('cuota12', type='integer'),
    Field('cuota13', type='integer'),
    Field('cuota14', type='integer'),
    Field('cuota15', type='integer'),
    Field('cuota16', type='integer'),
    Field('cuota17', type='integer'),
    Field('cuota18', type='integer'),
    Field('cuota19', type='integer'),
    Field('cuota20', type='integer'),
    Field('cuota21', type='integer'),
    Field('cuota22', type='integer'),
    Field('cuota23', type='integer'),
    Field('cuota24', type='integer'),
    Field('dias1', type='integer'),
    Field('dias2', type='integer'),
    Field('dias3', type='integer'),
    Field('dias4', type='integer'),
    Field('dias5', type='integer'),
    Field('dias6', type='integer'),
    Field('dias7', type='integer'),
    Field('dias8', type='integer'),
    Field('dias9', type='integer'),
    Field('dias10', type='integer'),
    Field('dias11', type='integer'),
    Field('dias12', type='integer'),
    Field('dias13', type='integer'),
    Field('dias14', type='integer'),
    Field('dias15', type='integer'),
    Field('dias16', type='integer'),
    Field('dias17', type='integer'),
    Field('dias18', type='integer'),
    Field('dias19', type='integer'),
    Field('dias20', type='integer'),
    Field('dias21', type='integer'),
    Field('dias22', type='integer'),
    Field('dias23', type='integer'),
    Field('dias24', type='integer'),
    Field('gastos1', type='decimal(10,None)'),
    Field('gastos2', type='decimal(10,None)'),
    Field('gastos3', type='decimal(10,None)'),
    Field('gastos4', type='decimal(10,None)'),
    Field('gastos5', type='decimal(10,None)'),
    Field('gastos6', type='decimal(10,None)'),
    Field('gastos7', type='decimal(10,None)'),
    Field('gastos8', type='decimal(10,None)'),
    Field('gastos9', type='decimal(10,None)'),
    Field('gastos10', type='decimal(10,None)'),
    Field('gastos11', type='decimal(10,None)'),
    Field('gastos12', type='decimal(10,None)'),
    Field('gastos13', type='decimal(10,None)'),
    Field('gastos14', type='decimal(10,None)'),
    Field('gastos15', type='decimal(10,None)'),
    Field('gastos16', type='decimal(10,None)'),
    Field('gastos17', type='decimal(10,None)'),
    Field('gastos18', type='decimal(10,None)'),
    Field('gastos19', type='decimal(10,None)'),
    Field('gastos20', type='decimal(10,None)'),
    Field('gastos21', type='decimal(10,None)'),
    Field('gastos22', type='decimal(10,None)'),
    Field('gastos23', type='decimal(10,None)'),
    Field('gastos24', type='decimal(10,None)'),
    migrate=migrate)
    
# cost center
db.define_table('centroscosto',
    Field('centrocostoid', type='integer', default=0),
    Field('centrocosto', type='string', length=25),
    Field('alta', type='datetime'),
    Field('baja', type='datetime'),
    migrate=migrate)

# checkbook
db.define_table('chequeras',
    Field('chequeraid', type='id'),
    Field('chequera', type='string', length=50),
    Field('cuentaid', type='integer'),
    Field('conceptoid', type='integer'),
    Field('desde', type='integer', default=0),
    Field('hasta', type='integer', default=0),
    Field('proximo', type='integer', default=0),
    migrate=migrate)
    
# check
db.define_table('valores',
    Field('valorid', type='id'),
    Field('deudorid', type='integer'),
    Field('acreedorid', type='integer'),
    Field('numero', type='string', length=50),
    Field('bancoid', type='integer'),
    Field('importe', type='double'),
    Field('alta', type='datetime'),
    Field('vencimiento', type='datetime'),
    Field('baja', type='datetime'),
    Field('pagado', type='datetime'),
    Field('canjeado', type='boolean', default=False),
    Field('rechazado', type='boolean', default=False),
    Field('operacionid', type='integer'),
    Field('id1', type='integer'),
    Field('salida', type='integer'),
    Field('rechazo', type='integer'),
    Field('conceptoid', type='integer'),
    Field('detalle', type='string', length=50),
    Field('bd', type='integer'),
    Field('propio', type='boolean', default=False),
    Field('saldo', type='double'),
    migrate=migrate)

# credit card coupons
db.define_table('cupones',
    Field('cuponid', type='id'),
    Field('conceptoid', type='reference conceptos'),
    Field('numero', type='string', length=20),
    Field('lote', type='string', length=20),
    Field('cuotas', type='integer'),
    Field('importe', type='double'),
    Field('alta', type='date'),
    Field('baja', type='date'),
    Field('vencimiento', type='date'),
    Field('presentacion', type='date'),
    Field('pago', type='date'),
    Field('movimientoid', type='integer'),
    migrate=migrate)
