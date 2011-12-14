# coding: utf8
# intente algo como

import crm
import datetime


def index(): return dict(message="hello from crm.py")

@auth.requires_login()
def customer_panel():
    """ Customer on-line panel. Show info/stats/links to actions"""
    contact_user = db(db.contact_user.user_id == auth.user_id).select().first()
    if contact_user is None:
        return dict(customer_orders = None, message=T("No tax id selected"), customer = None)
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

    return dict(customer_orders = customer_orders, message=T("Customer panel"), customer = customer)


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
    'reference subcustomer', requires=IS_EMPTY_OR(IS_IN_DB(db, db.subcustomer, "%(legal_name)s"))))
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
                response.flash = T("Error: could not calculate\
                 the total debt.")
                break
                
        columns = ["operation.operation_id", "operation.posted", \
        "operation.amount", "operation.customer_id", \
        "operation.subcustomer_id", "document.description"]
        headers = { "operation.operation_id": T("Edit"), \
        "operation.posted": T("Posted"), "operation.amount": T("Amount"), \
        "operation.customer_id": T("Customer"), \
        "operation.subcustomer_id": T("Subcustomer"), \
        "document.description": T("Document") }
               
        operations = SQLTABLE(the_set.select(), columns=columns, \
        headers=headers, linkto=URL(c="operations", f="ria_movements"))
    return dict(query_form = query_form, operations = operations, \
    total_debt = total_debt)


def new_customer():
    form = crud.create(db.customer)
    return dict(form = form)

def new_subcustomer():
    form = crud.create(db.subcustomer)
    return dict(form = form)

def customer_current_account_status():
    if request.args[0] == "customer":
        customer = db.customer[request.args[1]]
        value = crm.customer_current_account_value(db, \
        customer.customer_id)
    elif request.args[0] == "subcustomer":
        customer = db.subcustomer[request.args[1]]
        value = crm.subcustomer_current_account_value(db, \
        customer.subcustomer_id)
        
    return dict(value = value, customer = customer)
    