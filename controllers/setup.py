# -*- coding: utf-8 -*-

""" Setup for development db """

def setup():
    records = 0
    tables = 0
    # TODO: General app setup

    accounts = list()
    return dict(message="Done", records = records, tables = tables)


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
    
    # general dictionary for db initial setup
    # Incomplete
    
    # db data input design:
    # records: {
    #    "table_x": [ { "field_a": value, "field_b": value, ... }, ... { } ]
    # }
    
    records = dict()
    
    # for each tablename in records
    #     for each dictionary object obj in records["tablename"]:
    #         insert unpacked obj in tablename
    
    message="Done"
    return dict(message=message, records = len(records))


def db_to_csv():
    errors = []
    dumped = []
    with open('db_dump_file.csv','w') as the_file:
       db.export_to_csv_file(the_file)
    return dict(message="The CSV data was stored at your web2py root folder")
