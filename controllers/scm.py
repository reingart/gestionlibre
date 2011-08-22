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

def order_allocation():
    # Note: this is a draft for
    # Inventory/Order allocation
    # management and is not intended
    # as a complete and refined solution
    # for the matter. TODO: order allocation
    # algorithms implementation
    
    # the current algorithm
    # has not been tested
    # and may lead to stock inconsistencies
    
    # get movements from order operations
    # wich have unallocated items (unprocessed)

    q = db.movement.operation_id == db.operation.operation_id
    q &= db.operation.processed != True
    q &= db.operation.document_id == db.document.document_id
    q &= db.document.orders == True
    preset = db(q)
    order_movements = preset.select()
    
    # separate movements by customer and concept
    movements_stack = dict()
    pending_stack = dict()
    operations = set()
    for om in order_movements:
        try:
            qty = float(om.movement.quantity)
        except (ValueError, KeyError):
            qty = 0
        try:    
            concept = int(om.movement.concept_id)
            customer = int(om.operation.customer_id)
            operation = int(om.operation.operation_id)
            operations.add(operation)
        except KeyError:
            concept = customer = operation = None
        
        if customer in movements_stack:
            if concept in movements_stack[customer]:
                movements_stack[customer][\
                concept]["qty"] += qty
            else:
                movements_stack[customer][\
                concept] = dict(first = operation, \
                qty = qty, allocated = 0, pending = True, \
                stock = 0, allocate = 0.0)
        else:        
            movements_stack[customer] = dict()
            movements_stack[customer][concept] = dict(\
            first = operation, qty = qty, \
            allocated = 0, pending = True, stock = 0, allocate = 0.0)
    
    # compare order quantity and allocated qty
    # per order item (order allocation after order date)
    for customer in movements_stack:
        for concept in movements_stack[customer]:
            # get the item stock
            # TODO: manage user selected warehouses
            
            try:
                stock = db(\
                db.stock.concept_id == concept).select().first().value
                oldest = db.operation[movements_stack[\
                customer][concept]["first"]\
                ].posted
            except AttributeError:
                stock = oldest = None
            
            # update the stock value for the current customer/concept    
            movements_stack[customer][concept]["stock"] = stock            

            q = db.movement.posted >= oldest and db.movement.concept_id == concept
            q &= db.movement.operation_id == db.operation.operation_id
            q &= db.operation.document_id == db.document.document_id
            q &= db.document.books == True
            allocated_set = db(q)
            
            # set allocated amount
            try:
                movements_stack[customer][concept][\
                "allocated"] = sum(\
                [m.movement.quantity for m in allocated_set.select() \
                if m.movement.quantity is not None], 0.00)
            except KeyError:
                movements_stack[customer][concept][\
                "allocated"] = 0.00
            # if allocated is equal to ordered for any order movement
            # set item as completed
            if movements_stack[customer][concept]["qty"] <= \
            movements_stack[customer][concept]["allocated"]:
                movements_stack[customer][concept]["pending"] = False
    
    # present a form-row to allocate from inventory
    # based on available stock value.
    form_rows = []
    for customer, v in movements_stack.iteritems():
        for concept, w in v.iteritems():
            try:
                # getting the customer with dictionary syntax
                # throws a KeyError exception
                customer_desc = db(db.customer.customer_id == customer).select().first().description
            except (AttributeError, KeyError):
                customer_desc = customer
            try:
                concept_code = db.concept[str(concept)].code
                concept_desc = db.concept[str(concept)].description                
            except (AttributeError, KeyError):
                concept_code = concept_desc = concept
                
            form_rows.append(TR(TD(customer_desc), TD(concept_code), \
            TD(concept_desc), TD(w["qty"]), TD(w["allocated"]), \
            TD(w["stock"]), \
            INPUT(_name="order_allocation_%s_%s" % (customer, concept))))
            
    form = FORM(TABLE(THEAD(TR(TH("Customer"),TH("Product code"), \
    TH("Concept"), TH("Ordered"), TH("Allocated"), TH("Stock"), \
    TH("Allocate"))), TBODY(*form_rows), TFOOT(TR(TD(), TD(), TD(), \
    TD(), TD(), TD(), TD(INPUT(_value="Allocate orders", _type="submit"))))))
    
    # form processing:
    # classify allocated items by customer
    # for each customer allocation item group

    operations = set()
    
    if form.accepts(request.vars, session):
        for var in request.vars:
            if "order_allocation" in var:
                try:
                    concept = int(var.split("_")[3])
                    customer = int(var.split("_")[2])
                    movements_stack[customer][concept]["allocate"] = float(request.vars[var])
                except (ValueError, TypeError, KeyError):
                    customer = None
                    concept = None
       
        # create and populate the order allocation document
        for customer, v in movements_stack.iteritems():
            operation = None
            for concept, w in v.iteritems():
                if w["allocate"] > 0:
                    if operation is None:
                        # new operation
                        # TODO: order allocation document defined by user input/configuration
                        operation = db.operation.insert(customer_id = customer, document_id = db(db.document.books == True).select().first())
                    db.movement.insert(operation_id = operation, quantity = w["allocate"], concept_id = concept)
                    # reduce stock value
                    stock_item = db(db.stock.concept_id == concept).select().first()
                    stock_value = stock_item.value -w["allocate"]
                    stock_item.update_record(value = stock_value)
                    operations.add(operation)

    # return a list with allocations by item
    return dict(form = form, operations = operations)

def list_order_allocations():
    q = db.operation.processed == False
    q &= db.operation.document_id == db.document.document_id
    q &= db.document.books == True
    columns = ["operation.operation_id", "operation.code", "operation.description", "operation.posted"]
    order_allocations = SQLTABLE(db(q).select(), columns = columns, linkto=URL(c="scm", f="update_order_allocation"))
    
    return dict(order_allocations = order_allocations)
    
def update_order_allocation():
    order_allocation = crud.update(db.operation, request.args[1])
    return dict(order_allocation = order_allocation)

def packing_slip():
    order_allocation_id = request.args[1]
    order_allocation = db.operation[order_allocation_id]
    # copy the allocation data to the new packing slip
    # TODO: user/configuration document selection
    packing_slip_id = db.operation.insert(customer_id = order_allocation.customer_id, document_id = db(db.document.packing_slips == True).select().first().document_id)
    # TODO: fill packing slip with allocation movements
    return dict(packing_slip = crud.update(db.operation, packing_slip_id))
