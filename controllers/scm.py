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
    requires=IS_EMPTY_OR(IS_IN_DB(db, db.warehouse, \
    '%(description)s'))), \
    Field('product', 'reference concept', \
    requires = IS_EMPTY_OR(IS_IN_DB(db(\
    db.concept.orderable == True), \
    'concept.concept_id', '%(description)s')))
    )

    # Query for the stock list
    if stock_query_form.accepts(request.vars, session, \
    keepvalues = True, \
    formname="stock_query_form"):
        q = None
        warehouse_query = db.stock.warehouse_id == \
        request.vars.warehouse
        product_query = db.stock.concept_id == \
        request.vars.product
        # filter by product if requested
        if len(request.vars.product) > 0:
            q = product_query

        if len(request.vars.warehouse) > 0:
            if q is None:
                q = warehouse_query
            else:
                q &= warehouse_query

        if q is None: q = db.stock

        # stock list records
        s = db(q)
        rows = s.select()

        # TODO: presentation code should go into the view
        columns = ['stock.stock_id', 'stock.code', \
        'stock.concept_id', \
        'stock.posted', 'stock.value']
        headers = {'stock.stock_id': 'Edit', 'stock.code': 'Code', \
        'stock.concept_id': 'Product', 'stock.posted': 'Posted', \
        'stock.value': 'Value'}

        # TODO: unify action/function naming conventions
        stock_list = SQLTABLE(rows, columns = columns, \
        headers = headers, \
        linkto=URL(c="scm", f="stock_item_update"))

    # TODO: increase/decrease stock by product/warehouse and
    # inter warehouse transactions
    
    # Move stock
    stock_movement_form = SQLFORM.factory(\
    Field('product', 'reference concept', \
    requires = IS_IN_DB(db(db.concept.orderable == True), \
    'concept.concept_id', '%(description)s')), \
    Field('warehouse', 'reference warehouse', \
    requires=IS_IN_DB(db, db.warehouse, '%(description)s')), \
    Field('destination', 'reference warehouse', \
    requires=IS_IN_DB(db, db.warehouse, \
    '%(description)s')), Field('quantity', \
    'double', \
    requires=IS_FLOAT_IN_RANGE(-1e6, 1e6)), \
    )
    if stock_movement_form.accepts(request.vars, session, \
    keepvalues = True, \
    formname="stock_movement_form"):
        stock_item_source = db((\
        db.stock.concept_id == request.vars.product) & (\
        db.stock.warehouse_id == request.vars.warehouse)).select(\
        ).first()
        if request.vars.warehouse == request.vars.destination:
            response.flash = "Please choose different warehouses"
        elif stock_item_source is not None:
            tmp_stock_value = stock_item_source.value - float(\
            request.vars.quantity)
            if tmp_stock_value < 0:
                # negative stock
                response.flash = \
                "Insufficient source stock quantity"
            else:
                # get or create a stock            
                stock_item_destination = db((\
                db.stock.warehouse_id == request.vars.destination\
                ) & (\
                db.stock.concept_id == request.vars.product)\
                ).select().first()
                if stock_item_destination is None:
                    stock_item_destination_id = db.stock.insert(\
                    warehouse_id = request.vars.destination, \
                    concept_id = request.vars.product, value = 0.0)
                else:
                    stock_item_destination_id = \
                    stock_item_destination.stock_id
                    
                stock_item_source.update_record(\
                value = stock_item_source.value - \
                float(request.vars.quantity))
                old_value = float(\
                db.stock[stock_item_destination_id].value)
                db.stock[stock_item_destination_id].update_record(\
                value = old_value + float(request.vars.quantity))
                response.flash = "Stock updated"
        else:
            # the item does not exist
            response.flash = \
            "The item specified was not found in the warehouse"
    
    # Change stock value
    change_stock_form = SQLFORM.factory(
    Field('product', 'reference concept', \
    requires = IS_IN_DB(db(db.concept.orderable == True), \
    "concept.concept_id", "%(description)s")), \
    Field('warehouse', 'reference warehouse', \
    requires=IS_IN_DB(db, db.warehouse, '%(description)s')), \
    Field('quantity', 'double', \
    requires=IS_FLOAT_IN_RANGE(-1e6, +1e6)), \
    )

    if change_stock_form.accepts(request.vars, \
    session, keepvalues=True, formname="change_stock_form"):
        stock_item = db((\
        db.stock.concept_id == request.vars.product) & \
        (db.stock.warehouse_id == request.vars.warehouse\
        )).select().first()
        if stock_item is None:
            stock_item_id = db.stock.insert(\
            warehouse_id = request.vars.warehouse, \
            concept_id = request.vars.product, value = 0.0)
        else:
            stock_item_id = stock_item.stock_id

        tmp_value = db.stock[stock_item_id].value + \
        float(request.vars.quantity)
        
        if tmp_value < 0:
            response.flash = "Insufficient stock value."
        else:
            db.stock[stock_item_id].update_record(\
            value = tmp_value)
            response.flash = "Stock value changed"
            
    return dict(stock_list = stock_list, \
    stock_query_form = stock_query_form, \
    stock_movement_form = stock_movement_form, \
    change_stock_form = change_stock_form)

def stock_item_update():
    form = crud.update(db.stock, request.args[1])
    if form.accepts(request.vars, session, keepvalues = True):
        response.flash = "Record updated"
    return dict(form = form)
