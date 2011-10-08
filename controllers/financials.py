# coding: utf8
# intente algo como

import datetime

def operations_values(operations):
    # TODO: optimize db queries
    # invert values based on document types
    
    # filter movements by current_account concept and operation id set
    # get the movements rows object
    # populate the array with movement values
    
    values = dict()
    for operation in operations:
        entry = 0.0
        exit = 0.0
        difference = 0.0
        movements = db(db.movement.operation_id == operation.operation_id).select()
        for movement in movements:
            try:
                if movement.concept_id.current_account == True:
                    if movement.amount > 0:
                        entry += float(movement.amount)
                    elif movement.amount < 0:
                        exit += float(movement.amount)*(-1)
            except (RuntimeError, AttributeError), e:
                print str(e)

            difference = entry -exit
        values[operation.operation_id] = [entry, exit, difference]

    return values


def index(): return dict(message="hello from financials.py")

def current_accounts_type():
    """ Lets the user choose the type
    of current account administration """
    form = SQLFORM.factory(Field("current_accounts_type", \
    requires = IS_IN_SET({"C":"Customer", "S":"Supplier"}), \
    widget = SQLFORM.widgets.radio.widget, default = "C"))
    if form.accepts(request.vars, session):
        print "Current accounts type: %s" % request.vars.current_accounts_type
        session.current_accounts_type = request.vars.current_accounts_type
        redirect(URL(f="current_accounts_data"))
    return dict(form = form)

    
def current_accounts_data():
    """ Initial parameters for the
    current accounts list """
    
    if session.current_accounts_type == "C":
        n = "customer"
        s = db(db.customer)
        i = "customer.customer_id"        
        f = "%(legal_name)s"
    elif session.current_accounts_type == "S":
        n = "supplier"
        s = db(db.supplier)
        i = "supplier.supplier_id"        
        f = "%(legal_name)s"
        
    today = datetime.date.today()
    start = datetime.date(1970, 1, 1)
    
    form = SQLFORM.factory(Field(n, requires = IS_IN_DB(s, i, f)), \
    Field("starts", "date", default = start), Field("ends", \
    "date", default = today), Field("due", "date", \
    default = today), Field("complete", "boolean"))
    if form.accepts(request.vars, session):
        print "Form data: %s" % str(request.vars)
        for k in request.vars:
            if not k.startswith("_"):
                if k == "complete":
                    if request.vars[k] == "on":
                        session["current_accounts_" + k] = True
                    else:
                        session["current_accounts_" + k] = False
                else:
                    session["current_accounts_" + k] = request.vars[k]

        redirect(URL(f="current_accounts_detail"))
    return dict(form = form)


def current_accounts_detail():
    """ List of current accounts operations"""
    if session.current_accounts_type == "C":
        supplier_id = db(db.option.name == "default_supplier_id").select().first().value
        session.current_accounts_supplier = supplier_id
        customer_id = session.current_accounts_customer
        payment_label = "Collect"

    elif session.current_accounts_type == "S":
        supplier_id = session.current_accounts_supplier
        customer_id = db(db.option.name == "default_customer_id").select().first().value
        session.current_accounts_customer = customer_id
        payment_label = "Pay"

    print "Session data: %s" % session

    # convert date string iso values
    starts_list = session.current_accounts_starts.split("-")
    ends_list = session.current_accounts_ends.split("-")
    due_list = session.current_accounts_due.split("-")

    # convert ISO to datetime object for DAL compatibility
    starts = datetime.datetime(int(starts_list[0]), int(starts_list[1]), int(starts_list[2]), 0, 0, 0)
    ends = datetime.datetime(int(ends_list[0]), int(ends_list[1]), int(ends_list[2]), 0, 0, 0)
    due = datetime.date(int(due_list[0]), int(due_list[1]), int(due_list[2]))
    
    print "Dates: ", starts, ends, due
    
    # TODO: repair query (returns no records or incomplete)
    # As the time value query is datetime based,
    # exact day matching does not work
    
    q = (db.operation.customer_id == customer_id) & (db.operation.supplier_id == supplier_id) & (db.operation.posted >= starts) & (db.operation.posted <= ends)
    q &= ((db.operation.due_date <= due) | (db.operation.due_date == None))

    # list items with text box (multiple selection)
    # form = SQLFORM.factory(Field("operations", "list:reference operation", requires = IS_IN_DB(operations, "operation.operation_id", "%(document_id)s        %(number)s:        %(amount)s", multiple = True)))

    s = db(q)
    operations = s.select()

    # Values is the array with operations and amounts from the operations query
    # values = dict( int operation_id = [float debit, float credit, float debit -credit], ... )
    
    values = operations_values(operations)
    print "Values: %s" % values    

    trows = []
    for operation in operations:
        trows.append(TR(TD(operation.document_id.description), TD(operation.operation_id), TD(operation.posted), TD(operation.due_date), TD(values[operation.operation_id][0]), TD(values[operation.operation_id][1]), TD(values[operation.operation_id][2]), TD(INPUT(_type="checkbox", _name="operation_%s" % operation.operation_id))))
    
    tbody = TBODY(*trows)
    table = TABLE(THEAD(TR(TH("Document"), TH("Number"), TH("Date"), TH("Due date"), TH("Debit"), TH("Credit"), TH("Difference"), TH("Select"))), tbody)
    
    form = FORM(SELECT(OPTION("Apply", _value="apply"), OPTION(payment_label, _value="payment"), _name="selection_action"), table, INPUT(_type="submit"))
    if form.accepts(request.vars, session):
        # TODO: apply/pay/collect actions

        # Get the selected operations or
        # Set the whole list as target
        operation_ids = [int(k.split("_")[1]) for k in request.vars if k.startswith("operation_")]

        # if there are selected items
        # clean the values array of unselected operations
        new_values = dict()
        
        if len(operation_ids) > 0:
            for k in values:
                if k in operation_ids:
                    # add item from values
                    new_values[k] = values[k]
            # add values array to session
            session.current_accounts_values = new_values
        else:
            session.current_accounts_values = values

        print "Operation id(s): %s" % str(operation_ids)
        print "Form data: %s" % request.vars
        print "Selection action: %s" % request.vars.selection_action
        if request.vars.selection_action == "payment":
            redirect(URL(f="current_accounts_payment"))

    return dict(form = form)


def current_accounts_payment():
    if session.current_accounts_type == "S":
        point_of_sale_id = db(db.option.name == "purchases_payment_point_of_sale_id").select().first().value
        operation_type = "P"
        invert_value = -1

    elif session.current_accounts_type == "C":
        point_of_sale_id = db(db.option.name == "sales_payment_point_of_sale_id").select().first().value
        operation_type = "S"
        invert_value = 1

    # get the default payment terms for current accounts
    payment_terms_id = db(db.option.name == "current_account_payment").select().first().value

    # document widget settings
    s = db(db.document.point_of_sale_id == point_of_sale_id)
    i = "document.document_id"
    f = "%(description)s"

    # calculate difference from values array
    values = session.current_accounts_values
    
    difference = sum([values[v][2] for v in values], 0.0) * invert_value
    print "Calculated difference: %s" % difference

    # pre-operation form
    form = SQLFORM.factory(Field("document", "reference document", requires = IS_IN_DB(s, i, f)), Field("amount", "double", default = difference), Field("concept", "reference concept", requires = IS_IN_DB(db(db.concept.current_account == True), "concept.concept_id", "%(description)s")), Field("payment_terms", "reference payment_terms", requires = IS_IN_DB(db(db.payment_terms.payment_terms_id != None), "payment_terms.payment_terms_id", "%(description)s")))
    
    if form.accepts(request.vars, session):
        # create the operation with stored user options
        # insert the current accounts movement
        # and redirect to the operation detail form

        # todo: auto operation values (fund, subcustomer, other)

        # receipt payment terms
        if len(request.vars.payment_terms) > 0:
            payment_terms_id = request.vars.payment_terms

        # get the concept db record
        concept = db.concept[request.vars.concept]

        # current account movement amount
        amount = float(request.vars.amount)

        # new receipt/current accounts operation
        operation_id = db.operation.insert(customer_id = session.current_accounts_customer, supplier_id = session.current_accounts_supplier, document_id = request.vars.document, type = operation_type, payment_terms_id = payment_terms_id)

        # current accounts movement
        db.movement.insert(operation_id = operation_id, amount = amount, value = amount, quantity = 1, concept_id = concept.concept_id)
        session.operation_id = operation_id

        print "Operation details: %s" % str(db.operation[operation_id])
        
        redirect(URL(c="operations", f="movements_detail"))

    return dict(form = form)
