# -*- coding: utf-8 -*-

migrate = True

# Human Resources management

db.define_table('staff',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('name', type='string', length=40),
    Field('addres', type='string', length=40),
    Field('city', 'reference city'), # reference
    Field('zipcode', type='string', length=4),
    Field('state', 'reference state'),  # reference
    Field('telephone', type='string', length=12),
    Field('birth', type='datetime'),
    Field('ssn', type='string', length=15), # (Argentina's DNI)
    Field('nationality', 'reference country'), # reference country
    Field('itin', type='string', length=13), # ¿cuil?
    Field('sex', type='string', length=1),
    Field('maritalstatus', type='string', length=1),
    Field('addition', type='datetime'),
    Field('deletion', type='datetime'),
    Field('replica', type='boolean', default=False),
    format='%(name)s',
    migrate=migrate)

db.define_table('plant',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

db.define_table('department',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

db.define_table('laborunion',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('percentage', type='integer', default=0, comment='Personal percentage for the union'),
    Field('patronal', type='integer', default=0, comment='Employer percentage for the union'),
    Field('voluntary', type='integer', default=0, comment='Voluntary contribution'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

db.define_table('file',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('staff', 'reference staff'),  # reference
    Field('extrahours', type='double'),
    Field('presenteesm', type='double', comment='Presenteesm amount'), # ¿presentismo?
    Field('gobermentincrease', type='double', comment='salary extra by statal dispositions (divided by months)'),
    Field('sickdays', type='integer', default=0, comment='Number of sick days'),
    Field('presenteesmdiscount', type='double'),
    Field('failure', type='double', comment='Failure discount'),
    Field('contributiondiscount', type='double'),
    Field('seniority', type='double'),
    Field('perdiem', type='double', comment='Per diem amount'),
    Field('profitpercentage', type='double'),
    Field('schooling', type='integer', default=0, comment='Schooling help: number of children'),
    Field('allowance', type='integer', default=0, comment='Number of children for annual allowance'),
    Field('paidvacation', type='double'),
    Field('halfbonus', type='double', comment='Importe del Medio Aguinaldo'),
    Field('prenatal', type='integer', default=0),
    Field('category', 'reference category'),  # reference
    Field('healthcare', 'reference healthcare'),  # reference
    Field('laborunion', 'reference laborunion'),  # reference
    Field('pension', type='integer', default=0, comment='(pension id)'),  # reference
    Field('costcenter', 'reference costcenter'),  # reference
    Field('entry', type='datetime'),
    Field('exit', type='datetime'),
    Field('salary', type='double', comment='Base salary (monthly)'),
    Field('seniorityyears', type='integer'),
    Field('spouse', type='boolean', default=False),
    Field('senioritymonths', type='integer'),
    Field('largefamily', type='boolean', default=False),
    Field('code', type='string', length=20),
    Field('department', 'reference department'),  # reference
    Field('role', 'reference role'),  # reference
    Field('plant', 'reference plant'),  # reference
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

db.define_table('payroll',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description', comment='Type and period'),
    Field('type', type='string', length=1),  # reference?
    Field('halfbonus', type='boolean', default=False),
    Field('vacations', type='boolean', default=False),
    Field('fromdate', type='datetime'),
    Field('todate', type='datetime'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

db.define_table('new',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('file', 'reference file'),  # reference
    Field('concept', 'reference concept'),  # reference
    Field('datum', type='double', default=0),
    Field('payroll', 'reference payroll'),  # reference
    Field('addition', type='date'),
    Field('deletion', type='date'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

db.define_table('healthcare',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('percentage', type='integer', default=0, comment='Contribution percentage'),
    Field('patronal', type='integer', default=0, comment='Patronal contribution'),
    Field('voluntary', type='integer', default=0, comment='Voluntary contribution'),
    Field('adherent', type='integer', default=0, comment='Aporte por Adherente'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)
    
db.define_table('pension',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('percentage', type='double', comment='Personal contribution'),
    Field('contribution', type='integer', default=0, comment='Employer contribution'),
    Field('socialservices', type='integer', default=0), # Argentina: law number 19032
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)
    
db.define_table('role',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)
    
db.define_table('category',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('salary', type='double'),
    Field('hourly', type='double'),
    Field('type', type='string', length=1),  # reference?
    Field('journalized', type='boolean', default=False),
    Field('addition', type='datetime'),
    Field('deletion', type='datetime'),
    Field('agreement', 'reference agreement'),  # reference
    Field('plant', 'reference plant'),  # reference
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)
    
db.define_table('column',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('abbr', type='string', length=50),
    Field('ordernumber', type='integer', default=0), # order
    Field('receipt', type='boolean', default=False),
    Field('remunerative', type='boolean', default=False),
    Field('transactionrecord', 'reference transactionrecord'), # ¿operación?  # reference
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

db.define_table('relative',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('name', type='string', length=100),
    Field('staff', 'reference staff'),  # reference
    Field('kinship', type='string', length=1),
    Field('itin', type='string', length=13),
    Field('allowance', type='boolean', default=False),
    Field('disabled', type='boolean', default=False),
    Field('schooling', type='boolean', default=False),
    Field('nationality', 'reference nationality'),  # reference country
    Field('birth', type='datetime', comment='Fec.Nac.'),
    Field('maritalstatus', type='string', length=1, comment='marital status'),
    Field('address', type='string', length=25),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)
    
db.define_table('formula',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('name', type='string', length=50),
    Field('quantity', type='text'),
    Field('amount', type='double'),
    Field('datum', type='double'),
    Field('format', type='string', length=1),  # reference?
    Field('text', type='text'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)
    
   
db.define_table('salary',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('costcenter', 'reference costcenter'),  # reference
    Field('category', 'reference category'),  # reference
    Field('file', 'reference file'), # reference
    Field('concept', 'reference concept'), # reference
    Field('liquidation', 'reference liquidation'),  # reference
    Field('type', type='string', length=1),  # reference?
    Field('halfbonus', type='boolean', default=False),
    Field('quantity', type='double'),
    Field('amount', type='double'),
    Field('fromdate', type='datetime'),
    Field('todate', type='datetime'),
    Field('fixed', type='boolean', default=False),
    Field('liquidated', type='boolean', default=False),
    Field('format', type='string', length=1),
    Field('text', type='string', length=255),
    Field('agreement', 'reference agreement'),  # reference
    Field('department', 'reference department'), # reference
    Field('role', 'reference role'),
    Field('plant', 'reference plant'), # reference
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)

db.define_table('agreement',
    Field('code', unique = True, default=new_custom_serial_code),
    Field('description'),
    Field('text', type='text'),
    Field('amount', type='double'),
    Field('replica', type='boolean', default=False),
    format='%(description)s',
    migrate=migrate)
