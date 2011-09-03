# -*- coding: utf-8 -*-
# intente algo como
import datetime
from operations import process

def index():
    return dict()

def stock():
    stock_list = None
    stock_query_form = SQLFORM.factory(
    Field('warehouse', 'reference warehouse', \
    requires=IS_IN_DB(db, db.warehouse, '%(description)s')), \
    Field('product', 'reference concept', \
    requires = IS_EMPTY_OR(IS_IN_DB(db(db.concept.orderable == True), \
    'concept.concept_id', '%(description)s')))
    )

    # Query for the stock list
    if stock_query_form.accepts(request.vars, session, \
    keepvalues = True, \
    formname="stock_query_form"):
        q = db.stock.warehouse_id == request.vars.warehouse
        # filter by product if requested
        if len(request.vars.product) > 0:
            q &= db.stock.concept_id == request.vars.product

        # stock list records
        s = db(q)
        rows = s.select()

        # TODO: presentation code should go into the view
        columns = ['stock.stock_id', 'stock.code', 'stock.concept_id', \
        'stock.posted', 'stock.value']
        headers = {'stock.stock_id': 'Edit', 'stock.code': 'Code', \
        'stock.concept_id': 'Product', 'stock.posted': 'Posted', \
        'stock.value': 'Value'}

        # TODO: unify action/function naming conventions
        stock_list = SQLTABLE(rows, columns = columns, headers = headers, \
        linkto=URL(c="scm", f="stock_item_update"))

    # TODO: increase/decrease stock by product/warehouse and
    # inter warehouse transactions

    return dict(stock_list = stock_list, \
    stock_query_form = stock_query_form)

