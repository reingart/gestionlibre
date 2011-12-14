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
                    db.debugging.insert(msg=T("Populate_with_legacy_db Insert Error: Table %(table)s, row %(n)s: %(e)s") % dict(table=table, n=str(n), e=str(e)))
                    errors += 1
    return records, errors, voidstrings

def index(): return dict(message="hello from migration.py")

# Get legacy database records and insert them in the app's db
def import_csv_dir():
    db(db.debugging.id > 0).delete()
    error_list=None
    form = SQLFORM.factory(
                Field("csv_input_file", requires=IS_NOT_EMPTY(), comment=T("CSV parameters file: /absolute/path/file_name.csv")),
                Field("csv_folder", requires=IS_NOT_EMPTY(), comment=T("CSV table files path: /absolute/path/tables_folder")),
                )
    if form.accepts(request.vars, session):
        legacy_tables = import_csv_pattern(request.vars.csv_input_file)
        result = populate_with_legacy_db(request.vars.csv_folder, legacy_tables)
        error_list = db(db.debugging).select()
        return dict(records = result[0], errors = result[1], voidstrings = result[2], form = form, error_list = error_list)
    return dict(records = "", errors = "", voidstrings = "", form = form, error_list = error_list)

# Old database field conversion pattern (from csv to dict)
# Input csv file: a list of records in the following syntax:
# tablearchive.csv, db_table_name, db_field_name, csv_record_field_index,
# data type (web2py dal), default value
def import_csv_pattern(path):
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

# show app tables
def tables():
    return dict(tables = str(db.tables))
    