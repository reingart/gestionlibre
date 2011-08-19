# -*- coding: utf-8 -*-
migrate = True

# entry item (posting) "Partidas"
db.define_table('entry', # revisar: ¿"Partida"?
    Field('entry_id', 'id'),
    Field('code', unique = True),
    Field('description', type='string', length=50),
    Field('journal_entry_id', 'reference journal_entry'), # reference
    Field('account_id', 'reference account'), # reference
    Field('type', type='string', length=1), # reference?
    Field('amount', type='double'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)
