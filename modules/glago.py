# -*- coding: utf-8 -*-

LEGACY_TABLES = {\
"Cuentas.csv": {"table_name": "account", "fields": [("id", 0),("code", 1), ("description", 2),("receives", 3), ("contactgroup", 4),("bank", 5),("vat", 6),("grossreceipts", 7), ("collections", 8),("retentions", 9),("replica", 11)] },
"Ejercicios.csv": {"table_name": "accountingperiod", "fields": [("id",0), ("description", 1),("fromdate", 2), ("todate", 3), ("replica", 4)]},
"Asientos.csv": {"table_name": "journalentry", "fields": [("id",0), ("number",1), ("description",2), ("date",3), ("source",4), ("type",5), ("draft",6), ("accountingperiod",7), ("replica",8)]},
"Partidas.csv": {"table_name": "accountingentry", "fields": [("id",0), ("description",1), ("journalentry",2), ("account",3), ("type",4), ("amount",5), ("replica",6)]},
"IVAs.csv": {"table_name": "vat", "fields": [("id",0), ("description",1), ("category",1), ("abbr",2), ("discriminate",3), ("documentsales",4), ("documentpurchases",5), ("replica",6)]},
"Rubros.csv": {"table_name": "item", "fields": [("id",0), ("description",1), ("code",2), ("products",3), ("units",4), ("times",5), ("replica",6)]},
"SubRubro.csv": {"table_name": "subitem", "fields": [("id",0), ("code",1), ("description",2)]},
"Jurisdicciones.csv": {"table_name": "jurisdiction", "fields": [("id",0), ("description",1)]},
"Deudores.csv": {"table_name": "customer", "fields": [("id",0), ("code",1), ("description",2), ("firmname",3), ("vat",4), ("tin",5), ("ssn",6), ("address",7), ("zipcode",8), ("city",9), ("state",10), ("country",11), ("fax",12), ("telephone",13), ("paymentterms",14), ("pricelist",15), ("salesperson",16), ("currentaccount",17),  ("situation",18), ("contactgroup",19), ("observations",20), ("placeofdelivery",21), ("transport",23), ("contact",24), ("purveyor",25), ("addition",27), ("replica",28), ("deletion",29), ("currentaccountlimit",30), ("checklimit", 31), ("jurisdiction", 32)]},
"CLIENTES.csv": {"table_name": "subcustomer", "fields": [("id",0), ("code",0), ("firmname",1), ("address",2), ("telephone",5), ("tin",7), ("balance",8), ("currentaccountlimit",9), ("observations",11)]},
"Grupos.csv": {"table_name": "contactgroup", "fields": [("id",0), ("description",1), ("replica",2)]},
"Contactos.csv": {"table_name": "contact", "fields": [("id",0), ("description",1), ("customer",2), ("purveyor",3), ("department",4), ("telephone",5), ("fax",6), ("email",7), ("shcedule",8), ("address",9), ("zipcode", 10), ("city", 11), ("state", 12), ("observations", 13), ("replica", 14)]},
"Situaciones.csv": {"table_name": "situation", "fields": [("id",0), ("description",1), ("replica",2), ]},
"Vendedores.csv": {"table_name": "salesperson", "fields": [("id",0), ("description",1), ("telephone",2), ("address",3), ("state",4), ("notes",5), ("replica",6), ("commission",7)]},
"Fondos.csv": {"table_name": "fund", "fields": [("id",0), ("description",1), ("type",2), ("upperlimit",3), ("balance",4), ("closed",5), ("currentaccount", 6), ("bankchecks", 7), ("concept", 8), ("account", 9), ("replica", 10)]},
"Bancos.csv": {"table_name": "bank", "fields": [("id",0), ("code",1), ("description",2), ("bankcheck",3), ("replica",5), ("concept",4)]},
"Conciliaciones.csv": {"table_name": "reconciliation", "fields": [("id",0), ("concept",1), ("date",2), ("amount",3), ("activity",4), ("addition",5), ("deletion",6), ("replica",7)]},
"Cierres.csv": {"table_name": "cashbalance", "fields": [("id",0), ("date",1), ("balance",2), ("canceled",3), ("prints",4), ("transactionrecord1",5), ("transactionrecord2",6), ("pages",7), ("cash",8), ("fund",9),("replica",10)]},
"CondicionesPago.csv": {"table_name": "paymentterms", "fields": [("id",0), ("description",1), ("canceled",5), ("concept",6), ("currentaccount",7), ("replica",8)]},
"FormasPago.csv": {"table_name": "paymentmethod", "fields": [("id",0), ("description",1), ("concept",2), ("coupons",98)]},
\
"Valores.csv": {"table_name": "bankcheck", "fields": [("id",0), ("customer",1), ("purveyor",2), ("number",3), ("bank",4), ("amount",5), ("addition",6), ("duedate",7), ("deletion",8), ("paid",9), ("exchanged",10), ("bouncer",11), ("transactionrecord",12), ("id1",13), ("exit",14), ("rejection",15), ("concept",16), ("detail",17), ("bd",18), ("own",19), ("balance",20), ("replica",21)]},\
\
"Comprobantes.csv": {"table_name": "documenttype", "fields": [("id",0), ("description",1), ("pointofsale",2), ("abbr",3), ("type",4), ("tax",5), ("discriminate",6), ("branch",7), ("number",8), ("entry",9), ("exit",10), ("fiscal",11), ("stock",12), ("currentaccount",13), ("cash",14), ("debit",15), ("credit",16), ("invoices",17), ("receipts",18), ("packingslips",19), ("orders",20), ("countable",21), ("printer",22), ("lines",23), ("fund",24), ("replicate",25), ("replica",26), ("notes",27), ("descriptions",28), ("cashbox",31), ("books",32), ("form",33), ("budget",34), ("downpayment",35), ("confirmprinting",37), ("internal",38), ("invert",39), ("concept",40), ("continuous",41), ("multiplepages",42), ("preprinted",43)]},
"Conceptos.csv": {"table_name": "concept", "fields": [("id",0), ("code",1), ("description",2), ("item",3), ("quantity",4), ("amount",5), ("vat",6), ("family",8), ("color",9), ("size",10), ("account",11), ("addition",12), ("measure",13), ("desired",14), ("customer",15), ("purveyor",16), ("presentation",17), ("description",18), ("entry",19), ("exit",20), ("taxed",21), ("stock",22), ("unitary",23), ("internal",24), ("paymentmethod",25), ("tax",26), ("currentaccount",27), ("cashbox",28), ("extra",29), ("cash",30), ("banks",31), ("receipt",32), ("statement",33), ("abbr",34), ("quantity",35), ("replica",36), ("floor",37), ("suspended",38), ("discounts",39), ("surcharges",40), ("subitem",41)]},
"Operaciones.csv": {"table_name": "transactionrecord", "fields": [("id",0), ("customer",1), ("purveyor",2), ("subcustomer",3), ("salesperson",4), ("detail",6), ("paymentterms",7), ("term",8), ("amount",9), ("balance",14), ("date",15), ("issue",16), ("documenttype",17), ("branch",18), ("number",19), ("duedate",20), ("documenttype",22), ("canceled",23), ("processed",24), ("voided",25), ("replicated",26), ("fund",27), ("module",29), ("purveyor",33), ("observations",35), ("description",36), ("cancellation",37), ("avoidance",38), ("file",39), ("liquidation",40), ("user",41), ("hour",42), ("replica",45), ("replicated",46), ("jurisdiction",50)]},
"Movimientos.csv": {"table_name": "activity", "fields": [("id",0), ("transactionrecord",1), ("concept",2), ("price",3), ("quantity",4), ("amount",5), ("discriminated",6), ("tablenumber",7), ("detail",9), ("value",10), ("start",11), ("replica",12), ("discount",13), ("surcharge",14)]},
"ListasPrecio.csv": {"table_name": "pricelist", "fields": [("id",0), ("description",1), ("entry",2), ("exit",3), ("replica",4)]},
"Precios.csv": {"table_name": "price", "fields": [("id",0), ("concept",1), ("pricelist",2), ("item",3), ("salesperson",4), ("customer",5), ("purveyor",6), ("contactgroup",7), ("situation",8), ("fund",9), ("rate",10), ("paymentmethod",11), ("documenttype",12), ("taxed",13), ("vat",14), ("type",15), ("value",16), ("calculate",17), ("operation",18), ("source",19), ("condition",20), ("quantity1",21), ("quantity2",22), ("discriminate",23), ("priority",25), ("replica",26)]},
"Talonarios.csv": {"table_name": "pointofsale", "fields": [("id",0), ("description",1), ("branch",2), ("number",3), ("pac",4), ("duedate",5), ("replica",6)]},
"Acreedores.csv": {"table_name": "purveyor", "fields": [("id",0), ("description",1), ("firmname",3), ("vat",4), ("tin",5), ("address",6), ("zipcode",7), ("city",8), ("state",9), ("telephone",10), ("fax",11), ("observations",12), ("replica",13), ("jurisdiction",14)]},
"Colecciones.csv": {"table_name": "collection", "fields": [("id",0), ("description",1), ("fromdate",2), ("todate",3), ("replica",4)]},
"Colores.csv": {"table_name": "color", "fields": [("id",0), ("code",1), ("description",2), ("replica",3)]},
"Talles.csv": {"table_name": "size", "fields": [("id",0), ("type",1), ("code",2), ("ordernumber",4), ("replica",6)]},
"Depositos.csv": {"table_name": "warehouse", "fields": [("id",0), ("description",1), ("address",2), ("replica",3)]},
\
"Stock.csv": {"table_name": "stock", "fields": [("value",4), ("date",5), ("accumulated",12), ("replica",13), ("reserved",14), ("concept",1), ("warehouse",10), ("id",0)]},\
\
"INVENTARIO.csv": {"table_name": "product", "fields": [("id",0), ("description",1)]},\
\
}

def dict_to_csv(arg):
    f = open("glago_convert_fields.csv", "w")
    for k, v in LEGACY_TABLES.iteritems():
        for fd in v["fields"]:
            tmpstring = ""            
            tmpstring += "%s, %s, %s, %s" % (str(k), str(v["table_name"]), str(fd[0]), str(fd[1]))
            tmpstring += "\n"
            f.write(tmpstring)
    f.close()
