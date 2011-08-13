# -*- coding: utf-8 -*-
# intente algo como
import datetime

# list of orderable concepts
# returns a dict with value, name pairs for
# IS_IN_SET validator
def orderable_concepts(limit_by = None):
    the_dict = dict()
    rows = db(db.concept.orderable == True).select()
    for n, row in enumerate(rows):
        if (n < limit_by) or (limit_by is None):
            the_dict[row.concept_id] = row.description
        else:
            break
    return the_dict

@auth.requires_login()
def index():
    """ Customer on-line panel. Show info/stats/links to actions"""
    contact_user = db(db.contact_user.user_id == auth.user_id).select().first()
    if contact_user is None:
        return dict(customer_orders = None, message="No tax id selected", customer = None)
    try:
        contact = db(db.contact.contact_id == contact_user.contact_id).select().first()
    except KeyError:
        contact = None
    try:
        customer = db(db.customer.customer_id == contact.customer_id).select().first()
    except KeyError:
        customer = None
    
    now = datetime.datetime.now()
    delta = datetime.timedelta(7)
    time_limit = now - delta

    q = db.operation.document_id == db.document.document_id
    q &= db.document.orders == True
    preset = db(q)
    customer_orders_set = preset((db.operation.customer_id == customer) & (db.operation.posted >= time_limit))
    
    """
    TODO: filter by order document type

    # list all document types with orders == True
    order_documents = db(db.document.orders == True).select()
    order_documents_list = [document.document_id for document in order_documents]    
    # make a subset of operations with order documents
    customer_orders_subset = customer_orders_set & db()
    """
    # get operation rows
    customer_orders = customer_orders_set.select()

    return dict(customer_orders = customer_orders, message="Customer panel", customer = customer)

@auth.requires_login()
def new_customer_order():
    """ Customer's ordering on-line form.
    Note: get db objects with db(query).select()
    i.e. contact.customer returns the db record id """

    if len(request.args) > 0:
        session.operation_id = int(request.args[1])
    
    reset_order = FORM(INPUT(_type="submit", _value="Reset order"))
    if reset_order.accepts(request.vars, session):
        session.operation_id = None
    contact_user = db(db.contact_user.user_id == auth.user_id).select().first()
    
    # catch incomplete registrations (no contact user relations)
    if contact_user is None:
        return dict(form=None, reset = None, contact = None, customer = None, order = None, contact_user=None)
    try:
        contact = db(db.contact.contact_id == contact_user.contact_id).select().first()
    except KeyError:
        contact = None
    try:
        customer = db(db.customer.customer_id == contact.customer_id).select().first()
    except KeyError:
        customer = None

    # Look for allowed orders in options db
    customer_allowed_orders = db(db.option.name == "customer_allowed_orders").select().first()
    if customer_allowed_orders and  isinstance(customer_allowed_orders.value, basestring):
        allowed_orders_list = [int(o) for o in customer_allowed_orders.value.split("|") if len(o) > 0]
    else:
        allowed_orders_list = []
    # Get the default order
    default_order = db(db.option.name == "customer_default_order").select().first()
    if isinstance(default_order, basestring): default_order = int(default_order)

    # create a new order with pre-populated user data
    if not "operation_id" in session.keys():
        customer_order = db.operation.insert(customer_id = customer, document_id = default_order.value)
        session.operation_id = customer_order
    else:
        customer_order = session.operation_id
        if session.operation_id is None:
            customer_order = db.operation.insert(customer_id = customer, document_id = default_order.value)
            session.operation_id = customer_order

    form = SQLFORM(db.operation, customer_order, fields=["description"], _id="new_customer_order_form")

    # Available order documents
    order_documents = db(db.document.orders == True).select()
    checks = 0
    loop_count = 0
    check_list = list()
    order_options = dict()
                
    if form.accepts(request.vars, session):
        db.operation[customer_order].update_record(document_id = request.vars.order_type)
        response.flash = "Form accepted"

    for order_document in order_documents:
        loop_count += 1
        # check option if previously selected
        if db.operation[customer_order].document_id == order_document.document_id:
            checked = True
        elif order_document.document_id == default_order.value:
            checked = True
        else:
            checked = False
        if order_document.document_id in allowed_orders_list:
            order_options[order_document.document_id] = dict()
            order_options[order_document.document_id]["label"] = order_document.description
            order_options[order_document.document_id]["name"] = "order_type"
            order_options[order_document.document_id]["value"] = order_document.document_id
            if checked:
                order_options[order_document.document_id]["checked"] = True
                checked = False
            else:
                order_options[order_document.document_id]["checked"] = False

    return dict(form=form, reset = reset_order, contact = contact, customer = customer, order = db.operation[customer_order], contact_user = contact_user, order_options = order_options)

# order movement creation
def new_customer_order_element():
    """ Insert sub-form for product selection at Customer ordering form"""
    if not "operation_id" in session.keys():
        raise HTTP(500, "Customer order not found.")
    form = SQLFORM.factory(Field('concept_id', 'reference concept', requires=IS_IN_SET(orderable_concepts())), Field('description'), Field('quantity', 'double'), _id="new_customer_order_element_form")
    if form.accepts(request.vars, session):
        db.movement.insert(operation_id = session.operation_id, concept_id = request.vars.concept_id, description = request.vars.description, quantity = request.vars.quantity)
        response.flash = "Form accepted"
    order_list = db(db.movement.operation_id == session.operation_id).select()
    return dict(form=form, order_list = order_list)

# order movement modification
def new_customer_order_modify_element():
    """ Customer order element edition sub-form."""
    if not "operation_id" in session.keys():
        raise HTTP(500, "Customer order not found.")
    customer_order_element = db.movement[request.args[1]]
    
    form = SQLFORM.factory(Field('concept_id', 'reference concept', requires=IS_IN_SET(orderable_concepts()), default=customer_order_element.movement_id), Field('description', default=customer_order_element.description), Field('quantity', 'double', default = customer_order_element.quantity), _id="new_customer_order_modify_element_form")
    if form.accepts(request.vars, session):
        customer_order_element.update_record(description = request.vars.description, concept_id = request.vars.concept_id, quantity = request.vars.quantity)
        response.flash = "Form accepted"
        redirect(URL(f="new_customer_order"))
    return dict(form=form)

def new_customer():
    form = crud.create(db.customer)
    return dict(form = form)
    
def new_subcustomer():
    form = crud.create(db.subcustomer)
    return dict(form = form)
