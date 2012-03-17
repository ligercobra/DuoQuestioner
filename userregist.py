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
from dateutil.relativedelta import *

#from view import UserView
from Model import UserLogic
from Model import SumParts
from Model import UserLogin

'''
formに正しく値が入っているか
'''
def form_ref(mform):
    if(("regid" in mform) and ("upass" in mform)):
        return True
    else:
        return False

ck = SimpleCookie()
ck.load(os.environ.get("HTTP_COOKIE",""))
form = cgi.FieldStorage()
sump = SumParts.SumParts()
trans = SumParts.Transporter()
ulauth = UserLogin.UserRegist()

'''
formをチェックし空ならエラー
'''
if(not form_ref(form)):
    trans.to_registuser_result(fl=False)

tmp_regid = form.getfirst("regid","").decode("utf-8")
tmp_password = form.getfirst("upass","").decode("utf-8")

'''
入力された文字列をチェック
'''
if(not sump.check_userauth(tmp_regid,tmp_password)):
    trans.to_registuser_result(fl=False)
else:
    if(ulauth.userinsert(tmp_regid,tmp_password)):
        trans.to_registuser_result(fl=True)
    else:
        trans.to_registuser_result(fl=False)

