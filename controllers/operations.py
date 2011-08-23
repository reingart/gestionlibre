# coding: utf8
# intente algo como

import datetime

# process operation
def process(operation_id):
    # TODO: move this code to a special module
    
    # error list for web client feedback
    errors = []
    
    # process operation and movements
    # return True if successful
        
    # get the operation record
    operation = db.operation[operation_id]
    
    # the document must be countable
    document = operation.document_id
    if not document.countable:
        return False
    
    # check if already processed
    if operation.processed:
        return False
    
    # get the last journal entry
    # TODO: precise j.e. selection/creation
    journal_entry = db(db.journal_entry).select().last()
    
    # movements loop (process entries)
    entries = 0
    for mov in db(db.movement.operation_id == operation_id).select():
        # check if entry or exit and change the records amount with correct sign
        concept = mov.concept_id
        amount = None
        if concept.entry:
            amount = mov.amount
        elif concept.exit:
            amount = -(mov.amount)
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
        
    # no process made
    return False


@auth.requires_login()
def index():
    """ Staff on-line panel. Show info/stats/links to actions"""

    now = datetime.datetime.now()
    delta = datetime.timedelta(7)
    time_limit = now - delta

    q = db.operation.operation_id > 0
    preset = db(q)
    the_set = preset(db.operation.posted >= time_limit)

    """
    TODO: filter by order document type

    # list all document types with orders == True
    order_documents = db(db.document.orders == True).select()
    order_documents_list = [document.document_id for document in order_documents]
    # make a subset of operations with order documents
    customer_orders_subset = customer_orders_set & db()
    """
    # get operation rows
    operations = the_set.select()

    return dict(operations = operations, message="Administrative panel")

# base web interface for movements
# administration
@auth.requires_login()
def movements():
    # reset the current operation (sent client-side)
    reset_operation_form = FORM(INPUT(_type="submit", _value="Reset operation"))
    if reset_operation_form.accepts(request.vars, formname="reset_operation"):
        session.operation_id = None

    # get the current operation if stored in session
    operation_id = session.get("operation_id", None)
    
    # if the user started a new operation, or none was
    # specified, create one
    if ("new" in request.vars) or (operation_id is None):
        session.operation_id = operation_id = db.operation.insert(\
        user_id = auth.user_id)
    elif len(request.args) > 0:
        session.operation_id = operation_id = int(request.args[1])

    # standard operation update sqlform
    # TODO: operation change shouldn't be allowed if processed
    form = SQLFORM(db.operation, operation_id, _id="operation_form")
    if form.accepts(request.vars):
        response.flash = "Form accepted"
    
    # Process operation for accounting/other when accepted
    process_operation_form = FORM(INPUT(_value="Process", _type="submit"))
    
    if process_operation_form.accepts(request.vars, formname="process_operation"):
        # TODO: incomplete
        # do not expose if operation was already processed
        # process/validate the operation
        if process(operation_id):
            response.flash = "Operation processed"
        else:
            response.flash = "Could not process the operation"
    
    return dict(message="Operation number %s" % operation_id, form = form, \
    reset_operation_form = reset_operation_form, process_operation_form = process_operation_form)
    
def movements_element():
    """ Insert sub-form for concept selection at movements form"""
    if not "operation_id" in session.keys():
        raise HTTP(500, "Operation not found.")
    form = SQLFORM(db.movement, fields=["code","description",
"concept_id", "price_id", "quantity", "amount", "discriminated_id", \
"table_number", "detail", "value", "posted", "discount", "surcharge", \
"replica"], _id="movements_element_form")
    form.vars.operation_id = session.operation_id
    
    if form.accepts(request.vars, session, keepvalues=True):
        response.flash = "Form accepted"
    elif form.errors:
        response.flash = "The form has errors"
        
    # query for operation movements
    movements_list = db(db.movement.operation_id == session.operation_id).select()
    
    return dict(form=form, movements_list = movements_list)

def movements_modify_element():
    """ Movements element edition sub-form."""
    movements_element = request.args[1]
    form = SQLFORM(db.movement, movements_element, \
    _id="movements_modify_element_form")
    if form.accepts(request.vars, session):
        response.flash = "Form accepted"
        redirect(URL(f="movements"))
    return dict(form=form)

# create intallment/quotas for current operation
def operation_installment():
    total = 0
    installment = None
    # get session operation
    operation = db.operation[session.operation_id]

    # calculate operation total payment
    movements = db(db.movement.operation_id == operation.operation_id).select()
    for mov in movements:
        try:
            total += float(mov.value) * float(mov.quantity)
        except (ValueError, TypeError):
            # TODO: adding error warning/andling
            pass

    # installment creation form
    form = SQLFORM.factory(Field('quotas', 'integer'), \
    Field('fee_id', 'integer', requires=IS_IN_DB(db, db.fee)))
    if form.accepts(request.vars, session):
        # create installment and fixed quotas
        # TODO: custom quota fields
        session.installment_id = installment_id = db.installment.insert(\
        customer_id = operation.customer_id, subcustomer_id = operation.subcustomer_id, \
        supplier_id = operation.supplier_id, fee_id = request.vars.fee_id)
        
        # quota amount = total / quotas
        quota_amount = total / int(request.vars.quotas)
        quotas_list = list()
        for x in range(int(request.vars.quotas)):
            quotas_list.append(db.quota.insert(installment_id = installment_id, \
            fee_id = request.vars.fee_id, number = x+1, amount = quota_amount))

        installment = db.installment[installment_id]
        installment.update(quotas = len(quotas_list), \
        monthly_amount = quota_amount, starting_quota_id = quotas_list[0], \
        ending_quota_id = quotas_list[len(quotas_list) -1])
        response.flash = "Installment created"

    return dict(total = total, form = form, installment = installment)
