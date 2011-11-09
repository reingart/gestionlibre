# -*- coding: utf-8 -*-
from gluon import *
import datetime

# table/field functions

def define_tables(db, auth, web2py = True, migrate = True):

    # custom serial code creation. Include plain text between \t tab chars: "A\tThis is not randomized\tBN"
    # A: alphabetical, B: alphanumeric, N: integers between zero and nine, \t [text] \t: normal text bounds
    # To include "A", "B", "N" use the \tA\t syntax. Auxiliar characters are allowed outside \t \t separators
    # As expected, no \t characters are allowed inside escaped text
    # TODO: Simplify/standarize serial code pseudo-syntax for user html form input


    CUSTOM_SERIAL_CODE_STRUCTURE = "AAAA-NNNN-BBBBBB"
    def new_custom_serial_code(structure=CUSTOM_SERIAL_CODE_STRUCTURE):
        import random
        def generate_custom_serial_code(s):
            tmpstring = ""
            skip = False
            for element in s:
                if not skip:
                    if element == "A":
                        element = random.choice([char for char in \
                        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]) # get random char
                    elif element == "N":
                        element = random.randint(0,9) # get random integer
                    elif element == "B":
                        element = random.choice([char for char in \
                        "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"]) # get random alphanumeric
                    elif element == "\t":
                        skip = True
                        continue
                else:
                    if element == "\t":
                        skip = False
                        continue
                tmpstring += str(element)
            return tmpstring

        while True:
            the_code = generate_custom_serial_code(structure)
            if len(db(db.custom_serial_code.code == the_code).select()) <= 0:
                # store serial code in db
                db.custom_serial_code.insert(code = the_code)
                return the_code

        return None


    # login/register forms
    
    def custom_post_login(arg):
        contacts_per_user = len(db(db.contact_user.user_id == auth.user_id).select())
        if contacts_per_user < 1:
            redirect(URL(a="gestionlibre", c="registration", f="post_register_specify_firm"))

    def custom_post_register(arg):
        redirect(URL(a="gestionlibre", c="registration", f="post_register_specify_firm"))


    # auth settings
    
    if web2py == True:
        auth.settings.register_onaccept = custom_post_register
        auth.settings.login_onaccept = custom_post_login


    def today():
        return datetime.date.today()

    def now():
        return datetime.datetime.now()

    def price_format(price):
        try:
            r = "%s - %s" % (price.concept_id.description, price.price_list_id.description)
        except (ValueError, KeyError, AttributeError, IndexError, RuntimeError):
            r = "Format error. price index " + str(price.price_id)
        return r

    def operation_format(r):
        try:
            of = "%s %s" % (db.document[r.document_id].description, r.operation_id)
        except (AttributeError, KeyError, ValueError, TypeError):
            of = "Format error: operation %s" % r.operation_id
        return of


    if not web2py:
        # Auth tables
        db.define_table("auth_user", Field("first_name"), Field("last_name"), \
        Field("email"), Field("password"), Field("registration_key"), \
        Field("reset_password_key"))

    # db_00_accounting

    # Accounting period, fiscal year (FY) "Ejercicios"
    db.define_table('accounting_period',
        Field('accounting_period_id', 'id'),
        Field('code', unique = True),
        Field('description', type='string', length=50),
        Field('starting', type='date'),
        Field('ending', type='date'),
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    # db_00_common

    # tables used both in sales, purchases, etc.

    # product main category
    db.define_table('category',
        Field('category_id', 'id'),
        Field('code', unique = True),
        Field('description', type='string', length=20),
        Field('products', type='boolean', default=False),
        Field('units', type='boolean', default=False), # ¿unidades?
        Field('times', type='boolean', default=False), # ¿tiempos?
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    # product sub category
    db.define_table('subcategory',
        Field('subcategory_id', 'id'),
        Field('code', unique = True),
        Field('description', type='string', length=50),
        Field('category_id', 'reference category'),
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    db.define_table('jurisdiction',
        Field('jurisdiction_id', 'id'),
        Field('code', unique = True),
        Field('description', type='string', length=50),
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    # country?
    db.define_table('country',
        Field('country_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    # states/province/district
    db.define_table('state',
        Field('state_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('country_id', 'reference country'),
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    # city?
    db.define_table('city',
        Field('city_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('city', type='string', length=50),
        Field('state_id', 'reference state'),
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    # Address?
    db.define_table('address',
        Field('address_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('street', type='string'),
        Field('number', type='string', length=50),
        Field('other', type='string', length=200), # whatever else comes here
        Field('zip_code', type='string', length=9), # Argentina's CPA
        Field('city_id', 'reference city'),
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    # tax category
    db.define_table('tax',
        Field('tax_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('tax', 'boolean'), # Argentina's CUIT (yes/no)
        Field('percentage', type='double'),
        Field('aliquot', type='double'),
        Field('category'), # vat type
        Field('abbr', type='string', length=3),
        Field('discriminate', type='boolean', default=False),
        Field('document_sales_id', 'integer'),  # reference
        Field('document_purchases_id', 'integer'),  # reference
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)


    # custom serial code table for validation purposes
    db.define_table('custom_serial_code',
        Field('custom_serial_code_id', 'id'),
        Field('code', unique=True),
        Field('replica', 'boolean', default=True),
        format='%(code)s',
        migrate=migrate)

    # debugging entries
    db.define_table('debugging',
        Field('debugging_id', 'id'),
        Field('msg', 'text'),
        format='%(msg)s',
        migrate=migrate)

    # gestionlibre options
    db.define_table('option',
        Field('option_id', 'id'),
        Field('name', unique=True, requires=IS_NOT_EMPTY()), # "option_1"
        Field('args'), # a value to perform name-args searches (i.e. id or id1 | ... idn)
        Field('description'),
        Field('type', requires=IS_NOT_EMPTY(), default = 'string'), # a valid dal field type
        Field('represent'),
        Field('requires'),
        Field('value', 'text'),
        format='%(name)s',
        migrate=migrate)

    # db_00_crm

    # groups
    db.define_table('customer_group',
        Field('customer_group_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    # status (active, unactive, prospect, etc.)
    db.define_table('situation',
        Field('situation_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    # db_00_financials

    # cost center
    db.define_table('cost_center',
        Field('cost_center_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('addition', type='datetime'),
        Field('deletion', type='datetime'),
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    # banks "Bancos"
    db.define_table('bank',
        Field('bank_id', 'id'),
        Field('code', unique = True),
        Field('description', type='string', length=250),
        Field('bank_check'),  # reference
        Field('concept_id', 'integer'),  # reference
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    # db_00_hr

    db.define_table('plant',
        Field('plant_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    db.define_table('department',
        Field('department_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    db.define_table('labor_union',
        Field('labor_union_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('percentage', type='integer', default=0, comment='Personal percentage for the union'),
        Field('patronal', type='integer', default=0, comment='Employer percentage for the union'),
        Field('voluntary', type='integer', default=0, comment='Voluntary contribution'),
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    db.define_table('payroll',
        Field('payroll_id', 'id'),
        Field('code', unique = True),
        Field('description', comment='Type and period'),
        Field('type', type='string', length=1),  # reference?
        Field('half_bonus', type='boolean', default=False),
        Field('vacations', type='boolean', default=False),
        Field('starting', type='datetime'),
        Field('ending', type='datetime'),
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    db.define_table('healthcare',
        Field('healthcare_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('percentage', type='integer', default=0, comment='Contribution percentage'),
        Field('patronal', type='integer', default=0, comment='Patronal contribution'),
        Field('voluntary', type='integer', default=0, comment='Voluntary contribution'),
        Field('adherent', type='integer', default=0, comment='Aporte por Adherente'),
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    db.define_table('pension',
        Field('pension_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('percentage', type='double', comment='Personal contribution'),
        Field('contribution', type='integer', default=0, comment='Employer contribution'),
        Field('social_services', type='integer', default=0), # Argentina: law number 19032
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    db.define_table('role',
        Field('role_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    db.define_table('formula',
        Field('formula_id', 'id'),
        Field('code', unique = True),
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

    db.define_table('agreement',
        Field('agreement_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('text', type='text'),
        Field('amount', type='double'),
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    # db_00_operations

    # pricelists
    db.define_table('price_list',
        Field('price_list_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('entry', type='boolean', default=False),
        Field('exit', type='boolean', default=False),
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    # points of sale
    db.define_table('point_of_sale',
        Field('point_of_sale_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('branch'),
        Field('number', type='integer', default=0),
        Field('authorization_code', type='string', length=50), # Argentina's CAI (invoice printing official number)
        Field('due_date', type='datetime'),
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)


    # db_00_scm

    # collections "Colecciones"
    db.define_table('collection',
        Field('collection_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('starting', type='date'),
        Field('ending', type='date'),
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    # colours (products 1st variant)
    db.define_table('color',
        Field('color_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    # sizes (products 2nd variant ) ie. clothes...
    db.define_table('size',
        Field('size_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('type'),
        Field('order_number', 'integer'),
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    # warehouses
    db.define_table('warehouse',
        Field('warehouse_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('address', type='string', length=50),
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    # rates / fare / tariff
    db.define_table('rate',
        Field('rate_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('type', type='string', length=1),  # reference?
        Field('capacity', type='double'),
        Field('measure', type='string', length=1),
        Field('stock', type='integer', default=0),
        Field('index_value', type='double', default=0),
        Field('price', type='double', default=0),
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    # db_01_accounting

    # Account (higher level of Chart of Accounts) "Cuentas"
    db.define_table('account',
        Field('account_id', 'id'),
        Field('code', unique = True),
        Field('description', type='string', length=50),
        Field('receives', type='boolean', default=False),
        Field('customer_group_id', 'reference customer_group'), # reference
        Field('bank_id', 'reference bank'), # reference
        Field('tax', type='boolean', default=False),
        Field('gross_receipts', type='boolean', default=False), # ¿iibb?
        Field('collections', type='boolean', default=False), # ¿percepciones?
        Field('retentions', type='boolean', default=False),
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    # Journal entry "Asientos"
    db.define_table('journal_entry',
        Field('journal_entry_id', 'id'),
        Field('code', unique = True),
        Field('description', type='string', length=50, comment='Description'),
        Field('number', type='integer', default=0),
        Field('posted', type='datetime', default=now),
        Field('source'),
        Field('valuation', type='datetime'),
        Field('type', type='string', length=1), # reference?
        Field('draft', type='boolean', default=False),
        Field('accounting_period_id', 'reference accounting_period'), # reference
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    # db_01_hr

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

    # db_02_accounting

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

    # db_02_crm

    # salesman
    db.define_table('salesperson',
        Field('salesperson_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('staff_id', 'reference staff'), # reference
        Field('commission', type='double'),
        Field('telephone', type='string', length=50),
        Field('address', type='string', length=50),
        Field('state_id', 'reference state'),  # reference
        Field('city_id', 'reference city'),  # reference
        Field('notes', type='text'),
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    # db_02_hr

    db.define_table('file',
        Field('file_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('staff_id', 'reference staff'),  # reference
        Field('extra_hours', type='double'),
        Field('presenteesm', type='double', comment='Presenteesm amount'), # ¿presentismo?
        Field('government_increase', type='double', comment='salary extra by statal dispositions (divided by months)'),
        Field('sick_days', type='integer', default=0, comment='Number of sick days'),
        Field('presenteesm_discount', type='double'),
        Field('failure', type='double', comment='Failure discount'),
        Field('contribution_discount', type='double'),
        Field('seniority', type='double'),
        Field('per_diem', type='double', comment='Per diem amount'),
        Field('profit_percentage', type='double'),
        Field('schooling', type='integer', default=0, comment='Schooling help: number of children'),
        Field('allowance', type='integer', default=0, comment='Number of children for annual allowance'),
        Field('paid_vacation', type='double'),
        Field('half_bonus', type='double', comment='Importe del Medio Aguinaldo'),
        Field('prenatal', type='integer', default=0),
        Field('staff_category_id', 'reference staff_category'),  # reference
        Field('healthcare_id', 'reference healthcare'),  # reference
        Field('labor_union_id', 'reference labor_union'),  # reference
        Field('pension_id', 'reference pension', default=0, comment='(pension id)'),  # reference
        Field('cost_center_id', 'reference cost_center'),  # reference
        Field('entry', type='datetime'),
        Field('exit', type='datetime'),
        Field('salary', type='double', comment='Base salary (monthly)'),
        Field('seniority_years', type='integer'),
        Field('spouse', type='boolean', default=False),
        Field('seniority_months', type='integer'),
        Field('large_family', type='boolean', default=False),
        Field('department_id', 'reference department'),  # reference
        Field('role_id', 'reference role'),  # reference
        Field('plant_id', 'reference plant'),  # reference
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    db.define_table('relative',
        Field('relative_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('name', type='string', length=100),
        Field('staff_id', 'reference staff'),  # reference
        Field('kinship', type='string', length=1),
        Field('tax_identification', type='string', length=13),
        Field('allowance', type='boolean', default=False),
        Field('disabled', type='boolean', default=False),
        Field('schooling', type='boolean', default=False),
        Field('nationality_id', 'reference country'),  # reference country
        Field('birth', type='datetime', comment='Fec.Nac.'),
        Field('marital_status', type='string', length=1, comment='marital status'),
        Field('address', type='string', length=25),
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    # db_03_scm

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

    # db_04_scm

    # product families/lines grouping
    db.define_table('family',
        Field('family_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('collection_id', 'reference collection'), # reference
        Field('amount', type='decimal(10,2)', default=0),
        Field('entry', type='boolean', default=False),
        Field('exit', type='boolean', default=False),
        Field('category_id', 'reference category'),  # reference
        Field('subcategory_id', 'reference subcategory'),  # reference
        Field('supplier_id', 'reference supplier'),  # reference
        Field('suspended', type='boolean', default=False),
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    # db_05_operations

    db.define_table('concept',
        Field('concept_id', 'id'),
        Field('code', unique = True, default=new_custom_serial_code),
        Field('description'),
        Field('category_id', 'reference category'), # reference
        Field('subcategory_id', 'reference subcategory'), # reference
        Field('family_id', 'reference family'), # reference
        Field('color_id', 'reference color'),# reference
        Field('size_id', 'reference size'), # reference
        Field('quantity', type='integer', default=0),
        Field('amount', type='double', default=0),
        Field('addition', type='date'),
        Field('deletion', type='date'),
        Field('tax_id', 'reference concept'), # self table reference
        Field('supplier_id', 'reference supplier'), # reference
        Field('customer_id', 'integer'), # reference
        Field('account_id', 'reference account'),# reference
        Field('measure', type='string', length=1),
        Field('desired', type='double', default=0), # ¿deseado?
        Field('presentation', type='string', length=100),
        Field('entry', type='boolean', default=False),
        Field('exit', type='boolean', default=False),
        Field('taxed', type='boolean', default=False), #  ¿gravado?
        Field('stock', type='boolean', default=False),
        Field('unitary', type='boolean', default=False),
        Field('internal', type='boolean', default=False),
        Field('payment_method', type='boolean', default=False),
        Field('tax', type='boolean', default=False),
        Field('current_account', type='boolean', default=False),
        Field('cash_box', type='boolean', default=False),
        Field('extra', type='boolean', default=False),
        Field('cash', type='boolean', default=False),
        Field('banks', type='boolean', default=False),
        Field('receipt', type='string', length=50),
        Field('statement', type='string', length=50), # ¿resumen?
        Field('abbr', type='string', length=50),
        Field('stock_quantity', type='double'),
        Field('collection_id', 'reference collection'), # reference
        Field('floor', type='double'), # ¿mínimo?
        Field('suspended', type='boolean', default=False),
        Field('discounts', type='boolean', default=False),
        Field('surcharges', type='boolean', default=False),
        Field('replica', type='boolean', default=False),
        Field('orderable', 'boolean', default=False), # can be ordered/bought, do not use, filter concepts by internal property
        format='%(description)s',
        migrate=migrate)

    db.concept.tax_id.requires = IS_IN_DB(db(db.concept.tax == True), "concept.concept_id", "%(description)s")

    # db_06_financials

    # funds types (available, imprest/fixed/office fund): "Fondos"
    db.define_table('fund',
        Field('fund_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('type', type='integer', default=0), # reference?
        Field('upper_limit', type='decimal(10,2)', default=0),
        Field('balance', type='decimal(10,2)', default=0),
        Field('closed', type='boolean', default=False),
        Field('current_account', type='boolean', default=False),
        Field('bank_checks', type='boolean', default=False),
        Field('concept_id', 'reference concept'),  # reference
        Field('account_id', 'reference account'), # reference
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    # payment terms "CondicionesPago"
    db.define_table('payment_terms',
        Field('payment_terms_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('canceled', type='boolean', default=False),
        Field('concept_id', 'reference concept'),  # reference
        Field('current_account', type='boolean', default=False),
        Field('days_1', 'integer'),
        Field('days_2', 'integer'),
        Field('days_3', 'integer'),
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    # payment methods
    db.define_table('payment_method',
        Field('payment_method_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('concept_id', 'reference concept'),  # reference
        Field('coupons', 'integer'),

        Field('coefficient_01', type='double'),
        Field('coefficient_02', type='double'),
        Field('coefficient_03', type='double'),
        Field('coefficient_04', type='double'),
        Field('coefficient_05', type='double'),
        Field('coefficient_06', type='double'),
        Field('coefficient_07', type='double'),
        Field('coefficient_08', type='double'),
        Field('coefficient_09', type='double'),
        Field('coefficient_10', type='double'),
        Field('coefficient_11', type='double'),
        Field('coefficient_12', type='double'),
        Field('coefficient_13', type='double'),
        Field('coefficient_14', type='double'),
        Field('coefficient_15', type='double'),
        Field('coefficient_16', type='double'),
        Field('coefficient_17', type='double'),
        Field('coefficient_18', type='double'),
        Field('coefficient_19', type='double'),
        Field('coefficient_20', type='double'),
        Field('coefficient_21', type='double'),
        Field('coefficient_22', type='double'),
        Field('coefficient_23', type='double'),
        Field('coefficient_24', type='double'),

        Field('quota_01', type='integer'),  # reference?
        Field('quota_02', type='integer'),  # reference?
        Field('quota_03', type='integer'),  # reference?
        Field('quota_04', type='integer'),  # reference?
        Field('quota_05', type='integer'),  # reference?
        Field('quota_06', type='integer'),  # reference?
        Field('quota_07', type='integer'),  # reference?
        Field('quota_08', type='integer'),  # reference?
        Field('quota_09', type='integer'),  # reference?
        Field('quota_10', type='integer'),  # reference?
        Field('quota_11', type='integer'),  # reference?
        Field('quota_12', type='integer'),  # reference?
        Field('quota_13', type='integer'),  # reference?
        Field('quota_14', type='integer'),  # reference?
        Field('quota_15', type='integer'),  # reference?
        Field('quota_16', type='integer'),  # reference?
        Field('quota_17', type='integer'),  # reference?
        Field('quota_18', type='integer'),  # reference?
        Field('quota_19', type='integer'),  # reference?
        Field('quota_20', type='integer'),  # reference?
        Field('quota_21', type='integer'),  # reference?
        Field('quota_22', type='integer'),  # reference?
        Field('quota_23', type='integer'),  # reference?
        Field('quota_24', type='integer'),  # reference?

        Field('days_01', type='integer'),
        Field('days_02', type='integer'),
        Field('days_03', type='integer'),
        Field('days_04', type='integer'),
        Field('days_05', type='integer'),
        Field('days_06', type='integer'),
        Field('days_07', type='integer'),
        Field('days_08', type='integer'),
        Field('days_09', type='integer'),
        Field('days_10', type='integer'),
        Field('days_11', type='integer'),
        Field('days_12', type='integer'),
        Field('days_13', type='integer'),
        Field('days_14', type='integer'),
        Field('days_15', type='integer'),
        Field('days_16', type='integer'),
        Field('days_17', type='integer'),
        Field('days_18', type='integer'),
        Field('days_19', type='integer'),
        Field('days_20', type='integer'),
        Field('days_21', type='integer'),
        Field('days_22', type='integer'),
        Field('days_23', type='integer'),
        Field('days_24', type='integer'),

        Field('expenditure_01', type='decimal(10,2)'), # ¿gasto?
        Field('expenditure_02', type='decimal(10,2)'), # ¿gasto?
        Field('expenditure_03', type='decimal(10,2)'), # ¿gasto?
        Field('expenditure_04', type='decimal(10,2)'), # ¿gasto?
        Field('expenditure_05', type='decimal(10,2)'), # ¿gasto?
        Field('expenditure_06', type='decimal(10,2)'), # ¿gasto?
        Field('expenditure_07', type='decimal(10,2)'), # ¿gasto?
        Field('expenditure_08', type='decimal(10,2)'), # ¿gasto?
        Field('expenditure_09', type='decimal(10,2)'), # ¿gasto?
        Field('expenditure_10', type='decimal(10,2)'), # ¿gasto?
        Field('expenditure_11', type='decimal(10,2)'), # ¿gasto?
        Field('expenditure_12', type='decimal(10,2)'), # ¿gasto?
        Field('expenditure_13', type='decimal(10,2)'), # ¿gasto?
        Field('expenditure_14', type='decimal(10,2)'), # ¿gasto?
        Field('expenditure_15', type='decimal(10,2)'), # ¿gasto?
        Field('expenditure_16', type='decimal(10,2)'), # ¿gasto?
        Field('expenditure_17', type='decimal(10,2)'), # ¿gasto?
        Field('expenditure_18', type='decimal(10,2)'), # ¿gasto?
        Field('expenditure_19', type='decimal(10,2)'), # ¿gasto?
        Field('expenditure_20', type='decimal(10,2)'), # ¿gasto?
        Field('expenditure_21', type='decimal(10,2)'), # ¿gasto?
        Field('expenditure_22', type='decimal(10,2)'), # ¿gasto?
        Field('expenditure_23', type='decimal(10,2)'), # ¿gasto?
        Field('expenditure_24', type='decimal(10,2)'), # ¿gasto?

        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    # checkbook
    db.define_table('checkbook',
        Field('checkbook_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('account_id', 'reference account'),  # reference
        Field('concept_id', 'reference concept'),  # reference
        Field('starting', type='datetime'),
        Field('ending', type='datetime'),
        Field('next', type='integer', default=0),  # reference?
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    # db_06_hr

    # new "Noticia"
    db.define_table('payroll_new',
        Field('payroll_new_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('file_id', 'reference file'),  # reference
        Field('concept_id', 'reference concept'),  # reference
        Field('datum', type='double', default=0),
        Field('payroll_id', 'reference payroll'),  # reference
        Field('addition', type='date'),
        Field('deletion', type='date'),
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    db.define_table('salary',
        Field('salary_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('payroll_id', 'reference payroll'),
        Field('cost_center_id', 'reference cost_center'),  # reference
        Field('staff_category_id', 'reference staff_category'),  # reference
        Field('file_id', 'reference file'), # reference
        Field('concept_id', 'reference concept'), # reference
        Field('liquidation'),  # reference?
        Field('type', type='string', length=1),  # reference?
        Field('half_bonus', type='boolean', default=False),
        Field('quantity', type='double'),
        Field('amount', type='double'),
        Field('starting', type='datetime'),
        Field('ending', type='datetime'),
        Field('fixed', type='boolean', default=False),
        Field('liquidated', type='boolean', default=False),
        Field('format', type='string', length=1),
        Field('text', type='string', length=255),
        Field('agreement_id', 'reference agreement'),  # reference
        Field('department_id', 'reference department'), # reference
        Field('role_id', 'reference role'),
        Field('plant_id', 'reference plant'), # reference
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    # db_06_operations

    db.define_table('document',
        Field('document_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('point_of_sale_id','reference point_of_sale'), # reference
        Field('abbr', type='string', length=3),
        Field('type', type='string', length=1), # reference?
        Field('tax', type='boolean', default=False), # ¿gravar?
        Field('discriminate', type='boolean', default=False),
        Field('branch'), # ¿sucursal?
        Field('number', type='integer', default=0),
        Field('entry', type='boolean', default=False),
        Field('exit', type='boolean', default=False),
        Field('fiscal', type='boolean', default=False),
        Field('stock', type='boolean', default=False),
        Field('current_account', type='boolean', default=False),
        Field('cash', type='boolean', default=False), # ¿al contado?
        Field('debit', type='boolean', default=False),
        Field('credit', type='boolean', default=False),
        Field('invoices', type='boolean', default=False),
        Field('receipts', type='boolean', default=False),
        Field('packing_slips', type='boolean', default=False), # ¿Remitos?
        Field('orders', type='boolean', default=False), # ¿Pedidos?
        Field('budget', type='boolean', default=False), # ¿Presupuesto?
        Field('countable', type='boolean', default=False),
        Field('printer', type='string', length=50), # reference?
        Field('lines', type='integer', default=0),
        Field('fund_id', 'reference fund'), # reference
        Field('replicate', type='boolean', default=False),
        Field('notes', type='text'),
        Field('observations', type='text'),
        Field('descriptions', type='text'),
        Field('cash_box', type='boolean', default=False), # ¿caja?
        Field('books', type='boolean', default=False), # ¿reservas?
        Field('form', 'string'), # reference?
        Field('down_payment', type='boolean', default=False),
        Field('copies', type='integer'),
        Field('confirm_printing', type='boolean', default=False),
        Field('internal', type='boolean', default=False),
        Field('invert', type='boolean', default=False),
        Field('continuous', type='boolean', default=False),
        Field('multiple_pages', type='boolean', default=False),
        Field('preprinted', type='boolean', default=False),
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    # db_06_scm

    # product structure (bill of materials)
    db.define_table('product_structure',
        Field('product_structure_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('concept_id', 'reference concept'),
        Field('quantity', type='double', default=0),
        Field('scrap', type='double', default=0),
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)



    # products inventory (in/out)
    db.define_table('stock',
        Field('stock_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('concept_id', 'reference concept'),  # reference
        Field('posted', type='date', comment='Date of entry'),
        Field('reserved', type='boolean', default=False),
        Field('warehouse_id', 'reference warehouse'),  # reference
        Field('accumulated', type='boolean', default=False),
        Field('value', type='double', default=0),
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    # db_07_crm

    # customers/clients: "Deudores"
    db.define_table('customer',
        Field('customer_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('contact'),
        Field('legal_name', type='string', length=50, comment='Customer firm name'),
        Field('address', type='string', length=100, comment='Postal address'),
        Field('zip_code', type='string', length=9),
        Field('city_id', 'reference city'),
        Field('state_id', 'reference state'),
        Field('country_id', 'reference country'),
        Field('fax', type='string', length=20, comment='Fax'),
        Field('telephone', type='string', length=60, comment='Telephone numbers'),
        Field('salesperson_id', 'reference salesperson'), # reference
        Field('price_list_id', 'reference price_list'), # reference
        Field('tax_identification', type='string', length=20, comment='Tax _id'), # similar to Argentina's cuit
        Field('tax_id', 'reference tax'),  # reference
        Field('payment_terms_id', 'reference payment_terms'),  # reference
        Field('invoice', type='string', length=1, comment='Invoice header type'),
        Field('current_account', type='string', length=1, comment='Type of current account'),  # reference?
        Field('situation_id', 'reference situation', comment='Finantial situation'),  # reference
        Field('customer_group_id', 'reference customer_group', comment='Contact Group'),  # reference
        Field('observations', type='text'),
        Field('place_of_delivery', type='text'),
        Field('supplier', 'string'), # no reference (customer entry)
        Field('addition', type='datetime', comment='Customer starting date'),
        Field('deletion', type='datetime', comment='Customer deletion date'),
        Field('replica', type='boolean', default=False),
        Field('current_account_limit', type='double'),
        Field('check_limit', type='double'),
        Field('jurisdiction_id', 'reference jurisdiction'),  # reference
        Field('debt_limit', type='decimal(10,2)'),
        Field('id_number'), # Argentina's DNI
        Field('transport'),
        Field('replica', type='boolean', default=False),
        format='%(legal_name)s',
        migrate=migrate)

    # sub-customers ("sub-accounts") "CLIENTES"
    db.define_table('subcustomer',
        Field('subcustomer_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('customer_id', 'reference customer'),  # reference
        Field('legal_name', type='string', length=50),
        Field('address', type='string', length=100),
        Field('zip_code', type='string', length=4),
        Field('city_id', 'reference city'),
        Field('state_id', 'reference state'),  # reference
        Field('country_id', 'reference country'), # reference
        Field('fax', type='string', length=20),
        Field('telephone', type='string', length=60),
        Field('tax_id', 'reference tax'),  # reference
        Field('tax_identification'),  # reference
        Field('invoice', type='string', length=1),
        Field('current_account', type='string', length=1),  # reference?
        Field('price_list_id', 'reference price_list'),  # reference
        Field('situation_id', 'reference situation'),  # reference
        Field('customer_group_id', 'reference customer_group'),  # reference
        Field('observations', type='text'),
        Field('place_of_delivery', type='text'),
        Field('supplier', 'string'),  # no reference (subcustomer entry)
        Field('addition', type='datetime'),
        Field('deletion', type='datetime'),
        Field('current_account_limit', type='double'),
        Field('check_limit', type='double'),
        Field('jurisdiction_id', 'reference jurisdiction'), # reference
        Field('sex', type="string", length=1),
        Field('birth', type='date'),
        Field('balance', type='double'),
        Field('replica', type='boolean', default=False),
        format='%(legal_name)s',
        migrate=migrate)

    # db_07_fees

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

    # db_08_crm

    # contacts
    db.define_table('contact',
        Field('contact_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('customer_id', 'reference customer'),  # reference
        Field('supplier_id', 'reference supplier'),  # reference
        Field('tax_identification'),  # Argentina's CUIT
        Field('department', type='string', length=50),  # reference?
        Field('telephone', type='string', length=100),
        Field('fax', type='string', length=100),
        Field('email', type='string', length=100),
        Field('schedule', type='string', length=100),
        Field('address', type='string', length=50),
        Field('zip_code', type='string', length=50, comment='Zip code'),
        Field('city_id', 'reference city'),  # reference
        Field('state_id', 'reference state'),  # reference
        Field('observations', type='text'),
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    # db_08_fees

    db.define_table('installment',
        Field('installment_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('customer_id', 'reference customer'), # reference
        Field('supplier_id', 'reference supplier', comment='Wich supplier to pay to'), # reference
        Field('subcustomer_id', 'reference subcustomer'), # reference
        Field('fee_id', 'reference fee'), # reference
        Field('net', type='double', comment='Net amount'),
        Field('discount', type='double'),
        Field('paid', type='double'),
        Field('quotas', type='integer', default=0, comment='number of quotas'),
        Field('interests', type='double', default=0, comment='Transferred interests'),
        Field('late_payment', type='double', default=0, comment='Late payment fees'),
        Field('monthly_amount', type='double'),
        Field('paid_quotas', type='integer', default=0),
        Field('starting_quota_id', 'integer', comment='quota_id'), # reference
        Field('ending_quota_id', 'integer', default=0, comment='quota_id'), # reference
        Field('starting', type='datetime'),
        Field('first_due', type='datetime', comment='x days of month'),
        Field('second_due', type='datetime', comment='y days of month'),
        Field('observations', type='string', length=50),
        Field('canceled', type='boolean', default=False),
        Field('collected', type='double'),
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    db.define_table('quota',
        Field('quota_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('installment_id', 'reference installment'),
        Field('number', 'integer'), # TODO: computed field: index number in quotas ordered set +1 (order by id)
        Field('fee_id', 'reference fee'), # reference
        Field('amount', type='double'),
        Field('surcharge', type='double'),
        Field('discount', type='double'),
        Field('paid', type='double'),
        Field('due_date', type='datetime'),
        Field('entry', type='integer', default=0), # reference?
        Field('exit', type='integer', default=0), # reference?
        Field('canceled', type='boolean', default=False),
        Field('collected', type='double'),
        Field('extra', type='boolean', default=False),
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    # db_08_operations

    # Source Document (transactions records)
    db.define_table('operation',
        Field('operation_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('customer_id', 'reference customer'), # reference
        Field('supplier_id', 'reference supplier'), # reference
        Field('detail', type='string', length=60, comment='Observations'),
        Field('payment_terms_id', 'reference payment_terms', comment='Terms of payment'), # reference
        Field('term', type='string', length=50),
        Field('amount', type='double'),
        Field('balance', type='double'),
        Field('posted', type='datetime', default = now),
        Field('issue', type='datetime'),
        Field('document_id', 'reference document', comment='Points to order / invoice / packingslips'), # reference
        Field('branch'),
        Field('number', type='integer', default=0),
        Field('due_date', type='datetime'),
        Field('type', type='string', length=1, requires=IS_IN_SET({'T': 'Stock','S': 'Sales','P': 'Purchases'})), # reference? types: T: Stock, S: Sales, P: Purchases
        Field('canceled', type='boolean', default=False, comment='False if deferred payment (df), True if paid with cash, ch (check) or current account'),
        Field('processed', type='boolean', default=False),
        Field('voided', type='boolean', default=False), # ¿anulado?
        Field('fund_id', 'reference fund'), # reference
        Field('cost_center_id', 'reference cost_center'), # reference
        Field('module', type='integer', default=0, comment='Referenced table'), # reference?
        Field('observations', type='string', length=50),
        Field('cancellation', type='boolean', default=False),
        Field('avoidance', type='boolean', default=False), # ¿anulación?
        Field('file_id', 'reference file'), # ¿legajo? # reference
        Field('payroll_id', 'reference payroll'), # reference
        Field('user_id', 'reference auth_user'), # reference
        Field('hour', type='datetime'),
        Field('replicated', type='datetime'),
        Field('subcustomer_id', 'reference subcustomer'), # reference
        Field('salesperson_id', 'reference salesperson'), # reference
        Field('printed', type='boolean', default=False),
        Field('jurisdiction_id', 'reference jurisdiction'), # reference
        Field('replica', type='boolean', default=False),
        format=operation_format,
        migrate=migrate)


    # price "engine":
    db.define_table('price',
        Field('price_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('concept_id', 'reference concept'), # reference
        Field('category_id', 'reference category'), # reference
        Field('salesperson_id', 'reference salesperson'), # reference
        Field('customer_id', 'reference customer'), # reference
        Field('supplier_id', 'reference supplier'), # reference
        Field('customer_group_id', 'reference customer_group'), # reference
        Field('situation_id', 'reference situation'), # reference
        Field('fund_id', 'reference fund'), # reference
        Field('rate_id', 'reference rate', comment='Container type'), # ¿tarifaid? # reference
        Field('payment_method_id', 'reference payment_method', comment='Method of payment'), # reference
        Field('document_id', 'reference document', comment='Document type'), # reference
        Field('price_list_id', 'reference price_list'), # reference
        Field('taxed', type='boolean', default=False),
        Field('tax_id', 'reference tax'), # reference
        Field('type', type='string', length=1), # reference?
        Field('value', type='double', default=0, comment='Insert a value to calculate'),
        Field('calculate', type='string', length=1),
        Field('operation'), # reference?
        Field('source', type='string', length=1, comment='Field on wich operations will be performed'),
        Field('condition', type='string', length=2),
        Field('quantity_1', type='double'),
        Field('quantity_2', type='double'),
        Field('discriminate', type='boolean', default=False),
        Field('priority', type='integer'),
        Field('formula', type='text'),
        Field('replica', type='boolean', default=False),
        format=price_format,
        migrate=migrate)


    # db_09_crm

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

    # db_09_financials

    # check
    db.define_table('bank_check',
        Field('bank_check_id', 'id'),
        Field('checkbook_id', 'reference checkbook', \
        requires=IS_EMPTY_OR(IS_IN_DB(db(db.checkbook), \
        "checkbook.checkbook_id", "%(description)s"))), # reference
        Field('code', unique = True),
        Field('description'),
        Field('customer_id', 'reference customer'), # reference
        Field('supplier_id', 'reference supplier'), # reference
        Field('number', type='string', length=50),
        Field('bank_id', 'reference bank'),  # reference
        Field('amount', type='double'),
        Field('addition', type='datetime'),
        Field('due_date', type='datetime'),
        Field('deletion', type='datetime'),
        Field('paid', type='datetime'),
        Field('exchanged', type='boolean', default=False),
        Field('bouncer', type='boolean', default=False),
        Field('operation_id', 'reference operation'),  # reference
        Field('id_1', type='integer'),
        Field('exit', type='integer'),
        Field('rejection', type='integer'),
        Field('concept_id', 'reference concept'),  # reference
        Field('detail', type='string', length=50),
        Field('bd', type='integer'),
        Field('own', type='boolean', default=False),
        Field('balance', type='double'),
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    # cash balance "Cierres"
    db.define_table('cash_balance',
        Field('cash_balance_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('posted', type='date'),
        Field('balance', type='decimal(10,2)', default=0),
        Field('canceled', type='boolean', default=False), # ¿anulado?
        Field('balanced', type='boolean', default=False),
        Field('prints', type='integer', default=0),
        Field('operation_1_id', 'reference operation'),  # reference
        Field('operation_2_id', 'reference operation'),  # reference
        Field('pages', type='integer', default=0),
        Field('cash', type='integer', default=0),
        Field('fund_id', 'reference fund'),  # reference
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    # db_09_hr

    # column
    db.define_table('payroll_column',
        Field('payroll_column_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('abbr', type='string', length=50),
        Field('order_number', type='integer', default=0), # order
        Field('receipt', type='boolean', default=False),
        Field('remunerative', type='boolean', default=False),
        Field('operation_id', 'reference operation'), # ¿operación?  # reference
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    # db_09_operations

    # ie.: "traditional" line items
    db.define_table('movement',
        Field('movement_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('operation_id', 'reference operation'), # reference
        Field('concept_id', 'reference concept' ), # reference
        Field('price_id', 'reference price'), # ¿tarifaid? # reference
        Field('quantity', type='double', default=0),
        Field('amount', type='decimal(10,2)', default=0),
        Field('discriminated_id', 'reference tax'), # changed (was integer i.e. 21)
        Field('table_number', type='integer', default=0), # reference?
        Field('detail', type='string', length=255),
        Field('value', type='decimal(10,2)', default=0),
        Field('posted', type='date', default=today),
        Field('discount', type='decimal(10,2)'),
        Field('surcharge', type='decimal(10,2)'),
        Field('replica', type='boolean', default=False),
        Field('bank_check_id', 'integer'), # reference
        format='%(description)s',
        migrate=migrate)

    # db_10_financials

    # bank reconciliation "Conciliación"
    db.define_table('reconciliation',
        Field('reconciliation_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('concept_id', 'reference concept'),  # reference
        Field('posted', type='date'),
        Field('amount', type='decimal(10,2)'),
        Field('movement_id', 'reference movement'), # ¿movimiento?  # reference
        Field('addition', type='date'),
        Field('deletion', type='date'),
        Field('detail', type='text'),
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)


    # credit card coupons
    db.define_table('credit_card_coupon',
        Field('credit_card_coupon_id', 'id'),
        Field('code', unique = True),
        Field('description'),
        Field('concept_id', 'reference concept'),  # reference
        Field('number', type='string', length=20),
        Field('lot', type='string', length=20),
        Field('fees', type='integer'),
        Field('amount', type='double'),
        Field('addition', type='date'),
        Field('deletion', type='date'),
        Field('due_date', type='date'),
        Field('presentation', type='date'),
        Field('payment', type='date'),
        Field('movement_id', 'reference movement'), # ¿movimiento?  # reference
        Field('replica', type='boolean', default=False),
        format='%(description)s',
        migrate=migrate)

    # end of define_tables function
    