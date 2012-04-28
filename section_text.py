#!/usr/local/bin/python
#-*- coding:utf-8 -*-

import sys
import os
import cgi
import cgitb
import urllib2
import tempita

import utils
import models

#Show error as a page description
sys.stderr = sys.stdout
#Enable debug output
cgitb.enable


'''
check login
'''
mnck = utils.ManageCookie()
ses,reg = mnck.check_ses_reg()
if(not ses):
    utils.to_login()
else:
    uauth=models.UserInfo()
    uinfo = uauth.get_uinfo(mregid=reg,mseskey=ses)
    if(not uinfo):
        utils.to_login()

'''
processing of the form
'''
form = cgi.FieldStorage()

secid = int(form.getvalue('secid','1'))
if ( secid < 1 or 45 < secid ):
    secid = 1
secid = str(secid)

'''
connect databese
'''
models.MYDB.connect()
us = models.UserSelect()
questions = us.section_question(secid)

'''
output
'''
title = "DuoQuestioner | " + "Section " + secid
menu = "text"
username = uinfo["regid"]
usid = uinfo["usid"]

temphtml = tempita.HTMLTemplate(open('common/section_text.html').read(),get_template=tempita.get_file_template)

mnck.destroy_allck()
mnck.set_ck(regid=reg,seskey=ses)
mnck.print_ck()
utils.to_stand_res()
print "\n\n"
print temphtml.substitute(locals())
