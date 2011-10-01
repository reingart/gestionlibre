#! /usr/env python
# -*- coding: utf-8 -*-
from gluon import *


def current_account_value(db, operations):
    """ Calculates the current account value
    for the customer specified

    arguments:
    db: DAL object
    operations: rows object with all
    customer/subcustomer operations
    """

    value = 0.0
    for operation in operations:
        invert_value = 1
        if operation.document_id.invert == True:
            invert_value = -1
        movements = db(db.movement.operation_id == \
        operation.operation_id).select()
        
        for movement in movements:
            try:
                # Filter current_account movements
                if movement.concept_id.current_account != True:
                    if movement.concept_id.entry == True:
                        value += \
                        invert_value*float(movement.amount)
                    elif movement.concept_id.exit == True:
                        value += \
                        invert_value*float(movement.amount)*(-1)
                        
            except (ValueError, TypeError, AttributeError, RuntimeError), e:
                print \
                "Current account value: error calculating movement id %s: %s" \
                % (movement.movement_id, str(e))

    return value

def customer_current_account_value(db, customer_id):
    operations = db(db.operation.customer_id == customer_id).select()
    value = current_account_value(db, operations)
    return value

def subcustomer_current_account_value(db, subcustomer_id):
    operations = db(db.operation.subcustomer_id == subcustomer_id).select()
    value = current_account_value(db, operations)    
    return value

