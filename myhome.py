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
import tempita

#from view import UserView
from Model import UserLogic
from Model import SumParts
from Model import UserLogin

#Show error as a page description
sys.stderr = sys.stdout
#Enable debug output
cgitb.enable

tmpl_path="./common/myhome_tmpl.html"

ck = SimpleCookie()
ck.load(os.environ.get("HTTP_COOKIE",""))
form = cgi.FieldStorage()
ul = UserLogic.UserSelect()
#print("Content-type:text/html\n\n")

'''
ログインチェック
'''
trans = SumParts.Transporter()

if(not ("regid" in ck) or not("seskey" in ck)):
    trans.to_login_error()
else:
    sump = SumParts.SumParts()
    tmp_ses = ck["seskey"].value
    tmp_reg = ck["regid"].value
    res = sump.check_id_seskey(mregid=tmp_reg,mseskey=tmp_ses)
    if(not res):
        trans.to_login_error()
    else:
        uauth=UserLogin.UserInfo()
        uinfo = uauth.get_uinfo(mregid=tmp_reg,mseskey=tmp_ses)
        if(not uinfo):
            trans.to_login_error()
        '''
        ログイン成功、ユーザ情報をセットする
        '''
'''
pageがあるか?
'''
if("page" in form):
    tmp_page = form.getfirst("page","")
    if(sump.check_page(tmp_page)):
        page = int(tmp_page)
    else:
        page = 1


d = dict(title="Duo Questioner| Question",
        username=uinfo["uname"])

html_temp = tempita.HTMLTemplate(open(tmpl_path).read()) 

print("Content-type: text/html")
print(ck.output("regid"))
print(ck.output("seskey"))
print("\n\n")
print(html_temp.substitute(d))
