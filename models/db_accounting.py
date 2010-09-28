# coding: utf8

# Account (higher level of Chart of Accounts)
db.define_table('cuentas',
    Field('cuentaid', type='id'),
    Field('codigo', type='string', length=50),
    Field('cuenta', type='string', length=50),
    Field('recibe', type='boolean', default=False),
    Field('agrupa', type='integer', default=0),
    Field('bancoid', type='integer', default=0),
    Field('iva', type='boolean', default=False),
    Field('iibb', type='boolean', default=False),
    Field('percepciones', type='boolean', default=False),
    Field('retenciones', type='boolean', default=False),
    migrate=migrate)

# Accounting period, fiscal year (FY):
db.define_table('ejercicios',
    Field('ejercicioid', type='id'),
    Field('ejercicio', type='string', length=50),
    Field('desde', type='date'),
    Field('hasta', type='date'),
    Field('replica', type='boolean', default=False),
    migrate=migrate)

# Journal entry
db.define_table('asientos',
    Field('asientoid', type='id'),
    Field('numero', type='integer', default=0),
    Field('asiento', type='string', length=50, comment='Descripci\xc3\xb3n'),
    Field('fecha', type='datetime'),
    Field('valorizacion', type='datetime'),
    Field('tipo', type='string', length=1),
    Field('borrador', type='boolean', default=False),
    Field('ejercicioid', type='integer', default=0),
    migrate=migrate)

# entry item (posting):
db.define_table('partidas',
    Field('partidaid', type='id'),
    Field('partida', type='string', length=50),
    Field('asientoid', type='integer', default=0),
    Field('cuentaid', type='integer', default=0),
    Field('tipo', type='string', length=1),
    Field('importe', type='double'),
    migrate=migrate)
