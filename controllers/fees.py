# coding: utf8
# intente algo como
def index(): return dict(message="hello from fees.py")

def list_fees():
    return dict(fees = SQLTABLE(db(db.fee).select(), \
    columns = ["fee.fee_id", "fee.code", "fee.description", \
    "fee.due_date", "fee.document_id", "fee.starting", "fee.ending"], \
    headers = {"fee.fee_id": "Edit", "fee.code": "Code", \
    "fee.description": "Description", "fee.due_date": "Due date", \
    "fee.document_id": "Document", "fee.starting": "Starting", \
    "fee.ending": "Ending"}, \
    linkto=URL(c="fees", f="update_fee")))
    
def update_fee():
    form = crud.update(db.fee, request.args[1])
    return dict(form = form)
    
def create_fee():
    form = crud.create(db.fee)
    return dict(form = form)

def list_installments():
    operation = db.operation[session.operation_id]
    
    query = (db.installment.customer_id == operation.customer_id)
    query |= (db.installment.subcustomer_id == operation.subcustomer_id)
    query |= (db.installment.supplier_id == operation.supplier_id)

    preset = db(query)
    return dict(installments = SQLTABLE(preset.select(), \
    columns = ["installment.installment_id","installment.customer_id",\
    "installment.subcustomer_id","installment.supplier_id", \
    "installment.fee_id", "installment.quotas"], \
    headers = {"installment.installment_id": "Edit", \
    "installment.customer_id": "Customer",\
    "installment.subcustomer_id": "Subcustomer", \
    "installment.supplier_id": "Supplier", \
    "installment.fee_id": "Fee", "installment.quotas": "Quotas"}, \
    linkto=URL(c="fees", f="update_installment")))
    
def update_installment():
    session.installment_id = int(request.args[1])
    return dict(form = crud.update(db.installment, request.args[1]))

def list_quotas():
    return dict(quotas = SQLTABLE(db(\
    db.quota.installment_id == session.installment_id).select(), \
    columns = ["quota.quota_id","quota.number",\
    "quota.due_date", \
    "quota.fee_id", "quota.amount"], \
    headers = {"quota.quota_id": "Edit","quota.number": "Number",\
    "quota.due_date": "Due date", \
    "quota.fee_id": "Fee", "quota.amount": "Quota"}, \
    linkto=URL(c="fees", f="update_quota.html")))
    
def update_quota():
    form = crud.update(db.quota, request.args[1])
    return dict(form = form)
