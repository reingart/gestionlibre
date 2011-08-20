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
