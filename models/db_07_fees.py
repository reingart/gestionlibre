# -*- coding: utf-8 -*-

migrate = True

# Fees, installments, quotes

db.define_table('fee',
    Field('fee_id', 'id'),
    Field('code', unique = True),
    Field('description'),
    Field('due_date', type='date'),
    Field('number', type='integer', default=0),
    Field('month', type='integer', default=0),
    Field('year', type='integer', default=0),
    Field('additions', type='boolean', default=False),
    Field('document_id', 'reference document'), # reference
    Field('extras', type='boolean', default=False),
    Field('ticket', type='boolean', default=False),
    Field('separate', type='boolean', default=False),
    Field('starting', type='date'),
    Field('ending', type='date'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)
 
