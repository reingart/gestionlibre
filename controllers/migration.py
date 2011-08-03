# -*- coding: utf-8 -*-

# intente algo como

import os, csv

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
        for n, table_record in enumerate(spam_reader):
            if n>0:
                tmpdict = dict()
                try:
                    for v in fields:
                        if not ((table_record[v[1]] == '') or (table_record[v[1]] is None)):
                            tmpdict[v[0]] = table_record[v[1]].strip()
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
    form = FORM(LABEL("CSV file name", _for="#csvinputfile"), INPUT(_id="csvinputfile", _type="text", _name="csvinputfile"), INPUT(_type="submit"))
    if form.accepts(request.vars, session):
        legacytables = importcsvpattern(os.path.join(PRIVATE_ROUTE, request.vars["csvinputfile"]))
        result = populate_with_legacy_db(LEGACY_TABLES_ROUTE, legacytables)
        return dict(records = result[0], errors = result[1], voidstrings = result[2], form = form)
    return dict(records = "", errors = "", voidstrings = "", form = form)

# propietary firm database fieldname transfer
# TODO: Store at firm's own archive space
def convertglagodict():
    glago = local_import("glago")
    glago.dict_to_csv(glago.LEGACY_TABLES)
    return dict(ok="Conversion finished")

# Old database field conversion pattern (from csv to dict)
# Input csv file: a list of records in the following syntax:
# tablearchive.csv, db_table_name, db_field_name, csv_record_field_index
def importcsvpattern(path):
    csvfilename = ""
    tmpdict = {}
    spam_reader = csv.reader(open(path, "rb"))
    for line in spam_reader:
        # check table change
        if line[0] != csvfilename:
            tmpdict[line[0]] = dict(table_name = line[1].strip(), fields = [(line[2].strip(), int(line[3])),])
        else:
            tmpdict[line[0]]["fields"].append((line[2].strip(), int(line[3])))
        csvfilename = line[0]
    return tmpdict
