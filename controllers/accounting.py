# coding: utf8
# intente algo como
def index(): return dict(message="hello from accounting.py")

def journal_entries():
    journal_entries = SQLTABLE(db(db.journal_entry).select(), linkto=URL(c="accounting", f="journal_entry"))
    return dict(journal_entries = journal_entries)
    
def journal_entry():
    # j.e. sum
    # TODO: detect unallowed entries (like None values)
    total = 0
    for e in db(db.entry.journal_entry_id == request.args[1]).select():
        if e.amount: total += float(e.amount)
    journal_entry_id = request.args[1]
    journal_entry = crud.read(db.journal_entry, journal_entry_id)
    entries = SQLTABLE(db(db.entry.journal_entry_id == journal_entry_id).select(), linkto=URL(c="accounting", f="entry"))
    return dict(journal_entry = journal_entry, entries = entries, total = total)
    
def entry():
    entry = crud.update(db.entry, request.args[1])
    return dict(entry = entry)
