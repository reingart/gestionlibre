#!/usr/bin/env python
# coding: utf8
from gluon import *
import datetime

# operation processing

# process operation (for accounting)
def process(db, session, operation_id):
    # TODO: validate operation
    # with movements inspection and
    # user / customer parameters

    # invert entry values (1 or -1)
    invert = 1
    
    # error list for web client feedback
    session.process_errors = []
    
    # process operation and movements
    # return True if successful
        
    # get the operation record
    operation = db.operation[operation_id]
    
    # the document must be countable
    document = operation.document_id
    if not document.countable:
        return False
        
    # Get the document inversion property
    if document.invert == True: invert = -1
    
    # check if already processed
    if operation.processed:
        return False
    
    # get the last journal entry
    # or create one
    # TODO: precise j.e. selection/creation
    journal_entry = db(db.journal_entry).select().last()
    # check if journal entry is valid
    # TODO: Do standard entry validation
    # according to local regulations
    # and return error code/messages
    today = datetime.date.today()
    if (journal_entry is None) or (not ((\
    journal_entry.posted.year == today.year) and \
    (journal_entry.posted.month == today.month) and \
    (journal_entry.posted.day == today.day))):
        journal_entry_id = db.journal_entry.insert(\
        accounting_period_id = db(\
        db.accounting_period).select().last(), \
        description="%s entry" % str(today))
        journal_entry = db.journal_entry[journal_entry_id]

    # movements loop (process entries)
    entries = 0

    for mov in db(db.movement.operation_id == operation_id\
    ).select():
        # check if entry or exit and change the records amount with correct sign
        concept = db(db.concept.concept_id == mov.concept_id).select().first()
        amount = None
        if concept.entry == True:
            amount = mov.amount*invert
        elif concept.exit == True:
            amount = -(mov.amount)*invert
        # insert entry record
        db.entry.insert(journal_entry_id = journal_entry, \
        account_id = concept.account_id, amount = amount)
        entries += 1

    # if all records were successfuly added
    # TODO: (and operation validates)
    if entries > 0:
        # check operation as processed
        # and exit
        operation.update_record(processed = True)
        return True

    # end of process        
    # no process made
    return False

