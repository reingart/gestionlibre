# coding: utf8

# Supply Chain Management

# suppliers/providers:
db.define_table('acreedores',
    Field('acreedorid', type='id'),
    Field('codigo', type='string', length=5),
    Field('acreedor', type='string', length=50),
    Field('razon', type='string', length=50),
    Field('iva', type='integer', default=0),
    Field('cuit', type='string', length=20),
    Field('direccion', type='string', length=30),
    Field('cp', type='string', length=50),
    Field('localidad', type='string', length=50),
    Field('provinciaid', type='integer', default=0),
    Field('telefono', type='string', length=20),
    Field('fax', type='string', length=50),
    Field('situacionid', type='integer', default=1),
    Field('documento', type='string', length=20),
    Field('observaciones', type='text'),
    Field('cuil', type='string', length=20),
    Field('cdi', type='string', length=20),
    Field('nacimiento', type='datetime'),
    Field('nacionalidad', type='string', length=35),
    Field('replica', type='boolean', default=False),
    Field('jurisdiccionid', type='integer'),
    migrate=migrate)
    
# collections
db.define_table('colecciones',
    Field('coleccionid', type='id'),
    Field('coleccion', type='string', length=50),
    Field('desde', type='date'),
    Field('hasta', type='date'),
    Field('replica', type='boolean', default=False),
    migrate=migrate)

# colours (products 1st variant) 
db.define_table('colores',
    Field('colorid', type='id'),
    Field('codigo', type='string', length=10),
    Field('color', type='string', length=50),
    Field('replica', type='boolean', default=False),
    migrate=migrate)

# sizes (products 2nd variant ) ie. clothes...
db.define_table('talle',
    Field('talleid', type='id'),
    Field('talle', type='string', length=50),
    Field('replica', type='boolean', default=False),
    migrate=migrate)
    
# warehouses
db.define_table('depositos',
    Field('depositoid', type='id'),
    Field('deposito', type='string', length=50),
    Field('direccion', type='string', length=50),
    Field('replica', type='boolean', default=False),
    migrate=migrate)
    
# product structure (bill of materials)
db.define_table('estructuras',
    Field('estructuraid', type='id'),
    Field('conceptoid', type='integer'),
    Field('id', type='integer'),
    Field('cantidad', type='double', default=0),
    Field('scrap', type='double', default=0),
    Field('replica', type='boolean', default=False),
    migrate=migrate)

# product families/lines grouping
db.define_table('familias',
    Field('familiaid', type='integer', default=0),
    Field('codigo', type='string', length=15),
    Field('familia', type='string', length=50),
    Field('coleccionid', type='integer'),
    Field('importe', type='decimal(10,None)', default=0),
    Field('entrada', type='boolean', default=False),
    Field('replica', type='boolean', default=False),
    Field('salida', type='boolean', default=False),
    Field('rubroid', type='integer'),
    Field('subrubroid', type='integer'),
    Field('acreedorid', type='integer'),
    Field('suspendido', type='boolean', default=False),
    primarykey=['familiaid'],
    migrate=migrate)

# rates / fare / tariff
db.define_table('tarifas',
    Field('tarifaid', type='id'),
    Field('tarifa', type='string', length=50),
    Field('tipo', type='string', length=1),
    Field('capacidad', type='double'),
    Field('medida', type='string', length=1),
    Field('stock', type='integer', default=0),
    Field('indice', type='double', default=0),
    Field('precio', type='double', default=0),
    migrate=migrate)

# products inventory (in/out)
db.define_table('stock',
    Field('stockid', type='id'),
    Field('conceptoid', type='integer', default=0),
    Field('fecha', type='datetime', comment='Fecha de Entrada'),
    Field('reservado', type='boolean', default=False),
    Field('depositoid', type='integer', default=0),
    Field('id', type='integer'),
    Field('acumulado', type='boolean', default=False),
    Field('stock', type='double', default=0),
    migrate=migrate)
