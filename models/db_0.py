# coding: utf8

migrate = True

# falta normalizar (ciudad/pais) 
# falta traducir

# categorías de IVA
db.define_table('tax_category',
    Field('id', 'id'),
    Field('name', 'string'),
    format='%(name)s',
    migrate=migrate,
    )

# impuestos (mayormente IVA)
db.define_table('tax',
    Field('id', type='id'),
    Field('name', type='string'),
    format='%(name)s',
    migrate=migrate,
    )
    
# jurisdicción
db.define_table('tax_zone',
    Field('id', type='id'),
    Field('name', type='string'),
    Field('rate', type='double'),
    format='%(name)s',
    migrate=migrate,
    )

# alicuotas
db.define_table('tax_rate',
    Field('id', type='id'),
    Field('tax_id', type=db.tax),
    Field('tax_zone_id', type=db.tax_zone),
    Field('rate', type='double'),
    format='%(name)s',
    migrate=migrate,
    )
