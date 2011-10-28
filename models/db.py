# -*- coding: utf-8 -*- 

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
#########################################################################

if request.env.web2py_runtime_gae:            # if running on Google App Engine
    db = DAL('gae')                           # connect to Google BigTable
    session.connect(request, response, db = db) # and store sessions and tickets there
    ### or use the following lines to store sessions in Memcache
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
else:                                         # else use a normal relational database
    db = DAL('sqlite://storage.sqlite')       # if not, use SQLite or other DB
    # db = DAL('postgres://web2py:web2py@localhost:5432/gestionlibre') # local postgresql connection
    # TODO: adapt db model for dal pg auto-sql (unordered tables raise pg errors)

## if no need for session
# session.forget()

#########################################################################
## Here is sample code if you need for 
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import *
mail = Mail()                                  # mailer
auth = Auth(globals(),db)                      # authentication/authorization
crud = Crud(globals(),db)                      # for CRUD helpers using auth
service = Service(globals())                   # for json, xml, jsonrpc, xmlrpc, amfrpc
plugins = PluginManager()

mail.settings.server = 'logging' or 'smtp.gmail.com:587'  # your SMTP server
mail.settings.sender = 'you@gmail.com'         # your email
mail.settings.login = 'username:password'      # your credentials or None

auth.settings.hmac_key = 'sha512:3f00b793-28b8-4b3c-8ffb-081b57fac54a'   # before define_tables()
auth.define_tables()                           # creates all needed tables
auth.settings.mailer = mail                    # for user email verification
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.messages.verify_email = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['verify_email'])+'/%(key)s to verify your email'
auth.settings.reset_password_requires_verification = True
auth.messages.reset_password = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['reset_password'])+'/%(key)s to reset your password'

#########################################################################
## If you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, uncomment and customize following
# from gluon.contrib.login_methods.rpx_account import RPXAccount
# auth.settings.actions_disabled=['register','change_password','request_reset_password']
# auth.settings.login_form = RPXAccount(request, api_key='...',domain='...',
#    url = "http://localhost:8000/%s/default/user/login" % request.application)
## other login methods are in gluon/contrib/login_methods
#########################################################################

crud.settings.auth = None                      # =auth to enforce authorization on crud

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

###################
# GestionLibre data
###################

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
                    element = random.choice([char for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]) # get random char
                elif element == "N":
                    element = random.randint(0,9) # get random integer
                elif element == "B":
                    element = random.choice([char for char in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"]) # get random alphanumeric
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

def custom_post_login(arg):
    contacts_per_user = len(db(db.contact_user.user_id == auth.user_id).select())
    if contacts_per_user < 1:
        redirect(URL(c="registration", f="post_register_specify_firm"))        

def custom_post_register(arg):
    redirect(URL(c="registration", f="post_register_specify_firm"))

auth.settings.register_onaccept = custom_post_register
auth.settings.login_onaccept = custom_post_login

migrate = True

# import GestionLibre database definitions
import db_gestionlibre
db_gestionlibre.define_tables(db, web2py = True)
