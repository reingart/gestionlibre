# coding: utf8
# intente algo como
def index(): return dict(message="hello from accounting.py")


def journal_entries():
    journal_entries = SQLTABLE(db(db.journal_entry).select(), \
    linkto=URL(c="accounting", f="journal_entry"), \
    columns=["journal_entry.journal_entry_id", "journal_entry.code", \
    "journal_entry.description", "journal_entry.number", \
    "journal_entry.posted", "journal_entry.accounting_period_id"], \
    headers={"journal_entry.journal_entry_id": "Edit", "journal_entry.code": "Code", \
    "journal_entry.description": "Description", "journal_entry.number": "Number", \
    "journal_entry.posted": "Posted", "journal_entry.accounting_period_id": "Period"})
    return dict(journal_entries = journal_entries)

    
def journal_entry():
    # j.e. sum
    # TODO: detect unallowed entries (like None values)
    total = 0
    for e in db(db.entry.journal_entry_id == request.args[1]).select():
        if e.amount: total += float(e.amount)
    journal_entry_id = request.args[1]
    journal_entry = crud.read(db.journal_entry, journal_entry_id)
    entries = SQLTABLE(db(\
    db.entry.journal_entry_id == journal_entry_id).select(), \
    linkto=URL(c="accounting", f="entry"), \
    columns=["entry.entry_id", "entry.code", \
    "entry.description", "entry.journal_entry_id", \
    "entry.account_id", "entry.amount"], \
    headers={"entry.entry_id": "Edit", "entry.code": "Code", \
    "entry.description": "Description", \
    "entry.journal_entry_id": "Journal Entry", \
    "entry.account_id": "Account", "entry.amount": "Amount"})
    return dict(journal_entry = journal_entry, entries = entries, \
    total = total)

    
def entry():
    entry = crud.update(db.entry, request.args[1])
    return dict(entry = entry)


def offset_accounts():
    """ List of offset accounts """
    rows = db(db.option).select()
    offset_account_list = []
    for r in rows:
        if "offset_account" in r.name:
            # add option to list
            offset_account_list.append(r)
    return dict(offset_account_list = offset_account_list)


def offset_account():
    """ Create or modify an offset account option
    
    Get the form values or action args for option
    selection and modify or create the parameters.
    """
    
    option = None
    fields_values = {"account": None, "document": None, \
    "offset": None, "payment_terms": None}
    if len(request.args) >= 2:
        option = db.option[request.args[1]]
        # option kind - values separation -> values
        tmp_str = option.name.split("____")[1]
        # k, v pairs separation -> list
        tmp_str_2 = tmp_str.split("___")
        for k__v in tmp_str_2:
            # Get the k, v pair stored as k__v string
            tmp_str_3 = k__v.split("__")
            fields_values[tmp_str_3[0]] = int(tmp_str_3[1])
            # Get the offset account stored value
            fields_values["offset"] = int(option.value)
            
    offset_form = SQLFORM.factory(
    Field("account", requires=IS_IN_DB(db(db.account), \
    "account.account_id", "%(description)s")), \
    Field("document", requires=IS_IN_DB(db(db.document), \
    "document.document_id", "%(description)s")), \
    Field("payment_terms", requires=IS_IN_DB(db(db.payment_terms), \
    "payment_terms.payment_terms_id", "%(description)s")), \
    Field("offset", requires=IS_IN_DB(db(db.account), \
    "account.account_id", "%(description)s")))

    for k, v in fields_values.iteritems():
        offset_form.vars[k] = v
    
    if offset_form.accepts(request.vars, session, \
    keepvalues = True, formname="offset_form"):
        # retrieve the db record
        tmp_text_value = "offset_account____"
        
        # complete the compound option name field
        for k in request.vars:
            if (not k=="offset") and (not k.startswith("_")):
                tmp_text_value += k + "__" + str(request.vars[k]) + "___"
        if len(request.vars) > 1:
            tmp_text_value = tmp_text_value[:-3]
            
        # Get option record with the compound name value
        option = db(db.option.name == tmp_text_value).select().first()
            
        # the offset account
        offset_id = int(request.vars["offset"])
        
        # create record if empty or modify current
        if option is None:
            db.option.insert(name = tmp_text_value, \
            value = offset_id)
            response.flash = "New option created."
        else:
            option.update_record(name = tmp_text_value, value = offset_id)
            response.flash = "Option modified."
    
    return dict(offset_form = offset_form)
