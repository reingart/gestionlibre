# -*- coding: utf-8 -*-
# intente algo como

import datetime

import operations
import crm


####################################################################
##   Auxiliar functions
####################################################################


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


def movements_taxes(operation_id):
    """ Performs tax operations for the given operation """

    # TODO: clean zero amount tax items,
    # Separate the movements values
    # processing in a function

    # WARNING: db.table[0] returns None

    operation = db.operation[operation_id]
    document = db.document[operation.document_id]
    # number of tax items
    items = 0
    taxes = dict()
    data = list()
    for movement in db(db.movement.operation_id == operation_id \
    ).select():
        # Compute the tax values if required
        concept = db(db.concept.concept_id == movement.concept_id \
        ).select().first()

        # Calculate movement amount without taxes
        try:
            amount = float(movement.value) * float(movement.quantity)
        except (TypeError, ValueError, AttributeError):
            amount = None

        if (concept is not None) and (concept.taxed):
            tax = db.concept[concept.tax_id]
            # None taxes can occur if a
            # concept is taxed but has no
            # tax concept as reference
            if (tax is not None) and (amount is not None):
                tax_amount = (float(amount) * float(tax.amount)) \
                - float(amount)
                try:
                    taxes[tax.concept_id] += tax_amount
                except KeyError:
                    taxes[tax.concept_id] = tax_amount

                if not document.discriminate:
                    # add to item amount if not discriminated
                    movement.update_record(amount = float( \
                    amount) + tax_amount)

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
                value = taxes[tax_concept_id], \
                amount = taxes[tax_concept_id], \
                concept_id = tax_concept_id, quantity = 1)
                tax_record = db.movement[tax_record_id]
            else:
                tax_record.update_record(amount = taxes[tax_concept_id], \
                value = taxes[tax_concept_id])
    items = len(taxes)
    return items


def movements_checks(operation_id):
    """ Movements check processing """
    # TODO: erease checks movement if amount is 0
    # TODO: return warnings/errors
    concept_id = None
    checks = db(db.bank_check.operation_id == operation_id).select()
    operation = db.operation[operation_id]
    document = db.document[operation.document_id]

    if operation.type == "S":
        concept_id = db(db.concept.code == db(\
        db.option.name == "sales_check_input_concept" \
        ).select().first().value).select().first().concept_id

    elif operation.type == "P":
        concept_id = db(db.concept.code == db( \
        db.option.name == "purchases_check_input_concept" \
        ).select().first().value).select().first().concept_id
        
    else:
        # Do not input checks if it is a stock operation
        return 0

    # get or create the movement
    if concept_id is not None:
        q = db.movement.operation_id == operation_id
        q &= db.movement.concept_id == concept_id
        s = db(q)

        if len(checks) > 0:
            checks_movement = s.select().first()
            if (checks_movement is None):
                checks_movement_id = db.movement.insert( \
                operation_id = operation_id, \
                concept_id = concept_id)

                # Get the new checks movement db record
                checks_movement = \
                db.movement[checks_movement_id]

            # Calculate the total amount and update the
            # checks movement
            checks_movement.update_record( \
            amount = sum([check.amount for check in checks]))

    else:
        # no concept configured for checks
        return 0

    return len(checks)



def movements_difference(operation_id):
    # None for unresolved amounts
    difference = None
    invert_value = 1
    operation = db.operation[operation_id]
    document = operation.document_id
    if document.invert: invert_value = -1

    # draft movements algorithm:
    # difference = exit concepts - entry c.
    q_entry = db.movement.concept_id == db.concept.concept_id
    q_entry &= db.concept.entry == True
    q_entry &= db.movement.operation_id == session.operation_id

    q_exit = db.movement.concept_id == db.concept.concept_id
    q_exit &= db.concept.exit == True
    q_exit &= db.movement.operation_id == session.operation_id

    print T("Calculate movements difference....")

    rows_entry = db(q_entry).select()
    print T("Entries: %s") % str([row.movement.amount for row in rows_entry])

    rows_exit = db(q_exit).select()
    print T("Exits: %s") % str([row.movement.amount for row in rows_exit])

    # Value inversion gives unexpected difference amounts in documents
    # TODO: complete difference evaluation including Entry/Exit parameters

    difference = float(sum([row.movement.amount for row in \
    rows_exit if row.movement.amount is not None], 0) \
    - sum([row.movement.amount for row \
    in rows_entry if row.movement.amount is not None], 0))
    # * invert_value

    print T("Difference: %s") % difference

    return difference


def movements_update(operation_id):
    """ Operation maintenance (amounts, checks, taxes, difference) """
    # Get options
    update_taxes = session.get("update_taxes", False)

    update = False

    if update_taxes == True:
        taxes = movements_taxes(operation_id)

    checks = movements_checks(operation_id)
    session.difference = movements_difference(operation_id)
    db.operation[operation_id].update_record( \
    amount = movements_amount(operation_id))
    update = True
    return update


def movements_amount(operation_id):
    """ Calculate the total amount of the operation"""

    amount = None

    q_items = db.movement.concept_id == db.concept.concept_id
    q_items &= db.concept.internal != True
    q_items &= db.concept.discounts != True
    q_items &= db.concept.surcharges != True
    q_items &= db.concept.current_account != True
    q_items &= db.movement.operation_id == operation_id

    q_discounts = db.movement.concept_id == db.concept.concept_id
    q_discounts &= db.concept.discounts == True
    q_discounts &= db.movement.operation_id == operation_id

    q_surcharges = db.movement.concept_id == db.concept.concept_id
    q_surcharges &= db.concept.surcharges == True
    q_surcharges &= db.movement.operation_id == operation_id

    rows_items = db(q_items).select()
    rows_surcharges = db(q_surcharges).select()
    rows_discounts = db(q_discounts).select()

    items = float(abs(sum([item.movement.amount for item \
    in rows_items if item.movement.amount is not None])))
    surcharges = float(abs(sum([item.movement.amount \
    for item in rows_surcharges if item.movement.amount is not None])))
    discounts = float(abs(sum([item.movement.amount \
    for item in rows_discounts if item.movement.amount is not None])))

    amount = float(items + surcharges -discounts)

    return amount


def movements_stock(operation_id):
    """ TODO: Return False as result if any stock errors are found"""
    
    update_stock_list = session.get("update_stock_list", set())
    result = False
    movements = db(db.movement.operation_id == operation_id).select()
    document = db.operation[operation_id].document_id
    warehouse_id = session.get("warehouse_id", None)
    items = 0
    for movement in movements:
        concept = db(db.concept.concept_id == movement.concept_id \
        ).select().first()
        if (concept is not None) and (warehouse_id is \
        not None) and (concept.stock == True) and (movement.movement_id in update_stock_list):
            stock = db(( \
            db.stock.warehouse_id == warehouse_id) \
            & (db.stock.concept_id == concept.concept_id) \
            ).select().first()
            if stock is not None:
                value = stock.value
                if (document is not None) and ( \
                document.invert == True):
                    value += movement.quantity
                else:
                    value -= movement.quantity

                # update stock value
                print T("Updating stock id: %(st)s as %(vl)s") % dict(st=stock.stock_id, vl=value)
                stock.update_record(value = value)
                items += 1

    return True


def is_editable(operation_id):
    """ Check if operation can be modified"""
    operation = db.operation[operation_id]
    if operation.voided or operation.canceled or operation.processed:
        return False
    return True

####################################################################
#   Controller actions
####################################################################

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

    return dict(operations = operations, message=T("Administrative panel"))

# base web interface for movements
# administration
@auth.requires_login()
def ria_movements():
    # reset the current operation (sent client-side)
    reset_operation_form = FORM(INPUT(_type="submit", _value=T("Reset operation")))
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
        response.flash = T("Form accepted")
    
    # Process operation for accounting/other when accepted
    process_operation_form = FORM(INPUT(_value="Process", _type="submit"))
    
    if process_operation_form.accepts(request.vars, formname="process_operation"):
        # TODO: incomplete
        # do not expose if operation was already processed
        # process/validate the operation
        if operations.process(db, session, operation_id):
            response.flash = T("Operation processed")
        else:
            response.flash = T("Could not process the operation")
    
    return dict(message=T("Operation number %s") % operation_id, \
    form = form, \
    reset_operation_form = reset_operation_form, \
    process_operation_form = process_operation_form)
    
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
        response.flash = T("Form accepted")
    elif form.errors:
        response.flash = T("The form has errors")
        
    # query for operation movements
    movements_list = db(db.movement.operation_id == session.operation_id).select()
    
    return dict(form=form, movements_list = movements_list)

def movements_modify_element():
    """ Movements element edition sub-form."""
    movements_element = request.args[1]
    form = SQLFORM(db.movement, movements_element, \
    _id="movements_modify_element_form")
    if form.accepts(request.vars, session):
        response.flash = T("Form accepted")
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
        quota_amount = total / float(request.vars.quotas)
        quotas_list = list()
        for x in range(int(request.vars.quotas)):
            quotas_list.append(db.quota.insert(installment_id = installment_id, \
            fee_id = request.vars.fee_id, number = x+1, amount = quota_amount))

        installment = db.installment[installment_id]
        installment.update(quotas = len(quotas_list), \
        monthly_amount = quota_amount, starting_quota_id = quotas_list[0], \
        ending_quota_id = quotas_list[len(quotas_list) -1])
        response.flash = T("Installment created")

    return dict(total = total, form = form, installment = installment)


@auth.requires_login()
def ria_new_customer_order():
    """ Customer's ordering on-line form.
    Note: get db objects with db(query).select()
    i.e. contact.customer returns the db record id """

    if len(request.args) > 0:
        session.operation_id = int(request.args[1])

    reset_order = FORM(INPUT(_type="submit", _value=T("Reset order")))
    if reset_order.accepts(request.vars, session):
        session.operation_id = None
    contact_user = db(db.contact_user.user_id == auth.user_id).select().first()

    # catch incomplete registrations (no contact user relations)
    if contact_user is None:
        return dict(form=None, reset = None, \
        contact = None, customer = None, order = None, \
        contact_user=None)
    try:
        contact = db(db.contact.contact_id == contact_user.contact_id \
        ).select().first()
    except KeyError:
        contact = None
    try:
        customer = db(db.customer.customer_id == contact.customer_id \
        ).select().first()
    except KeyError:
        customer = None

    # Look for allowed orders in options db
    customer_allowed_orders = db(db.option.name == \
    "customer_allowed_orders").select().first()
    
    if customer_allowed_orders and  isinstance( \
    customer_allowed_orders.value, basestring):
        allowed_orders_list = [\
        db(db.document.code == str(o).strip()).select().first().document_id \
        for o in \
        customer_allowed_orders.value.split("|") if len(o) > 0]
    else:
        allowed_orders_list = []
        
    # Get the default order
    
    default_order = db(db.document.code == db(db.option.name == \
    "customer_default_order").select().first().value).select().first().document_id
    
    if isinstance(default_order, basestring): \
    default_order = int(default_order)

    # create a new order with pre-populated user data
    if not "operation_id" in session.keys():
        customer_order = db.operation.insert( \
        customer_id = customer, document_id = default_order)
        session.operation_id = customer_order
    else:
        customer_order = session.operation_id
        if session.operation_id is None:
            customer_order = db.operation.insert( \
            customer_id = customer, \
            document_id = default_order)
            session.operation_id = customer_order

    form = SQLFORM(db.operation, customer_order, \
    fields=["description"], _id="new_customer_order_form")

    # Available order documents
    order_documents = db(db.document.orders == True).select()
    checks = 0
    loop_count = 0
    check_list = list()
    order_options = dict()

    if form.accepts(request.vars, session):
        db.operation[customer_order].update_record( \
        document_id = request.vars.order_type)
        response.flash = T("Form accepted")

    for order_document in order_documents:
        loop_count += 1
        # check option if previously selected
        if db.operation[customer_order].document_id \
        == order_document.document_id:
            checked = True
        elif order_document.document_id == default_order:
            checked = True
        else:
            checked = False
        if order_document.code in allowed_orders_list:
            order_options[order_document.document_id] = dict()
            order_options[order_document.document_id]["label"] = order_document.description
            order_options[order_document.document_id]["name"] = "order_type"
            order_options[order_document.document_id]["value"] = order_document.document_id
            if checked:
                order_options[order_document.document_id]["checked"] = True
                checked = False
            else:
                order_options[order_document.document_id]["checked"] = False

    return dict(form=form, reset = reset_order, contact = contact, \
    customer = customer, order = db.operation[customer_order], \
    contact_user = contact_user, order_options = order_options)

# order movement creation
def new_customer_order_element():
    """ Insert sub-form for product selection at Customer ordering form"""
    if not "operation_id" in session.keys():
        raise HTTP(500, "Customer order not found.")
    form = SQLFORM.factory(Field('concept_id', \
    'reference concept', requires=IS_IN_SET(orderable_concepts())), \
    Field('description'), Field('quantity', 'double'), \
    _id="new_customer_order_element_form")
    if form.accepts(request.vars, session):
        db.movement.insert(operation_id = session.operation_id, \
        concept_id = request.vars.concept_id, \
        description = request.vars.description, \
        quantity = request.vars.quantity)
        response.flash = T("Form accepted")
    order_list = db(db.movement.operation_id == session.operation_id  \
    ).select()
    return dict(form=form, order_list = order_list)

# order movement modification
def new_customer_order_modify_element():
    """ Customer order element edition sub-form."""
    if not "operation_id" in session.keys():
        raise HTTP(500, "Customer order not found.")
    customer_order_element = db.movement[request.args[1]]

    form = SQLFORM.factory(Field('concept_id', \
    'reference concept', requires=IS_IN_SET(orderable_concepts()), \
    default=customer_order_element.movement_id), \
    Field('description', default=customer_order_element.description), \
    Field('quantity', 'double', \
    default = customer_order_element.quantity), \
    _id="new_customer_order_modify_element_form")
    if form.accepts(request.vars, session):
        customer_order_element.update_record( \
        description = request.vars.description, \
        concept_id = request.vars.concept_id, \
        quantity = request.vars.quantity)
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
        except (KeyError, ValueError, AttributeError, TypeError):
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
                customer_desc = db(db.customer.customer_id == customer \
                ).select().first().description
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

    form = FORM(TABLE(THEAD(TR(TH(T("Customer")),TH(T("Product code")), \
    TH(T("Concept")), TH(T("Ordered")), TH(T("Allocated")), TH(T("Stock")), \
    TH(T("Allocate")))), TBODY(*form_rows), TFOOT(TR(TD(), TD(), TD(), \
    TD(), TD(), TD(), TD(INPUT(_value=T("Allocate orders"), _type="submit"))))))

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
                    movements_stack[customer][concept]["allocate"] = float( \
                    request.vars[var])
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
                        operation = db.operation.insert(customer_id = customer, \
                        document_id = db(db.document.books == True).select().first())
                    db.movement.insert(operation_id = operation, \
                    quantity = w["allocate"], concept_id = concept)
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
    headers={"operation.operation_id": T("Edit"), "operation.code":T("Code"), \
    "operation.description": T("Description"), "operation.posted": T("Posted")}
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
    T("ID"), "movement.code": T("Code"), \
    "movement.concept_id": T("Concept"), "movement.quantity": T("Quantity")}, \
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
    "movement.quantity"], headers={"movement.movement_id": T("ID"), \
    "movement.code": T("Code"), \
    "movement.concept_id": T("Concept"), "movement.quantity": T("Quantity")})

    return dict(packing_slip_form = packing_slip_form, \
    movements = movements, packing_slip_id = packing_slip_id)

def ria_receipt():
    """    Get or create a new receipt.
    Presents a one-view multi-form receipt
    for customer payments
    """
    operation_id = session.get("operation_id", None)

    # allow receipt reset
    reset_receipt_form = FORM(INPUT(_type="submit", _value=T("Reset receipt")))
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
            response.flash=T("Receipt processed")
        else:
            response.flash=T("Could not process the receipt")

    receipt_form = crud.update(db.operation, operation_id)
    if receipt_form.accepts(request.vars, \
    formname="receipt_form"):
        response.flash=T("Form accepted")

    if (document is None) or (document.receipts != True):
        # return error
        response.flash=T("Warning! Wrong document type.")

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

        response.flash = T("Item added")

    check_form.vars.operation_id = operation_id

    columns = ["bank_ckeck.bank_check_id", "bank_check.number", \
    "bank_check.customer_id", \
    "bank_check.code", "bank_check.description", "bank_check.amount"]
    headers = {"bank_ckeck.bank_check_id": T("Edit"), \
    "bank_check.number": T("Number"), "bank_check.customer_id": T("Customer"), \
    "bank_check.code": T("Code"), "bank_check.description": T("Description"), \
    "bank_check.amount": T("Amount")}

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
    headers = {"movement.movement_id": T("Edit"), "movement.code": T("Code"), \
    "movement.description": T("Description"), "movement.posted": T("Posted"), \
    "movement.amount": T("Amount"), "movement.concept_id": T("Concept")}

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
    headers = {"operation.operation_id": T("Edit"), \
    "operation.code": T("Code"), "operation.description": T("Description"), \
    "document.description": T("Document"), \
    "operation.posted": T("Posted")}

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
    if customer_form.accepts(request.vars, session, \
    keepvalues=True, formname="customer_form"):
        q = (db.operation.customer_id == request.vars.customer_id \
        ) | (db.operation.subcustomer_id == request.vars.subcustomer_id)
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
    document_options = [OPTION(document.description, \
    _value=document.document_id) for document in documents]

    billing_form = FORM(TABLE(THEAD(TR(TH(T("Operation")),TH(T("Posted")), \
    TH(T("Code")), TH(T("Description")), TH(T("Bill")))), \
    TBODY(*packing_slips_rows), \
    TFOOT(TR(TD(), TD(), TD(), TD(LABEL(T("Choose a document type"), \
    _for="document_id"), SELECT(*document_options, _name="document_id")), \
    TD(INPUT(_value=T("Bill checked"), _type="submit"))))))

    # operations marked for billing
    bill_items = []

    if billing_form.accepts(request.vars, session, \
    formname="billing_form"):
        for v in request.vars:
            if v.startswith("operation_"):
                bill_items.append(int(v.split("_")[1]))
        if len(bill_items) > 0:
            # create an invoice  with the collected data
            invoice_id = db.operation.insert( \
            document_id = request.vars.document_id, \
            customer_id = customer_id, \
            subcustomer_id =  subcustomer_id)
            # fill the invoice
            for packing_slip_id in bill_items:
                packing_slip_items = db( \
                db.movement.operation_id == packing_slip_id).select()
                for movement in packing_slip_items:
                    db.movement.insert(operation_id = invoice_id, \
                    concept_id = movement.concept_id, \
                    amount = movement.amount, value = movement.value, \
                    quantity = movement.quantity)
                # check the packing slip as processed
                db.operation[packing_slip_id].update_record( \
                processed = True)

            # TODO: insert ivoices payment / current account movements
            # set invoice as current operation
            session.operation_id = invoice_id
            # redirect to movements edition
            redirect(URL(c="operations", f="ria_movements"))

    return dict(customer_form = customer_form, \
    billing_form = billing_form)




####################################################################
############ Sequential operation processing (no RIA) ##############
####################################################################


def movements_start():
    """ Initial operation form """

    # erease stock update values
    session.update_stock_list = set()

    form = SQLFORM.factory(Field("type", \
    requires=IS_IN_SET({"T": T("Stock"), "S": \
    T("Sales"), "P": T("Purchases")}), \
    comment=T("Select an operation type")), Field("description"))
    
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

    # default form data
    default_supplier_option = db(db.option.name == "default_supplier_code").select().first()
    default_customer_option = db(db.option.name == "default_customer_code").select().first()
    customer_option = supplier_option = None

    if operation.type == "S":
        fields = ["code", "description", "supplier_id", \
        "customer_id", \
        "detail", "payment_terms_id", "term", "document_id", \
        "branch", "due_date", "voided", "fund_id", \
        "cost_center_id", "observations", "subcustomer_id", \
        "salesperson_id", "jurisdiction_id"]
        supplier_option = default_supplier_option

        # Document form options
        s = db(db.document.entry == True)

    elif operation.type == "T":
        fields = None

        # Document form options
        s = db(db.document.stock == True)
        
    elif operation.type == "P":
        fields = ["code", "description", "supplier_id", \
        "customer_id", \
        "detail", "payment_terms_id", "term", "document_id", \
        "branch", "due_date", "voided", "fund_id", \
        "cost_center_id", "observations", "jurisdiction_id"]
        customer_option = default_customer_option

        # Document form options
        s = db(db.document.exit == True)

    # Document filter by Sales, Purchases or Stock
    db.operation.document_id.requires = IS_IN_DB(s, "document.document_id", "%(description)s")

    form = SQLFORM(db.operation, operation_id, \
    fields = fields)

    # auto-complete header form
    if supplier_option is not None:
        try:
            form.vars.supplier_id = int(
            db(db.supplier.code == supplier_option.value).select().first().supplier_id
            )
        except (ValueError, TypeError):
            form.vars.supplier_id = None
    elif customer_option is not None:
        try:
            form.vars.customer_id = int(
            db(db.customer.code == customer_option.value).select().first().customer_id
            )
        except (ValueError, TypeError):
            form.vars.customer_id = None

    if form.accepts(request.vars, session):
        if operation.type in ("S", "P"):
            redirect(URL(f="movements_price_list"))
        else:
            redirect(URL(f="movements_detail"))
        
    return dict(form = form, operation = operation)


def movements_price_list():
    form = SQLFORM.factory(Field("price_list", \
    requires = IS_IN_DB(db(db.price_list), \
    "price_list.price_list_id", "%(description)s")))
    if form.accepts(request.vars, session):
        session.price_list_id = request.vars.price_list
        redirect(URL(f="movements_detail"))
    return dict(form = form)


def movements_detail():
    """ List of operation items
    
    A user interface to manage movements
    """

    operation_id = session.operation_id
    
    # Operation options
    update_stock = session.get("update_stock", None)
    warehouse_id = session.get("warehouse_id", None)
    # Tax items are updated by default
    
    update_taxes = session.get("update_taxes", None)
    if update_taxes is None:
        update_taxes = session.update_taxes = True
    
    # selected price list or None
    price_list_id = session.get("price_list_id", None)
    if price_list_id is not None:
        price_list = db.price_list[price_list_id]
    else: price_list = None

    # update operation values
    if is_editable(operation_id):
        update = movements_update(operation_id)
    else:
        update = False
        print T("Operation %s is not editable") % operation_id

    # Get the operation dal objects
    operation = db.operation[operation_id]
    customer = db(db.customer.customer_id == operation.customer_id).select().first()
    subcustomer = db(db.subcustomer.subcustomer_id == operation.subcustomer_id).select().first()
    supplier = db(db.supplier.supplier_id == operation.supplier_id).select().first()

    # { header:table, ... h:t} dictionary
    movements = dict()

    if warehouse_id is not None:
        warehouse = db.warehouse[warehouse_id].description
    else:
        warehouse = T("None selected")
        
    if update_stock is None:
        update_stock = session.update_stock = False
    
    # Items (Products/Services/Discounts ...)
    q = db.movement.concept_id == db.concept.concept_id
    q &= db.concept.internal != True
    q &= db.concept.tax != True
    q &= db.concept.banks != True
    q &= db.movement.operation_id == operation_id
    
    s = db(q)
    columns = ["movement.movement_id", "movement.code", \
    "movement.description", "movement.concept_id", \
    "movement.quantity", "movement.value", "movement.amount"]
    headers = {"movement.movement_id": T("Edit"), \
    "movement.code": T("Code"), \
    "movement.description": T("Description"), \
    "movement.concept_id": T("Concept"), \
    "movement.quantity": T("Quantity"), \
    "movement.value": T("Value"), \
    "movement.amount": T("Amount")}
    
    rows = s.select()
    movements["items"] = SQLTABLE(rows, \
    columns = columns, headers = headers, linkto=URL(f="movements_modify_item"))
   
    # Payments
    q = db.movement.concept_id == db.concept.concept_id
    q &= db.concept.banks != True
    q &= ((db.concept.payment_method == True) | ( \
    db.concept.current_account == True))
    q &= db.movement.operation_id == operation_id
    
    s = db(q)
    
    rows = s.select()
    movements["payments"] = SQLTABLE(rows, \
    columns = columns, headers = headers, linkto=URL(f="movements_modify_item"))

    # Checks
    q = db.bank_check.operation_id == operation_id
    s = db(q)

    rows = s.select()
    movements["checks"] = SQLTABLE(rows, columns = [
        "bank_check.bank_check_id", "bank_check.bank_id", \
        "bank_check.due_date", \
        "bank_check.number", "bank_check.amount"
        ],
        headers = {
        "bank_check.bank_check_id": T("Edit"), \
        "bank_check.bank_id": T("Bank"), \
        "bank_check.due_date": T("Due date"), \
        "bank_check.number": T("Number"), \
        "bank_check.amount": T("Amount")
        }, linkto=URL(f="movements_modify_item"))
    
    # Taxes
    q = db.movement.concept_id == db.concept.concept_id
    q &= db.concept.tax == True
    q &= db.movement.operation_id == operation_id
    s = db(q)
    
    rows = s.select()
    movements["taxes"] = SQLTABLE(rows, \
    columns = columns, headers = headers, linkto=URL(f="movements_modify_item"))

    return dict(operation = operation, \
    movements = movements, price_list = price_list, \
    update_stock = update_stock, warehouse = warehouse, \
    customer = customer, subcustomer = subcustomer, \
    supplier = supplier, update_taxes = update_taxes)


def movements_add_item():
    """ Adds an item movement to the operation.

    Note: on-form item value edition needs AJAX and js events
    for db price queries
    """

    try:
        concept_id = request.args[1]
    except (ValueError, IndexError, TypeError):
        concept_id = None

    # update stock option
    update_stock_list = session.get("update_stock_list", set())
    
    operation_id = session.operation_id
    operation = db.operation[operation_id]
    document = db.document[operation.document_id]

    price_list_id = session.get("price_list_id", None)

    form = SQLFORM.factory(Field("item", \
    requires=IS_IN_DB(db(db.concept.internal != True), \
    "concept.concept_id", "%(description)s"), default = concept_id), \
    Field("value", "double", comment = T("Blank for price list values")), \
    Field("quantity", requires = IS_FLOAT_IN_RANGE(-1e6, 1e6)), Field("update_stock", "boolean", default = True))

    if form.accepts(request.vars, session):
        # Get the concept record
        concept_id = request.vars.item
        quantity = float(request.vars.quantity)
        try:
            value = float(request.vars.value)
        except (ValueError, TypeError):
            # no value specified
            value = None
        amount = None

        print T("Item value input: %s") % value

        # Calculate price
        if (price_list_id is not None) and (value is None):
            price = db((db.price.price_list_id == price_list_id \
            ) & (db.price.concept_id == concept_id)).select().first()
            value = price.value
            
        # calculated amount for the movement
        try:
            amount = value * quantity
        except (ValueError, TypeError):
            # No price list or item value
            amount = None

        # Create the new operation item
        if is_editable(operation_id):
            movement_id = db.movement.insert(operation_id = operation_id, \
            amount = amount, value = value, concept_id = concept_id, \
            quantity = quantity)
            print T("Operation: %(o)s. Amount: %(a)s. Value: %(v)s. Concept: %(c)s, Quantity: %(q)s, Movement: %(m)s") % dict(o=operation_id, a=amount, v=value, c=concept_id, q=quantity, m=movement_id)
        else:
            movement_id = None
            print T("Operation %s is not editable") % operation_id

        # add movement to temporary stock update list
        if request.vars.update_stock:
            if movement_id is not None:
                update_stock_list.add(int(movement_id))
            session.update_stock_list = update_stock_list

        redirect(URL(f="movements_detail"))

    return dict(form = form)


def movements_modify_item():
    """ Modify an operation's item (or movement). """

    operation_id = session.operation_id
    operation = db.operation[operation_id]
    document = db.document[operation.document_id]
    movement = db.movement[request.args[1]]

    form = SQLFORM.factory(Field("item", \
    requires=IS_IN_DB(db(db.concept.internal != True), \
    "concept.concept_id", "%(description)s"), default = movement.concept_id), \
    Field("value", "double", requires = IS_FLOAT_IN_RANGE(-1e6, 1e6), default = movement.value), \
    Field("quantity", requires = IS_FLOAT_IN_RANGE(-1e6, 1e6), default = movement.quantity), \
    Field("delete", "boolean", default = False, comment = T("The item will be removed without confirmation")))

    if form.accepts(request.vars, session):
        print T("Delete value is %s") % request.vars.delete
        if request.vars.delete:
            # erase the db record if marked for deletion
            if is_editable(operation_id):
                print T("Erasing record %s") % movement.movement_id
                movement.delete_record()
            else:
                print T("Operation %s is not editable") % operation_id
        else:
            # Get the concept record
            concept_id = request.vars.item
            quantity = float(request.vars.quantity)
            value = amount = None

            """
            # Calculate price, value, quantity, amount            
            price_list_id = session.get("price_list_id", None)
            if price_list_id is not None:
                price = db((db.price.price_list_id == price_list_id \
                ) & (db.price.concept_id == concept_id)).select().first()

            # not used (price/value should be pre-established by a db insert form)
            """

            value = float(request.vars.value)
            amount = value * quantity

            # Modify the operation item
            if is_editable(operation_id):
                movement.update_record(\
                amount = amount, value = value, concept_id = concept_id, \
                quantity = quantity)
                print T("Operation: %(o)s. Amount: %(a)s. Value: %(v)s. Concept: %(c)s, Quantity: %(q)s") % dict(o=operation_id, a=amount, v=value, c=concept_id, q=quantity)
            else:
                print T("Operation %s is not editable") % operation_id

        redirect(URL(f="movements_detail"))
    return dict(form = form)


def movements_add_check():
    operation_id = session.operation_id
    
    """ Adds a check for any operation type """
    # TODO: select different fields for each operation type
    # add own for company checks
    fields = [
    "number", "bank_id", "customer_id", "supplier_id", "amount", \
    "due_date", "checkbook_id"
    ]
    form = SQLFORM(db.bank_check, fields=fields)
    form.vars.operation_id = operation_id
    if form.accepts(request.vars, session):
        redirect(URL(f="movements_detail"))
    return dict(form = form)


def movements_current_account_concept():
    """ Manage current account payment/quotas """
    operation_id = session.operation_id
    # calculate the amount for payment
    session.difference = movements_difference(operation_id)
    # create quotas based on user input
    # (for quotas number > 0)
    
    # define number of quotas and due dates
    session.quota_frequence = datetime.timedelta(\
    int(db(db.option.name == "quota_frequence"\
    ).select().first().value))
    
    session.today = datetime.date.today()

    if session.difference <= 0:
        # return 0 amount message and cancel
        redirect(URL(f="movements_detail"))

    # Current account concepts dal set
    q = db.concept.current_account == True
    s = db(q)

    form = SQLFORM.factory(Field("concept", "reference concept", \
    requires = IS_IN_DB(s, "concept.concept_id", "%(description)s")))

    if form.accepts(request.vars, session, formname="concept_form"):
        session.current_account_concept_id = int(request.vars.concept)
        redirect(URL(f="movements_current_account_quotas"))

    return dict(form = form)

def movements_current_account_quotas():
    form = SQLFORM.factory(Field("number_of_quotas", \
    "integer", requires = IS_INT_IN_RANGE(0, 1e3)))

    if form.accepts(request.vars, session, \
    formname="quotas_number_form"):
        session.current_account_quotas = int(request.vars.number_of_quotas)
        redirect(URL(f="movements_current_account_data"))
    return dict(form = form)

def movements_current_account_data():
    # Get operation id and check if it is not
    # editable
    operation_id = session.operation_id
    if not is_editable(operation_id):
        print T("Operation %s is not editable") % operation_id
        redirect(URL(f="movements_detail"))
        
    # Begin current account data processing
    try:
        amount_fields = [Field("quota_%s_amount" % (x+1), \
        "double", requires=IS_FLOAT_IN_RANGE(0, 1e6), \
        default=(session.difference / \
        float(session.current_account_quotas))) \
        for x in range(session.current_account_quotas)]
        due_date_fields = [Field("quota_%s_due_date" % (x+1), \
        "date", default=session.today+(session.quota_frequence*x)) \
        for x in range(session.current_account_quotas)]
        form_fields = []
    except ZeroDivisionError:
        # Zero quotas. Create the
        # current account movement
        # for the difference
        db.movement.insert( \
        concept_id = session.current_account_concept_id, \
        amount = session.difference, value = session.difference, \
        quantity = 1, operation_id = operation_id)
        redirect(URL(f="movements_detail"))

    for x in range(session.current_account_quotas):
        form_fields.append(amount_fields[x])
        form_fields.append(due_date_fields[x])

    # Present form for user input with
    # quota fields
    form = SQLFORM.factory(*form_fields)
    if form.accepts(request.vars, session, formname="quotas_data_form"):
        # create or modify the payment movements and quotas
        due_dates = dict()
        amounts = dict()
        # Search for current account items
        for var in request.vars:
            if var.endswith("amount"):
                amounts[var.split("_")[1]] = float(request.vars[var])
            elif var.endswith("due_date"):
                due_dates[var.split("_")[1]] = request.vars[var]
        for quota, amount in amounts.iteritems():
            # insert quota
            # insert movement
            db.movement.insert( \
            concept_id = session.current_account_concept_id, \
            amount = amount, value = amount, \
            quantity = 1, operation_id = operation_id)
            # insert payments/plans
        redirect(URL(f="movements_detail"))
    return dict(form = form)


def movements_add_discount_surcharge():
    """ Select discount to apply """

    # Get the session stored operation id
    operation_id = session.operation_id
    
    # user input: concept, % or value, value, description
    q = (db.concept.surcharges == True) | (db.concept.discounts == True)
    form = SQLFORM.factory(Field('concept', requires = IS_IN_DB(db(q), \
    "concept.concept_id", "%(description)s")), Field('percentage', \
    'boolean'), Field('value', 'double'), Field('description'))
    if form.accepts(request.vars, session):
        if request.vars.percentage:
            # TODO: refined discount/surcharge
            # processing. Move total amount
            # adding to function "total(operation_id)"
            q = db.movement.concept_id == db.concept.concept_id
            q &= db.movement.operation_id == operation_id
            q &= db.concept.internal != True
            q &= db.concept.tax != True
            rows = db(q).select()
            value = float(request.vars.value) * \
            float(sum([abs(item.movement.amount) \
            for item in rows])) / 100
        else: value = float(request.vars.value)

        if is_editable(operation_id):
            db.movement.insert(operation_id = operation_id, \
            description = request.vars.description, quantity = 1, \
            amount = value, value = value, \
            concept_id = request.vars.concept)
        else:
            print T("Operation %s is not editable") % operation_id
            
        redirect(URL(f="movements_detail"))
        
    return dict(form = form)


def movements_list():
    """ List of operations"""
    columns = ["operation.operation_id", "operation.code", \
    "operation.description", "operation.customer_id", \
    "operation.subcustomer_id", "operation.supplier_id", \
    "operation.document_id", "operation.posted"]
    headers = {"operation.operation_id": T("Edit"), \
    "operation.code": T("Code"), "operation.description": \
    T("Description"), "operation.customer_id": T("Customer"), \
    "operation.subcustomer_id": T("Subcustomer"), \
    "operation.supplier_id": T("Supplier"), \
    "operation.document_id": T("Document"), \
    "operation.posted": T("Posted")}
    table = SQLTABLE(db(db.operation).select(), \
    columns = columns, headers = headers, \
    linkto=URL(c="operations", f="movements_select"))
    return dict(table = table)

def movements_select():
    """ Set operation id and open a detail view """
    session.operation_id = request.args[1]
    redirect(URL(f="movements_detail"))

def movements_process():
    message = None

    operation_id = session.operation_id

    if not is_editable(operation_id):
        return dict(message = T("Could not process the operation: it is not editable"))
    
    operation = db.operation[operation_id]
    document = operation.document_id
    movements = db(db.movement.operation_id == operation_id).select()

    # offset / payment terms movement
    # Long notation for record id == 0 db issue
    payment_terms = db( \
    db.payment_terms.payment_terms_id == operation.payment_terms_id \
    ).select().first()

    # Purchases offset custom concept
    try:
        purchases_payment_terms_concept_id = db(\
        (db.option.name == "purchases_payment_terms_concept_code") & (db.option.args == str(payment_terms.code)) \
        ).select().first().value
        
    except AttributeError, e:
        print str(e)
        purchases_payment_terms_concept_id = None
        
    print T("For purchases: %(pt)s payment is recorded as concept id %s(c)") % dict(pt=payment_terms.description, c=purchases_payment_terms_concept_id)

    stock_updated = False

    # receipt documents movement and offset change
    if document.receipts == True:
        
        receipt_default_offset_concept_id = db(\
        db.concept.code == db(\
        db.option.name == "receipt_default_offset_concept_code"\
        ).select().first().value).select().first().concept_id

        if operation.type == "S":
            receipt_offset_concept_id = db(\
            db.concept.code == db(\
            db.option.name == "sales_receipt_offset_concept_code"\
            ).select().first().value).select().first().concept_id

        elif operation.type == "P":
            receipt_offset_concept_id = db(\
            db.concept.code == db(\
            db.option.name == "purchases_receipt_offset_concept_code"\
            ).select().first().value).select().first().concept_id

        receipt_offset_concept = db.concept[receipt_offset_concept_id]

        # Search current account movements
        has_current_account_movements = False

        for movement in movements:
            try:
                movement_concept = db(db.concept.concept_id == \
                movement.concept_id).select().first()

                if (movement_concept.current_account != True) and \
                (movement_concept.payment_method != True):
                    # change the movement concept for booking/current accounts
                    # add movement concept to the item description

                    # invert values if needed
                    if (receipt_offset_concept.entry == movement_concept.entry) or (receipt_offset_concept.exit == movement_concept.exit):
                        amount = movement.amount
                    else:
                        amount = (-1)*movement.amount

                    movement.update_record(concept_id = \
                    receipt_offset_concept_id, \
                    description = movement_concept.description, amount = amount)

                    # set operation with current account movements
                    # for offset concept selection
                    if receipt_offset_concept.current_account == True:
                        has_current_account_movements = True

                elif movement_concept.current_account == True:
                    has_current_account_movements = True
            except RuntimeError, e:
                print str(e)

        print T("The operation has current account movements: %s") % has_current_account_movements

        if has_current_account_movements:
            # set the default payment concept as offset
            offset_concept_id = receipt_default_offset_concept_id
        else:
            offset_concept_id = receipt_offset_concept_id
        print T("Setting offset concept to %s") % db.concept[receipt_offset_concept_id].description
        
    else:
        if operation.type == "P" and (purchases_payment_terms_concept_id is not None) and document.invoices:
            offset_concept_id = purchases_payment_terms_concept_id
        else:
            offset_concept_id = payment_terms.concept_id

    # end of receipt documents movement and offset change


    # Calculate difference for payments
    session.difference = movements_difference(operation_id)
    print T("Movements process. Operation: %s") % operation_id
    print T("session.difference :%s") % session.difference


    if abs(session.difference) > 0.01:
        # Wich offset / payment concept to record
        # option based offset concept

        offset_concept = db.concept[offset_concept_id]

        # TODO: validate current account limit if offset concept is
        # current account. Move validation to auxiliar function

        if (offset_concept.current_account == \
        True) and (operation.type == "S") and (not document.receipts == True):
            if operation.subcustomer_id is not None:
                current_account_value = \
                crm.subcustomer_current_account_value( \
                db, operation.subcustomer_id)
                print T("Current account value: %s") % current_account_value
                try:
                    # Get the current account limit
                    # allowed
                    debt_limit = float( \
                    operation.subcustomer_id.current_account_limit)
                except (TypeError, ValueError, AttributeError):
                    # No limit found
                    debt_limit = 0.00
                    
                print T("Debt limit: %s") % debt_limit

                if (current_account_value + session.difference) > debt_limit:
                    return dict(message= \
                    T("Operation processing failed: debt limit reached"))

            elif operation.customer_id is not None:
                current_account_value = \
                crm.customer_current_account_value(db, \
                operation.customer_id)
                print T("Current account value: %s") % current_account_value                
                try:
                    # Get the current account limit
                    # allowed
                    debt_limit = float( \
                    operation.customer_id.current_account_limit)
                except (TypeError, ValueError, AttributeError):
                    # No limit found
                    debt_limit = 0.00
                    
                print T("Debt limit: %s") % debt_limit
                
                if (current_account_value + session.difference) > debt_limit:
                    return dict(message= \
                    T("Operation processing failed: debt limit reached"))

        # Offset / Payment movement
        # TODO: change difference sign checking debit/credit
        # for now it only calculates correctly if offset concept has exit = True
        
        movement_id = db.movement.insert(operation_id = \
        operation_id, concept_id = offset_concept.concept_id, \
        quantity = 1, amount = session.difference, value = \
        session.difference)

        print T("Movement (offset): %(mo)s: %(a)s") % dict(mo=db.movement[movement_id].concept_id.description, a=db.movement[movement_id].amount)

        # update the operation
        updated = movements_update(operation_id)

    # TODO: operation difference revision (for accounting)

    result = None
    stock_updated = None

    # process operation
    if document.countable and operation.type in ("S", "P"):
        result = operations.process(db, session, session.operation_id)
        # print "Bypassing the operation processing"
        # result = True

    # change stock values if requested
    if (session.get("update_stock", False) == True) and (result != False):
        stock_updated = movements_stock(operation_id)

    if (result == False) or (stock_updated == False):
        message = T("The operation processing failed. Booking ok: %(rs)s. Stock ok: %(st)s") % dict(rs=result, st=stock_updated)
    else:
        message = T("Operation successfully processed")
        
    # TODO: rollback on errors
    return dict(message=message)


def movements_option_update_stock():
    """ Switch session update stock value """
    if session.update_stock == True:
        session.update_stock = False
    elif session.update_stock == False:
        session.update_stock = True
    redirect(URL(f="movements_detail"))

def movements_option_update_taxes():
    """ Switch session update taxes value """
    if session.update_taxes == True:
        session.update_taxes = False
    elif session.update_taxes == False:
        session.update_taxes = True

    print T("Change update taxes value to %s") % session.update_taxes    
    redirect(URL(f="movements_detail"))    

def movements_select_warehouse():
    form = SQLFORM.factory(Field("warehouse", \
    requires = IS_IN_DB(db(db.warehouse), \
    "warehouse.warehouse_id", "%(description)s")))
    if form.accepts(request.vars, session):
        session.warehouse_id = request.vars.warehouse
        redirect(URL(f="movements_detail"))
    return dict(form = form)



def movements_add_payment_method():
    # custom payment form
    operation = db.operation[session.operation_id]
    form = SQLFORM.factory(Field("method", "reference concept", \
    requires = IS_IN_DB(db(db.concept.payment_method == True), \
    "concept.concept_id", "%(description)s")), Field("amount", \
    "decimal(10,2)"), Field("quotas", "integer"), \
    Field("surcharge", "double"), Field("detail"), \
    Field("payment_reference_number", \
    comment = T("i.e. third party payment transaction number")))

    # on form validation process values
    if form.accepts(request.vars, session):
        # form name shortcuts and values filter
        detail = request.vars.detail
        reference = request.vars.payment_reference_number

        try:
            quotas = int(request.vars.quotas)
        except (ValueError, TypeError):
            quotas = 0

        try:
            amount = float(request.vars.amount)
        except (ValueError, TypeError):
            amount = 0.0

        try:
            surcharge = float(request.vars.surcharge)
        except:
            surcharge = 0.0

        # calculate the total amount with surcharge
        # when specified
        amount = amount*surcharge/100.0 + amount

        # Detailed quota amounts (uniform quota values)
        if quotas >1:
            quota_amount = amount/float(quotas)
            detail += T(" Quotas: %(quotas)s x%(quota_amount).2f") % dict(quotas=quotas, quota_amount=quota_amount)
            

        # Payment services transaction number in detail
        if len(reference) > 0:
            detail += T(" Transaction number: %s") % reference

        # insert the movement record if amount is not 0
        if amount != 0.0:
            db.movement.insert(operation_id = session.operation_id, \
            concept_id = request.vars.method, detail = detail, \
            amount = amount, description = detail, \
            value = amount, quantity = 1)

        redirect(URL(f="movements_detail"))

    return dict(form = form)


def movements_add_tax():
    operation = db.operation[session.operation_id]
    s = db(db.concept.tax == True)
    form = SQLFORM.factory(Field("concept", requires = IS_IN_DB(s, "concept.concept_id", "%(description)s")), Field("value", "double", requires = IS_FLOAT_IN_RANGE(-1e6, 1e6)))
    if form.accepts(request.vars, session):
        db.movement.insert(operation_id = operation.operation_id, concept_id = request.vars.concept, value = request.vars.value, quantity = 1, amount = request.vars.value)
        redirect(URL(f="movements_detail"))
    return dict(form = form)


def movements_articles():
    form = SQLFORM.factory(Field("category", "reference category", requires = IS_IN_DB(db, db.category, "%(description)s")), Field("subcategory", "reference subcategory", requires = IS_IN_DB(db, db.subcategory, "%(description)s")), Field("supplier", "reference supplier", requires = IS_IN_DB(db, db.supplier, "%(legal_name)s")))
    table = None
    
    if form.accepts(request.vars, session, keepvalues = True):
        # list items for selection
        q = db.concept.category_id == request.vars.category
        q &= db.concept.subcategory_id == request.vars.subcategory
        q &= db.concept.supplier_id == request.vars.supplier
        rows = db(q).select()

        columns = ["concept.concept_id", "concept.code", "concept.description", "concept.family_id", "concept.color_id"]
        headers = {"concept.concept_id": T("Select"), "concept.code": T("Code"), "concept.description": T("Description"), "concept.family_id": T("Family"), "concept.color_id": T("Color")}
        
        table = SQLTABLE(rows, columns = columns, headers = headers, linkto = URL(f="movements_add_item"))
        
    return dict(form = form, table = table)
