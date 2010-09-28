# coding: utf8

# tables used both in sales, purchases, etc.

# tax category
db.define_table('ivas',
    Field('iva', type='integer'),
    Field('categoria', type='string', length=25),
    Field('abr', type='string', length=3),
    Field('discriminar', type='boolean', default=False),
    Field('comprobanteidventas', type='integer', default=0),
    Field('comprobanteidcompras', type='integer', default=0),
    Field('replica', type='boolean', default=False),
    migrate=migrate)
       
# product main category    
db.define_table('rubros',
    Field('rubroid', type='id'),
    Field('rubro', type='string', length=20),
    Field('codigo', type='string', length=1),
    Field('productos', type='boolean', default=False),
    Field('unidades', type='boolean', default=False),
    Field('tiempos', type='boolean', default=False),
    migrate=migrate)

# product sub category
db.define_table('subrubros',
    Field('subrubroid', type='integer'),
    Field('codigo', type='string', length=5),
    Field('subrubro', type='string', length=50),
    migrate=migrate)

# states/province/district
db.define_table('provincias',
    Field('provinciaid', type='id'),
    Field('provincia', type='string', length=50),
    Field('codigo', type='string', length=1),
    migrate=migrate)

db.define_table('jurisdicciones',
    Field('jurisdiccionid', type='integer'),
    Field('jurisdiccion', type='string', length=50),
    primarykey=['jurisdiccionid'],
    migrate=migrate)
    
# country? 
# Adrress?
