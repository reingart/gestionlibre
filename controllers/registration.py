# coding: utf8
# intente algo como
def index(): return dict(message="hello from registration.py")

def post_register_specify_firm():
    form = FORM(INPUT(_name="firm_tin"), INPUT(_type="submit"))
    if form.accepts(request.vars, session):
        contact = db(db.contact.tin == request.vars["firm_tin"]).select().first()
        if contact and auth.user_id:
            db.contactuser.insert(user=auth.user_id, contact=contact, description=db.auth_user[auth.user_id].email)
            response.flash = T("Registration successful")
    return dict(form=form)
