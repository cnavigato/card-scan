# -*- coding: utf-8 -*-


if not request.env.web2py_runtime_gae:
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
else:
    db = DAL('google:datastore')
    session.connect(request, response, db=db)





