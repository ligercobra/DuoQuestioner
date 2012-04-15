#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import cgi
import cgitb
import urllib2
import sys
import datetime
import tempita
from dateutil.relativedelta import *

import utils
import models

def q_text(sec):

    sec_order = {
            "1":range(1,11),"11":range(11,21),
            "21":range(21,31),"31":range(31,41),"41":range(41,46)
            }
    if(sec in sec_order):
        tmp_sec = sec_order[sec]
    else:
        tmp_sec = sec_order["1"]
    return ("home_text_tmpl.html","text",tmp_sec)

def form_ref(mform):
    p_order = ["text",]
    res = {"q":"text","sec":range(1,10),"tmpl":"home_text_tmpl.html"}
    q_options = {
        "text":q_text,
        }
    
    if("q" in mform and form.getfirst("q","") in p_order):
        tmp_q = form.getfirst("q","")
        try:
            tmp_sec = form.getfirst("sec","")
        except:
            tmp_sec = "1"
        res["tmpl"],res["q"],res["sec"]=q_options.get(tmp_q,q_text)(tmp_sec)    
    return res

#Show error as a page description
sys.stderr = sys.stdout
#Enable debug output
cgitb.enable

form = cgi.FieldStorage()
ul = models.UserSelect()
mnck = utils.ManageCookie()

'''
check login
'''
ses,reg = mnck.check_ses_reg()
if(not ses):
    utils.to_login()
else:
    uauth=models.UserInfo()
    uinfo = uauth.get_uinfo(mregid=reg,mseskey=ses)
    if(not uinfo):
        utils.to_login()

#get section
pr = form_ref(form)

cd = dict(
        title="DuoQuestioner| home",
        menu="home",
        username=uinfo["regid"],
        section=pr["sec"],
        )
cont_tmpl = tempita.HTMLTemplate(open("common/"+pr["tmpl"]).read(),get_template=tempita.get_file_template)

#output
utils.to_stand_res()
mnck.destroy_allck()
mnck.set_ck(regid=reg,seskey=ses)
mnck.print_ck()
print("\n\n")
print(cont_tmpl.substitute(cd))

