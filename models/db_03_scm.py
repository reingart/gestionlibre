# -*- coding: utf-8 -*-
migrate = True

# suppliers/providers:
db.define_table('supplier',
    Field('supplier_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('legal_name', type='string', length=50),
    Field('tax_id', 'reference tax', default=0), # Argentina's IVA # reference
    Field('tax_identification', type='string', length=20), # Argentina's CUIT
    Field('address', type='string', length=30),
    Field('zip_code', type='string', length=50),
    Field('city_id', 'reference city'), # reference
    Field('state_id', 'reference state'),  # reference
    Field('telephone', type='string', length=20),
    Field('fax', type='string', length=50),
    Field('situation_id', 'reference situation'),  # reference
    Field('id_number', type='string', length=20), # ¿Argentina's DNI?
    Field('observations', type='text'),
    Field('identity_card', type='string', length=20),
    Field('birth', type='datetime'),
    Field('nationality_id', 'reference country'),  # reference country
    Field('jurisdiction_id', 'reference jurisdiction'),  # reference
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)
 
