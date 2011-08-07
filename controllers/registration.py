# coding: utf8
# intente algo como
def index(): return dict(message="hello from registration.py")

def post_register_specify_firm():
    form = FORM(INPUT(_name="firm_tax_id"), INPUT(_type="submit"))
    if form.accepts(request.vars, session):
        contact = db(db.contact.tax_identification == request.vars["firm_tax_id"]).select().first()
        if contact and auth.user_id:
            db.contact_user.insert(user_id=auth.user_id, contact_id=contact, description=db.auth_user[auth.user_id].email)
            response.flash = T("Registration successful")
    return dict(form=form)
