# -*- coding: utf-8 -*-

""" Setup for development db """

def setup():
    records = 0
    tables = 0
    # TODO: General app setup

    accounts = list()
    return dict(message=T("Done"), records = records, tables = tables)


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
    
    message=T("Done")
    return dict(message=message, records = len(records))


def db_to_csv():
    errors = []
    dumped = []
    with open('db_dump_file.csv','wb') as the_file:
       db.export_to_csv_file(the_file)
    return dict(message=T("The CSV data was stored at your web2py root folder"))

def csv_to_db():
    import os
    response.generic_patterns = ["*"]    
    errors = []
    loaded = []
    form = SQLFORM.factory(Field("folder", requires=IS_NOT_EMPTY(), comment=T("/absolute/folder/path")), Field("file", requires=IS_NOT_EMPTY(), comment=T("filename.ext")))

    if form.accepts(request.vars, session):
        with open(os.path.join(request.vars.folder, request.vars.file)) as the_file:
            db.import_from_csv_file(the_file)
            return dict(form=None, message=T("The db records were uploaded correctly"))
    elif form.errors:
        response.flash = T("The db load failed with these errors: ") + str(form.errors)
    return dict(form=form)


def convert_negative_or_zero_ids():
    """ Transfer record data with id less or equal to zero to a new db record """

    response.generic_patterns = ["*"]

    record_count = 0
    for table in db.tables:
        db_table = db[table]
        if (table + "_id") in db_table.fields:
            for record in db(db_table.id > -10000).select():
                if int(record["%s_id" % table]) <= 0:
                    new_record_id = None
                    tmp_dict = dict()
                    for k, v in record.iteritems():
                        if k in db_table.fields:
                            if not k.startswith("_"):
                                if not k == "id":
                                    if not k == (table + "_id"):
                                        tmp_dict[k] = v
                    if len(tmp_dict) > 0:
                        # avoid unique code constraint
                        if "code" in db_table.fields:
                            tmp_code = record["code"]
                            record.update_record(code = None)

                        new_record_id = db[table].insert(**tmp_dict)
                        print T("Moving to new record"), new_record_id, T("from table"), table, T("with old record"), record["%s_id" % table]
                        if new_record_id > 0:
                            # record.delete_record()
                            pass
                        record_count += 1

    return dict(total_records_moved = record_count)

def auto_id_code_fields():
    # convert code field values to table_id value
    response.generic_patterns = ["*"]
    
    import random

    random_values = set()
    for x in range(2000):
        v = random_values.add("-%s%s%s%s%s" % tuple([int(random.random()*10) for y in range(5)]))

    x = 0
    for table in db.tables:
        db_table = db[table]
        if ("%s_id" % table) in db_table.fields:
            if "code" in db_table.fields:
                for record in db(db_table).select():
                    try:
                        record.update_record(code = record["%s_id" % table])
                        x += 1
                    except Exception:
                        try:
                            tmp_random = random_values.pop()
                            print T("Could not change"), T("record"), record["%s_id" % table], "in", table
                            print T("Trying with"), str(record["%s_id" % table]) + tmp_random
                            record.update_record(code = str(record["%s_id" % table]) + tmp_random)
                        except Exception:
                            print T("Could not change"), T("record"), record["%s_id" % table], "in", table
                            print str(e)

    return dict(message=T("All tables modified"), modified_count = x)
