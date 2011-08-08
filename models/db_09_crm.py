# -*- coding: utf-8 -*-
migrate = True

# memos messages
db.define_table('memo',
    Field('memo_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('posted', type='date'),
    Field('contact_id', 'reference contact'),  # reference
    Field('subject', type='string', length=50),
    Field('observations', type='text'),
    Field('user_id', 'reference auth_user'),  # reference
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)


# many to many referenced user-contact table
db.define_table('contact_user',
    Field('contact_user_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('user_id', 'reference auth_user'),
    Field('contact_id', 'reference contact'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)
 
