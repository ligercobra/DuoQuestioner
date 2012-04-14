#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import cgi
import cgitb
import urllib2
import sys
import time
import datetime

import models
import utils

#Show error as a page description
sys.stderr = sys.stdout
#Enable debug output
cgitb.enable

ul = models.UserSelect()
mnck = utils.ManageCookie()
form = cgi.FieldStorage()

#Login
if(("regid" in form) and ("upass" in form)):
    if(not utils.check_userauth(form.getfirst("regid",""),
                                form.getfirst("upass",""))):
        utils.to_login()
    
    regid = form.getfirst("regid","")
    upass = form.getfirst("upass","")
    res = models.UserLogin()
    check = res.login(mregid=regid,mpasswd=upass)

    if(check):
        res = models.UserInfo()
        uinfo = res.get_uinfo(mregid=regid,mseskey=check)
        mnck.destroy_allck()
        mnck.set_ck(regid=uinfo["regid"])
        mnck.set_ck(seskey=uinfo["seskey"])
        mnck.print_ck()
        utils.to_home()
        sys.exit()

mnck.destroy_allck()
mnck.set_ck(login_e="1")
mnck.print_ck()
utils.to_login()
sys.exit()
