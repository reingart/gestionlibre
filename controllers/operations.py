# coding: utf8
# intente algo como

import datetime

operations = local_import("operations")

# list of orderable concepts
# returns a dict with value, name pairs for
# IS_IN_SET validator
def orderable_concepts(limit_by = None):
    the_dict = dict()
    rows = db(db.concept.internal == False).select()
    for n, row in enumerate(rows):
        if (n < limit_by) or (limit_by is None):
            the_dict[row.concept_id] = row.description
        else:
            break
    return the_dict


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
def ria_movements():
    # reset the current operation (sent client-side)
    reset_operation_form = FORM(INPUT(_type="submit", _value="Reset operation"))
    if reset_operation_form.accepts(request.vars, formname="reset_operation"):
        session.operation_id = None

    # get the current operation if stored in session
    operation_id = session.get("operation_id", None)

    # Get the operation id requested
    # (assuming that an operation was specified)
    if len(request.args) > 0:
        session.operation_id = operation_id = int(request.args[1])
    
    # Otherwise, if the user started a new operation, or none was
    # specified, create one
    elif ("new" in request.vars) or (operation_id is None):
        session.operation_id = operation_id = db.operation.insert(\
        user_id = auth.user_id)

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
        if operations.process(db, session, operation_id):
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
            # TODO: add error warning/handling
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


@auth.requires_login()
def ria_new_customer_order():
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

            q = (db.movement.posted >= oldest) & (db.movement.concept_id == concept)
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
    columns = ["operation.operation_id", "operation.code", \
    "operation.description", "operation.posted"]
    headers={"operation.operation_id": "Edit", "operation.code":"Code", \
    "operation.description": "Description", "operation.posted": "Posted"}
    order_allocations = SQLTABLE(db(q).select(), columns = columns, \
    headers = headers, \
    linkto=URL(c="operations", f="update_order_allocation"))
    return dict(order_allocations = order_allocations)

def update_order_allocation():
    order_allocation = crud.update(db.operation, request.args[1])
    movements = SQLTABLE(db(\
    db.movement.operation_id == request.args[1]).select(), \
    columns=["movement.movement_id", "movement.code","movement.concept_id", \
    "movement.quantity"], headers={"movement.movement_id": \
    "ID", "movement.code": "Code", \
    "movement.concept_id": "Concept", "movement.quantity": "Quantity"}, \
    linkto=URL(c="operations", f="movements_modify_element"))
    return dict(order_allocation = order_allocation, movements = movements)


def packing_slip():
    """Create a packing slip from order allocation
    operation.
    """
    packing_slip_id = None
    document_id = db(db.document.packing_slips == True).select(\
        ).first().document_id

    if len(request.args) > 0:
        order_allocation_id = request.args[1]
        order_allocation = db.operation[order_allocation_id]
        # copy the allocation data to the new packing slip
        # TODO: user/configuration document selection
        # and custom packing slip source and items

        packing_slip_id = db.operation.insert(\
        customer_id = order_allocation.customer_id, \
        document_id = document_id)
        # TODO: fill packing slip with allocation movements
        for m in db(db.movement.operation_id == order_allocation_id).select():
            db.movement.insert(operation_id = packing_slip_id, \
            quantity = m.quantity, \
            value = m.value, concept_id = m.concept_id)

        packing_slip_form = crud.update(db.operation, packing_slip_id)
        order_allocation.update_record(processed = True)

    else:
        packing_slip_form = crud.create(db.operation)
        packing_slip_form.vars.document_id = document_id

    if packing_slip_form.accepts(request.vars, session):
        # web2py stores the created record id as "id"
        # instead of using the table field definition
        packing_slip_id = packing_slip_form.vars.id
        packing_slip_form = crud.update(db.operation, packing_slip_id)

    movements = SQLTABLE(db(\
    db.movement.operation_id == packing_slip_id).select(), \
    columns=["movement.movement_id", "movement.code","movement.concept_id", \
    "movement.quantity"], headers={"movement.movement_id": "ID", \
    "movement.code": "Code", \
    "movement.concept_id": "Concept", "movement.quantity": "Quantity"})

    return dict(packing_slip_form = packing_slip_form, \
    movements = movements, packing_slip_id = packing_slip_id)

def ria_receipt():
    """    Get or create a new receipt.
    Presents a one-view multi-form receipt
    for customer payments
    """
    operation_id = session.get("operation_id", None)

    # allow receipt reset
    reset_receipt_form = FORM(INPUT(_type="submit", _value="Reset receipt"))
    if reset_receipt_form.accepts(request.vars, \
    formname="reset_receipt_form"):
        operation_id = session.operation_id = None

    # get the session receipt or create one
    if operation_id is None:
        # new receipt
        # TODO: user/configuration selected receipt document
        document = db(db.document.receipts == True).select().first()
        operation_id = session.operation_id = db.operation.insert(\
        document_id = document)

    operation = db.operation[session.operation_id]
    document = db.document[operation.document_id]

    process_receipt_form = FORM(INPUT(_value="Process receipt", \
    _type="submit"))

    if process_receipt_form.accepts(request.vars, formname = "process_receipt_form"):
        # TODO: receipt processing
        # Balance movements
        # Call common operation process
        # Check as processed or return errors
        if operations.process(db, session, operation_id):
            operation.update_record(processed = True)
            response.flash="Receipt processed"
        else:
            response.flash="Could not process the receipt"

    receipt_form = crud.update(db.operation, operation_id)
    if receipt_form.accepts(request.vars, \
    formname="receipt_form"):
        response.flash="Form accepted"

    if (document is None) or (document.receipts != True):
        # return error
        response.flash="Warning! Wrong document type."

    return dict(receipt_form = receipt_form, \
    process_receipt_form = process_receipt_form, \
    reset_receipt_form = reset_receipt_form)

def receipt_checks():
    operation_id = session.operation_id
    check_form = crud.create(db.bank_check)
    if check_form.accepts(request.vars, session):
        # create a movement for the current account entry
        # TODO: form/config sourced current account record option

        # check concept
        check_concept = db((db.concept.banks == True) \
        & (db.concept.entry == True)).select().first()

        db.movement.insert(operation_id = operation_id, \
        concept_id = check_concept.concept_id, value = request.vars.amount, \
        amount = request.vars.amount)

        # current account concept
        current_account_concept = db((db.concept.current_account == True) \
        & (db.concept.exit == True)).select().first()

        db.movement.insert(operation_id = operation_id, \
        concept_id = current_account_concept.concept_id, value = request.vars.amount, \
        amount = request.vars.amount)

        response.flash = "Item added"

    check_form.vars.operation_id = operation_id

    columns = ["bank_ckeck.bank_check_id", "bank_check.number", \
    "bank_check.customer_id", \
    "bank_check.code", "bank_check.description", "bank_check.amount"]
    headers = {"bank_ckeck.bank_check_id": "Edit", \
    "bank_check.number": "Number", "bank_check.customer_id": "Customer", \
    "bank_check.code": "Code", "bank_check.description": "Description", \
    "bank_check.amount": "Amount"}

    checks_list = SQLTABLE(db(\
    db.bank_check.operation_id == operation_id).select(), \
    columns = columns, headers = headers)

    return dict(check_form = check_form, checks_list = checks_list)

def receipt_items():
    """ Cash or inter bank account payments """
    receipt_item_form = crud.create(db.movement, \
    formname="receipt_item_form")
    operation_id = session.operation_id
    # TODO: auto complete movemens with payment data
    # and filter the rest of concepts stored in db

    if receipt_item_form.accepts(request.vars, session):
        # create a movement for the current account entry
        # TODO: form/config sourced current account record option
        concept = db((db.concept.current_account == True) & \
        (db.concept.exit == True)).select().first()
        db.movement.insert(operation_id = operation_id, \
        concept_id = concept.concept_id, value = request.vars.value, \
        amount = request.vars.amount)
        response.flash = "Item added"

    columns = ["movement.movement_id", "movement.code", \
    "movement.description", \
    "movement.posted", "movement.amount", "movement.concept_id"]
    headers = {"movement.movement_id": "Edit", "movement.code": "Code", \
    "movement.description": "Description", "movement.posted": "Posted", \
    "movement.amount": "Amount", "movement.concept_id": "Concept"}

    receipt_item_form.vars.operation_id = session.operation_id
    receipt_items_list = SQLTABLE(db(\
    db.movement.operation_id == session.operation_id).select(), \
    columns = columns, headers = headers, linkto=URL(c="operations", \
    f="movements_modify_element"))
    return dict(receipt_item_form = receipt_item_form, \
    receipt_items_list = receipt_items_list)

def list_receipts():
    q = (db.operation.document_id == db.document.document_id) & \
    (db.document.receipts == True)
    columns = ["operation.operation_id", "operation.code", \
    "operation.description", "document.description", \
    "operation.posted"]
    headers = {"operation.operation_id": "Edit", \
    "operation.code": "Code", "operation.description": "Description", \
    "document.description": "Document", \
    "operation.posted": "Posted"}

    receipts = SQLTABLE(db(q).select(), columns = columns, \
    headers = headers, linkto=URL(c="operations", f="movements"))
    return dict(receipts = receipts)

def ria_product_billing():
    """ Presents a packing slips list for billing
    and collects billing details. Creates an invoice
    and redirects the action to the movements update form.
    """
    packing_slips = list()
    packing_slips_rows = list()
    checked_list = list()
    document_id = None
    customer_id = session.get("customer_id", None)
    subcustomer_id = session.get("subcustomer_id", None)

    # form to filter packing slips  by customer
    customer_form = SQLFORM.factory(Field('customer_id', \
    'reference customer', requires = IS_IN_DB(db, db.customer, "%(legal_name)s")), \
    Field('subcustomer_id', 'reference subcustomer', \
    requires = IS_IN_DB(db, db.subcustomer, "%(legal_name)s")))
    if customer_form.accepts(request.vars, session, keepvalues=True, formname="customer_form"):
        q = (db.operation.customer_id == request.vars.customer_id) | (db.operation.subcustomer_id == request.vars.subcustomer_id)
        q &= db.operation.processed != True
        q &= db.operation.document_id == db.document.document_id
        q &= db.document.packing_slips == True
        packing_slips = db(q).select()
        customer_id = session.customer_id = request.vars.customer_id
        subcustomer_id = session.subcustomer_id = request.vars.subcustomer_id

    # create packing slips table for selection
    # and the actual billing form
    # TODO: present new eyecandy third party widgets for multiselect box
    for row in packing_slips:
        packing_slips_rows.append(TR(TD(row.operation.operation_id), \
        TD(row.operation.posted), \
        TD(row.operation.code), TD(row.operation.description), \
        INPUT(_type="checkbox", \
        _name="operation_%s" % row.operation.operation_id)))

    documents = db(db.document.invoices == True).select()
    document_options = [OPTION(document.description, _value=document.document_id) for document in documents]

    billing_form = FORM(TABLE(THEAD(TR(TH("Operation"),TH("Posted"), \
    TH("Code"), TH("Description"), TH("Bill"))), \
    TBODY(*packing_slips_rows), \
    TFOOT(TR(TD(), TD(), TD(), TD(LABEL("Choose a document type", \
    _for="document_id"), SELECT(*document_options, _name="document_id")), \
    TD(INPUT(_value="Bill checked", _type="submit"))))))

    # operations marked for billing
    bill_items = []

    if billing_form.accepts(request.vars, session, \
    formname="billing_form"):
        for v in request.vars:
            if v.startswith("operation_"):
                bill_items.append(int(v.split("_")[1]))
        if len(bill_items) > 0:
            # create an invoice  with the collected data
            invoice_id = db.operation.insert(document_id = request.vars.document_id, \
            customer_id = customer_id, subcustomer_id =  subcustomer_id)
            # fill the invoice
            for packing_slip_id in bill_items:
                packing_slip_items = db(db.movement.operation_id == packing_slip_id).select()
                for movement in packing_slip_items:
                    db.movement.insert(operation_id = invoice_id, concept_id = movement.concept_id, \
                    amount = movement.amount, value = movement.value, quantity = movement.quantity)
                # check the packing slip as processed
                db.operation[packing_slip_id].update_record(processed = True)

            # TODO: insert ivoices payment / current account movements
            # set invoice as current operation
            session.operation_id = invoice_id
            # redirect to movements edition
            redirect(URL(c="operations", f="movements"))

    return dict(customer_form = customer_form, \
    billing_form = billing_form)


###############################################
#### Sequential operation processing (no ria) #
###############################################

def movements_start():
    """ Initial operation form """
    
    form = SQLFORM.factory(Field("type", \
    requires=IS_IN_SET({"T": "Stock", "S": \
    "Sales", "P": "Purchases"}), \
    comment="Select an operation type"), Field("description"))
    
    if form.accepts(request.vars, session):
        # new operation
        session.operation_id = db.operation.insert( \
        type=request.vars.type, \
        description = request.vars.description)
        redirect(URL(f="movements_header"))
    return dict(form = form)

    
def movements_header():
    """ Collect or modify operation basic data"""

    operation_id = session.operation_id
    operation = db.operation[operation_id]
    
    if operation.type == "S":
        fields = ["code", "description", "customer_id", "detail", "payment_terms_id", "term", "document_id", "branch", "due_date", "voided", "fund_id", "cost_center_id", "observations", "subcustomer_id", "salesperson_id", "jurisdiction_id"]
    elif operation.type == "T":
        fields = []
    elif opertaion.type == "P":
        fields = []
        
    form = SQLFORM(db.operation, operation_id, fields = fields)
    if form.accepts(request.vars, session):
        if operation.type == "S":
            redirect(URL(f="movements_price_list"))
        else:
            redirect(URL(f="movements_detail"))
        
    return dict(form = form, operation = operation)


def movements_price_list():
    form = SQLFORM.factory(Field("price_list", requires = IS_IN_DB(db(db.price_list), "price_list.price_list_id", "%(description)s")))
    if form.accepts(request.vars, session):
        session.price_list_id = request.vars.price_list
        redirect(URL(f="movements_detail"))
    return dict(form = form)


def movements_detail():
    """ List of operation items
    
    A user interface to manage movements
    """
    
    operation_id = session.operation_id
    operation = db.operation[operation_id]
    
    # { header:table, ... h:t} dictionary
    movements = dict()
    
    # Items (Products/Services/Discounts ...)
    q = db.movement.concept_id == db.concept.concept_id
    q &= db.concept.internal != True
    q &= db.movement.operation_id == operation_id
    
    s = db(q)
    columns = ["movement.movement_id", "movement.code", "movement.description", "movement.concept_id", "movement.quantity", "movement.value", "movement.amount"]
    headers = {"movement.movement_id": "Edit", "movement.code": "Code", "movement.description": "Description", "movement.concept_id": "Concept", "movement.quantity": "Quantity", "movement.value": "Value", "movement.amount": "Amount"}
    
    rows = s.select()
    movements["items"] = SQLTABLE(rows, columns = columns, headers = headers)
   
    # Payments
    q = db.movement.concept_id == db.concept.concept_id
    q &= db.concept.banks != True
    q &= db.concept.payment_method == True
    q &= db.movement.operation_id == operation_id
    
    s = db(q)
    
    rows = s.select()
    movements["payments"] = SQLTABLE(rows, columns = columns, headers = headers)

    # Checks
    q = db.movement.concept_id == db.concept.concept_id
    q &= db.concept.banks == True
    q &= db.movement.operation_id == operation_id
    
    s = db(q)

    rows = s.select()
    movements["checks"] = SQLTABLE(rows, columns = columns, headers = headers)
    
    # Taxes
    q = db.movement.concept_id == db.concept.concept_id
    q &= db.concept.tax == True
    q &= db.movement.operation_id == operation_id
    s = db(q)
    
    rows = s.select()
    movements["taxes"] = SQLTABLE(rows, columns = columns, headers = headers)
    
    return dict(operation = operation, movements = movements)


def movements_add_item():
    """ Ads an item movement to the operation. """
    
    operation_id = session.operation_id
    operation = db.operation[operation_id]
    document = db.document[operation.document_id]

    price_list_id = session.get("price_list_id", None)
    
    if price_list_id is not None:
        price_list = db.price_list[price_list_id]
    else:
        price_list = None
        
    form = SQLFORM.factory(Field("item", \
    requires=IS_IN_DB(db(db.concept.internal != True), \
    "concept.concept_id", "%(description)s")), \
    Field("quantity", requires = IS_FLOAT_IN_RANGE(-1e6, 1e6)))

    if form.accepts(request.vars, session):
        # Get the concept record
        concept = db.concept[request.vars.item]
        concept_id = concept.concept_id
        quantity = float(request.vars.quantity)
        
        # Calculate price, value, quantity, amount
        if price_list is not None:
            price = db((db.price.price_list_id == price_list_id \
            ) & (db.price.concept_id == concept_id)).select().first()
            value = price.value
            amount = value * quantity

        # Create the new operation item
        db.movement.insert(operation_id = operation_id, \
        amount = amount, value = value, concept_id = concept_id, \
        quantity = quantity)
        
        # Update tax data
        tax_items = movements_taxes(operation_id)
        redirect(URL(f="movements_detail"))

    return dict(form = form)


def movements_taxes(operation_id):
    """ Performs tax operations for the given operation """
    
    # TODO: clean zero amount tax items
    # WARNING: ¿db.table[0] returns None?
    
    operation = db.operation[operation_id]
    document = db.document[operation.document_id]
    # number of tax items
    items = 0
    taxes = dict()
    data = list()
    for movement in db(db.movement.operation_id == operation_id).select():
        # Compute the tax values if required
        concept = db(db.concept.concept_id == movement.concept_id).select().first()
        amount = movement.amount
        if (concept is not None) and (concept.taxed):
            tax = db.concept[concept.tax_id]
            tax_amount = (float(amount) * float(tax.amount)) - float(amount)
            try:
                taxes[tax.concept_id] += tax_amount
            except KeyError:
                taxes[tax.concept_id] = tax_amount
                
            if not document.discriminate:
                # add to item amount if not discriminated            
                movement.amount += tax_amount
                movement.value = movement.value * tax.amount

    for tax_concept_id in taxes:
        tax = db.concept[tax_concept_id]
        # Get and increase or create tax item
        if document.discriminate:
            tax_record = db(( \
            db.movement.concept_id == tax_concept_id) & ( \
            db.movement.operation_id == operation_id \
            )).select().first()
        
            if tax_record is None:
                tax_record_id = db.movement.insert( \
                operation_id = operation_id, \
                value = taxes[tax_concept_id], amount = taxes[tax_concept_id], \
                concept_id = tax_concept_id)
                tax_record = db.movement[tax_record_id]
            else:
                tax_record.amount = taxes[tax_concept_id]
                tax_record.value = taxes[tax_concept_id]
    items = len(taxes)
    return items
