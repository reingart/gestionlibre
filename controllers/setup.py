# -*- coding: utf-8 -*-

""" Setup for development db """

def setup():
    registros = 0
    tablas = 0

    # datos para completar tablas
    accounts = list()
    return dict(message="Listo", registros = registros, tablas = tablas)

def options():
    the_options = db(db.option).select()
    return dict(options = the_options)

def option():
    if len(request.args) > 0:
        the_option = request.args[1]
        form = crud.update(db.option, the_option)

    else:
        form = crud.create(db.option)

    return dict(form = form)

def initialize():
    message = ""
    db(db.option).delete()
    # For list reference/string/... values: use the "|1|2|...n|" syntax
    options = [
        {"name": "customer_allowed_orders", "description":"The order documents exposed to the user", "type": "list:reference document", "represent": None, "requires": None, "value": None},
        {"name": "customer_default_order", "description":"Default order document selected", "type": "reference document", "represent": None, "requires": None, "value": None},
        ]
    for o in options:
        db.option.insert(**o)

    message="Done"
    return dict(message=message, options = len(db(db.option).select()))


    