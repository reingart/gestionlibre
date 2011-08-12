# coding: utf8
# intente algo como

import datetime

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
    if reset_operation_form.accepts(request.vars, session):
        session.operation_id = None

    # get the current operation if stored in session
    operation_id = session.get("operation_id", None)
    
    # if the user started a new operation, or none was
    # specified, create one
    if ("new" in request.vars) or (operation_id is None):
        session.operation_id = operation_id = db.operation.insert(user_id = auth.user_id)
    elif len(request.args) > 0:
        session.operation_id = operation_id = int(request.args[1])

    # standard operation update sqlform
    form = SQLFORM(db.operation, operation_id, _id="operation_form")
    if form.accepts(request.vars, session):
        response.flash = "Form accepted"
    
    return dict(message="Operation number %s" % operation_id, form = form, reset_operation_form = reset_operation_form)
    
def movements_element():
    """ Insert sub-form for concept selection at movements form"""
    if not "operation_id" in session.keys():
        raise HTTP(500, "Operation not found.")
    form = SQLFORM(db.movement, fields=["code","description",
"concept_id", "price_id", "quantity", "amount", "discriminated_id", "table_number", "detail", "value", "posted", "discount", "surcharge", "replica"], _id="movements_element_form")
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
    if not "operation_id" in session.keys():
        raise HTTP(500, "Operation not found.")
    movements_element = request.args[1]
    form = SQLFORM(db.movement, movements_element, _id="movements_modify_element_form")
    if form.accepts(request.vars, session):
        response.flash = "Form accepted"
        redirect(URL(f="movements"))
    return dict(form=form)
