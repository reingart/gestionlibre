# coding: utf8
# intente algo como

def invoice(): 
    form = SQLFORM.factory(
        Field("customer_id", db.customer, label=T("Customer"),requires=IS_IN_DB(db, "customer.id", "%(name)s")),
        Field("document_id", db.document, label=T("Document"),requires=IS_IN_DB(db, "document.id", "%(name)s")),
        Field("date", "date", label=T("Date")),
        Field("number", "number", label=T("Number"), default=1),
        )
    
    return dict(form=form)
    
def concept(): 
    form = SQLFORM.factory(
        Field("concept_id", db.customer, label=T("Concept"),requires=IS_IN_DB(db, "concept.id", "%(name)s")),
        Field("quantity", "double", label=T("Quantity")),
        Field("price", "double", label=T("Price")),
        Field("subtotal", "double", label=T("Subtotal")),
        Field("detail", "text", label=T("Text")),
        )
    
    return dict(form=form)
