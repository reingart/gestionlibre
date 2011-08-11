# coding: utf8
# intente algo como
def index(): return dict(message="hello from operations.py")

# base web interface for movements
# administration
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
