# -*- coding: utf-8 -*-
# intente algo como

@auth.requires_login()
def index():
    """ Customer on-line panel. Show info/stats/links to actions"""
    contactuser = db(db.contactuser.user == auth.user_id).select().first()
    if contactuser is None:
        return dict(customer_orders = None, message="No tin selected", customer = None)    
    try:
        contact = db(db.contact.id == contactuser.contact).select().first()
    except KeyError:
        contact = None
    try:
        customer = db(db.customer.id == contact.customer).select().first()
    except KeyError:
        customer = None
        
    customer_orders = db(db.customerorder.customer == customer.id).select()
    return dict(customer_orders = customer_orders, message="Customer panel", customer = customer)

@auth.requires_login()
def new_customer_order():
    """ Customer's ordering on-line form.
    Note: get db objects with db(query).select()
    i.e. contact.customer returns the db record id """
    reset_order = FORM(INPUT(_type="submit", _value="Reset order"))
    if reset_order.accepts(request.vars, session):
        session.customerorder = None
    contactuser = db(db.contactuser.user == auth.user_id).select().first()
    
    # catch incomplete registrations (no contact user relations)
    if contactuser is None:
        return dict(form=None, reset = None, contact = None, customer = None, order = None, contactuser=None)    
    try:
        contact = db(db.contact.id == contactuser.contact).select().first()
    except KeyError:
        contact = None
    try:
        customer = db(db.customer.id == contact.customer).select().first()
    except KeyError:
        customer = None

    # create a new order with pre-populated user data
    if not "customerorder" in session.keys():
        customerorder = db.customerorder.insert(customer = customer)
        session.customerorder = customerorder
    else:
        customerorder = session.customerorder    
        if session.customerorder is None:
            customerorder = db.customerorder.insert(customer = customer)
            session.customerorder = customerorder
        
    form = SQLFORM(db.customerorder, customerorder, fields=["description"], _id="new_customer_order_form")
    if form.accepts(request.vars, session):
        response.flash = "Form accepted"
    
    return dict(form=form, reset = reset_order, contact = contact, customer = customer, order = db.customerorder[customerorder], contactuser = contactuser)

def new_customer_order_elements():
    """ Insert sub-form for product selection at Customer ordering form"""
    if not "customerorder" in session.keys():
        raise HTTP(500, "Customer order not found.")
    form = SQLFORM(db.customerorderelement, fields=["description", "notes", "product", "quantity"], _id="new_customer_order_elements_form")
    form.vars.customerorder = session.customerorder
    if form.accepts(request.vars, session):
        response.flash = "Form accepted"
    orderlist = db(db.customerorderelement.customerorder == session.customerorder).select()
    return dict(form=form, orderlist = orderlist)

def new_customer_order_modify_elements():
    """ Customer order element edition sub-form."""
    if not "customerorder" in session.keys():
        raise HTTP(500, "Customer order not found.")
    customerorderelement = request.args[1]
    form = SQLFORM(db.customerorderelement, customerorderelement, fields=["description", "notes", "product", "quantity"], _id="new_customer_order_modify_elements_form")
    if form.accepts(request.vars, session):
        response.flash = "Form accepted"
        redirect(URL(f="new_customer_order"))
    return dict(form=form)
