# coding: utf8
# intente algo como
def index(): return dict(message="hello from crm.py")

def current_account_report():
    """ Performs a query of operations and
    returns the current account data
    """
    # 
    total_debt = 0
    
    operations = None
    # customer / subcustomer selection form
    query_form = SQLFORM.factory(Field('customer', 'reference customer', \
    requires=IS_IN_DB(db, db.customer, "%(legal_name)s")), Field('subcustomer', \
    'reference subcustomer', requires=IS_IN_DB(db, db.subcustomer, "%(legal_name)s")))
    if query_form.accepts(request.vars, session, keepvalues=True, formname="query_form"):
        q = ((db.operation.customer_id == request.vars.customer) | \
            (db.operation.subcustomer_id == request.vars.subcustomer))
        q &= (db.operation.document_id == db.document.document_id)
        q &= ((db.document.receipts == True) | (db.document.invoices == True))

        the_set = db(q)

        # a naive current account total debt
        # TODO: complete and customizable current
        # account processing
        
        for row in the_set.select():
            try:
                if row.document.receipts == True:
                    total_debt -= row.operation.amount
                elif row.document.invoices == True:
                    total_debt += row.operation.amount
            except (ValueError, TypeError):
                response.flash = "Error: could not calculate\
                 the total debt."
                break
                
        columns = ["operation.operation_id", "operation.posted", \
        "operation.amount", "operation.customer_id", \
        "operation.subcustomer_id", "document.description"]
        headers = { "operation.operation_id": "Edit", \
        "operation.posted": "Posted", "operation.amount": "Amount", \
        "operation.customer_id": "Customer", \
        "operation.subcustomer_id": "Subcustomer", \
        "document.description": "Document" }
               
        operations = SQLTABLE(the_set.select(), columns=columns, \
        headers=headers, linkto=URL(c="operations", f="movements"))
    return dict(query_form = query_form, operations = operations, \
    total_debt = total_debt)