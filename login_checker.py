#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import cgi
import cgitb
import urllib2
from Cookie import SimpleCookie
import sys
import time
import datetime

#from view import UserView
from Model import SumParts
from Model import UserLogin

#Show error as a page description
sys.stderr = sys.stdout
#Enable debug output
cgitb.enable


ck = SimpleCookie()
ck.load(os.environ.get("HTTP_COOKIE",""))

form = cgi.FieldStorage()

#Login
if(("regid" in form) and ("upass" in form)):
    sparts = SumParts.SumParts()
    trans = SumParts.Transporter()
    title=form.getfirst("regid","")
    username = form.getfirst("upass","")
    if(not sparts.check_userauth(form.getfirst("regid",""),
                                form.getfirst("upass",""))):
        trans.to_login_failed()
    regid = form.getfirst("regid","")
    upass = form.getfirst("upass","")
    res = UserLogin.UserLogin()
    check = res.login(mregid=regid,mpasswd=upass)

    if(check):
        res = UserLogin.UserInfo()
        uinfo = res.get_uinfo(mregid=regid,mseskey=check)
        trans.set_ck(regid=uinfo["regid"])
        trans.set_ck(seskey=uinfo["seskey"])
        trans.to_myhome()
    else:
        trans.to_login_failed()
else:
    trans.to_login_failed()
