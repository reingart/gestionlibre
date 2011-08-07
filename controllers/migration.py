# -*- coding: utf-8 -*-

# intente algo como

import os, csv, datetime

"""
Migration module for legacy databases
This is an experiment to transfer ms-access and other csv exportable sources to a DAL managed database
Input is a directory with one .csv file for each table (including a field name header)

Here is the transfering task. Map every field to the new database design structure

LEGACY_TABLES: dictionary with { [table_csv_file_name]: { "table_name": [new table name], fields: [ (fieldname, index or None), ... ] }, ... } structure

"""

LEGACY_TABLES = {}
LEGACY_TABLES_ROUTE = os.path.join("applications", request.application, "private", "legacy_tables")
PRIVATE_ROUTE = os.path.join("applications", request.application, "private")


# data parse for csv input
def parse_value(string_type, string_default, string_value):
    # TODO: handle value, attribute errors
    rt_value = None
    if string_type:
        if string_type == "integer":
            try:
                rt_value = int(string_value)
            except:
                try:
                    rt_value = int(string_default)
                except:
                    rt_value = None
        elif string_type == "double":
            try:
                rt_value = float(string_value)
            except:
                try:
                    rt_value = float(string_default)
                except:
                    rt_value = None
        elif string_type == "date":
            try:
                rt_value = datetime.date(int(string_value[:4]), int(string_value[5:7]), int(string_value[8:]))
            except:
                try:
                    rt_value = datetime.date(int(string_default[:4]), int(string_default[5:7]), int(string_default[8:]))
                except:
                    rt_value = None
        elif string_type == "string":
            try:
                rt_value = str(string_value)
                if len(rt_value) <= 0:
                    rt_value = None
            except:
                rt_value = None

        return rt_value
    else:
        return string_value




# insert database records using a dict pattern from csv tables
# csv tables must be stored in
# applications/application/private/legacy_tables

def populate_with_legacy_db(legacy_tables_route, legacy_tables):
    records = 0
    errors = 0
    voidstrings = 0
    for table_file_name, table_data in legacy_tables.iteritems():
        # open file with csv reader
        try:
            spam_reader = csv.reader(open(os.path.join(legacy_tables_route, table_file_name), 'rb'))
        except IOError:
            continue
        table = legacy_tables[table_file_name]["table_name"]
        fields = legacy_tables[table_file_name]["fields"]

        # delete table records
        db(db[table]).delete()
        db.commit()
        
        for n, table_record in enumerate(spam_reader):
            if n>0:
                tmpdict = dict()
                try:
                    for v in fields:
                        # v[2] is string data type (or '')
                        # v[3] is string default value (or '')
                        if not ((table_record[v[1]].strip() == '') or (table_record[v[1]] is None)):
                            # filter value
                            tmpdict[v[0].strip()] = parse_value(v[2], v[3], table_record[v[1]])
                        else:
                            voidstrings +=1

                    if len(tmpdict) > 1:
                        db[table].insert(**tmpdict)
                        records += 1 
                except Exception, e:
                    # TODO: catch common db exceptions
                    db.debugging.insert(msg="Populate_with_legacy_db Insert Error: Table %s, row %s: %s" % (table, str(n), str(e)))
                    errors += 1
    return records, errors, voidstrings

def index(): return dict(message="hello from migration.py")

# Get legacy database records and insert them in the app's db
def importcsvdir():
    db(db.debugging.id > 0).delete()
    error_list=None
    form = FORM(LABEL("CSV file name", _for="#csvinputfile"), INPUT(_id="csvinputfile", _type="text", _name="csvinputfile"), INPUT(_type="submit"))
    if form.accepts(request.vars, session):
        legacytables = importcsvpattern(os.path.join(PRIVATE_ROUTE, request.vars["csvinputfile"]))
        result = populate_with_legacy_db(LEGACY_TABLES_ROUTE, legacytables)
        error_list = db(db.debugging).select()
        return dict(records = result[0], errors = result[1], voidstrings = result[2], form = form, error_list = error_list)
    return dict(records = "", errors = "", voidstrings = "", form = form, error_list = error_list)

# propietary firm database fieldname transfer
# TODO: Store at firm's own archive space
# (not used)
def convertglagodict():
    glago = local_import("glago")
    glago.dict_to_csv(glago.LEGACY_TABLES)
    return dict(ok="Conversion finished")

# Old database field conversion pattern (from csv to dict)
# Input csv file: a list of records in the following syntax:
# tablearchive.csv, db_table_name, db_field_name, csv_record_field_index,
# data type (web2py dal), default value
def importcsvpattern(path):
    csvfilename = ""
    tmpdict = {}
    spam_reader = csv.reader(open(path, "rb"))
    for number, line in enumerate(spam_reader):
        # skip header
        if number <= 0:
            continue
        # check table change
        if line[0] != csvfilename:
             # 0: filename, 1: tablename , 2: field, 3: index value, 4 and 5 are type and default value
            tmpdict[line[0]] = dict(table_name = line[1].strip(), fields = [(line[2].strip(), int(line[3]), str(line[4]).strip(), str(line[5]).strip()),])
        else:
            tmpdict[line[0]]["fields"].append((line[2].strip(), int(line[3]), str(line[4]).strip(), str(line[5]).strip()))
        csvfilename = line[0]
    return tmpdict
