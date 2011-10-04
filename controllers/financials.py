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
            except RuntimeError, e:
                print str(e)
                    
            difference = entry -exit
        values[operation.operation_id] = [entry, exit, difference]
   
    return values

def index(): return dict(message="hello from financials.py")

def current_accounts_type():
    """ Lets the user choose the type
    of current account administration """
    form = SQLFORM.factory(Field("current_accounts_type", requires = IS_IN_SET({"C":"Customer", "S":"Supplier"}), widget = SQLFORM.widgets.radio.widget, default = "C"))
    if form.accepts(request.vars, session):
        print "%s was chosen" % request.vars.current_account_type
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
    
    form = SQLFORM.factory(Field(n, requires = IS_IN_DB(s, i, f)), Field("starts", "date", default = start), Field("ends", "date", default = today), Field("due", "date", default = today), Field("complete", "boolean"))
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
                
                print "Session data: %s" % session
                redirect(URL(f="current_accounts_detail"))
                
    return dict(form = form)


def current_accounts_detail():
    """ List of current accounts operations"""
    if session.current_accounts_type == "C":
        supplier_id = db(db.option.name == "default_supplier_id").select().first().value
        customer_id = session.current_accounts_customer
    elif session.current_accounts_type == "S":
        supplier_id = session.current_accounts_supplier
        customer_id = db(db.option.name == "default_customer_id").select().first().value
    
    print "Session data: %s" % session
    
    # convert date string iso values
    starts_list = session.current_accounts_starts.split("-")
    ends_list = session.current_accounts_ends.split("-")
    due_list = session.current_accounts_due.split("-")
    
    starts = datetime.date(int(starts_list[0]), int(starts_list[1]), int(starts_list[2]))
    ends = datetime.date(int(ends_list[0]), int(ends_list[1]), int(ends_list[2]))
    due = datetime.date(int(due_list[0]), int(due_list[1]), int(due_list[2]))
    
    print "Dates: ", starts, ends, due
    
    # TODO: repair query (returns no records or incomplete)
    q = (db.operation.customer_id == customer_id) & (db.operation.supplier_id == supplier_id) & (db.operation.posted >= starts) & (db.operation.posted <= ends) & (db.operation.due_date <= due)
    
    # list items with text box (multiple selection)
    # form = SQLFORM.factory(Field("operations", "list:reference operation", requires = IS_IN_DB(operations, "operation.operation_id", "%(document_id)s        %(number)s:        %(amount)s", multiple = True)))

    s = db(q)
    operations = s.select()
    
    values = operations_values(operations)
    print "Values: %s" % values    

    trows = []
    for operation in operations:
        trows.append(TR(TD(operation.document_id), TD(operation.number), TD(operation.posted), TD(operation.due_date), TD(values[operation.operation_id][0]), TD(values[operation.operation_id][1]), TD(values[operation.operation_id][2]), TD(INPUT(_type="checkbox", _name="operation_%s" % operation.operation_id))))
    
    tbody = TBODY(*trows)
    table = TABLE(THEAD(TR(TH("Document"), TH("Number"), TH("Date"), TH("Due date"), TH("Debit"), TH("Credit"), TH("Difference"), TH("Select"))), tbody)
    
    form = FORM(LABEL("Apply", _for="apply"), INPUT(_type="checkbox", _name="apply"), LABEL("Payment", _for="payment"), INPUT(_type="checkbox", _name="payment"), table, INPUT(_type="submit"))
    if form.accepts(request.vars, session):
        # TODO: apply/pay/collect actions
        print "Form data: %s" % request.vars
        
    return dict(form = form)
