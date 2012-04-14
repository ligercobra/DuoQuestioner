#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import cgi
import cgitb
import urllib2
import sys
import time
import datetime
from dateutil.relativedelta import *

import utils
import models

def form_ref(mform):
    if(("regid" in mform) and ("upass" in mform)):
        if(mform.getfirst("regid","") !="" and (mform.getfirst("upass","") != "")):
            return True
    return False

form = cgi.FieldStorage()
ulauth = models.UserRegist()
mnck = utils.ManageCookie()

'''
check form
'''
if(not form_ref(form)):
    mnck.destroy_allck()
    mnck.print_ck()
    utils.to_login()
    sys.exit()

tmp_regid = form.getfirst("regid","").decode("utf-8")
tmp_password = form.getfirst("upass","").decode("utf-8")

if(not utils.check_userauth(tmp_regid,tmp_password)):
    mnck.destroy_allck()
    mnck.set_ck(ureg="2")
    mnck.print_ck()
    utils.to_login()
else:
    if(ulauth.userinsert(tmp_regid,tmp_password)):
        mnck.destroy_allck()
        mnck.set_ck(ureg="1")
        mnck.print_ck()
        utils.to_login()
    else:
        mnck.destroy_allck()
        mnck.set_ck(ureg="0")
        mnck.print_ck()
        utils.to_login()
sys.exit()
