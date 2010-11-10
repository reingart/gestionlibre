# coding: utf8

# customers/clients:
db.define_table('customer',
    Field('id', type='id'),
    Field('code', type='string', length=5, comment=T("Internal Code")),
    Field('name', type='string', length=100),
    Field('legal_name', type='string', length=50, comment='Raz\xc3\xb3n Social, Nombre o Denominaci\xc3\xb3n'),
    Field('address', type='string', length=100, comment='Direcci\xc3\xb3n Postal'),
    Field('zip', type='string', length=4),
    Field('city', type='string', length=20),
    Field('state', type='integer', default=0),
    Field('country', type='string', length=15),
    Field('fax', type='string', length=20, comment='Númeroo de Teléfono para Fax'),
    Field('phone', type='string', length=60, comment='Teléfonos'),
    ##Field('vendedorid', type='integer', default=0),
    ##Field('listaprecioid', type='integer', default=0),
    Field('taxid', type='string', length=20, comment='Número de CUIT'),
    Field('tax_category_id', type=db.tax_category, default=1),
    ##Field('condicionpagoid', type='integer', default=0),
    ##Field('ctacte', type='string', length=1, comment='Tipo de Cuenta Corriente'),
    ##Field('situacionid', type='reference situaciones', default=1, comment='Estado'),
    ##Field('grupoid', type='integer', default=1, comment='Grupo'),
    Field('observaciones', type='text'),
    ##Field('lugarentrega', type='text'),
    ##Field('nroproveedor', type='string', length=50),
    Field('alta', type='datetime', comment='Fecha de Alta/Inicio', default=request.now),
    Field('baja', type='datetime', comment='Fecha de Baja'),
    ##Field('limitecc', type='double'),
    ##Field('limitech', type='double'),
    ##Field('jurisdiccionid', type='integer'),
    ##Field('limitedeuda', type='decimal(10,None)'),
    format="%(name)s",
    migrate=migrate)
