# -*- coding: utf-8 -*-

migrate = True

db.define_table('staff_category',
    Field('staff_category_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('salary', type='double'),
    Field('hourly', type='double'),
    Field('type', type='string', length=1),  # reference?
    Field('journalized', type='boolean', default=False),
    Field('addition', type='datetime'),
    Field('deletion', type='datetime'),
    Field('agreement_id', 'reference agreement'),  # reference
    Field('plant_id', 'reference plant'),  # reference
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

db.define_table('staff',
    Field('staff_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('staff_category_id', 'reference staff_category'), # reference
    Field('name', type='string', length=40),
    Field('addres', type='string', length=40),
    Field('city_id', 'reference city'), # reference
    Field('zip_code', type='string', length=4),
    Field('state_id', 'reference state'),  # reference
    Field('telephone', type='string', length=12),
    Field('birth', type='datetime'),
    Field('id_number', type='string', length=15), # (Argentina's DNI)
    Field('nationality_id', 'reference country'), # reference country
    Field('tax_identification', type='string', length=13), # ¿cuil? (note: taxid != CUIT)
    Field('sex', type='string', length=1),
    Field('marital_status', type='string', length=1),
    Field('addition', type='datetime'),
    Field('deletion', type='datetime'),
    Field('replica', type='boolean', default=False),
    format='%(name)s',
    migrate=migrate)

