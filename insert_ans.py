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
alert = "error"
comment = "とりあえずエラー！"

# POSTデータ判定
if ( os.environ['REQUEST_METHOD'] != "POST" ):
    comment = "METHOD不正"
else:
    form = cgi.FieldStorage()
    # key(usid)とkey(secid)のチェック
    if not (form.has_key("usid") and form.has_key("secid")):
        comment = "usid or secidパラメータ不正" 
    else:
        usid = form.getvalue("usid")
        secid = form.getvalue("secid")
        models.MYDB.connect()
        us = models.UserSelect()
        qids = us.get_qid(secid)

        qid_ans = []
        for qid in qids:
            #key = "ansRadio" + str(qid["qid"])
            key = "ansRadio" + str(qid["qid"])
            # key(qid)のチェック
            if not ( form.has_key(key) ):
                comment = "keyパラメータ不正"
                break
            # key(qid).valueのチェック
            ans = int(form.getvalue(key, "0"))
            if not ( ans == 0 or ans == 1 ):
                comment = "valueパラメータ不正"
                breaki
            qid_ans.append({'qid':qid["qid"], 'ans':ans})
        
        #print usid
        #sys.exit()
        #usid = int(form.getvalue("usid"))
        ui = models.UserInsert()
        ui.result(usid, secid, qid_ans)
        alert = "success"
        comment = "やったね！結果の保存完了！"

'''
output
'''
title = "DuoQuestioner | " + "Insert " + alert
menu = "text"
username = uinfo["regid"]

temphtml = tempita.HTMLTemplate(open('common/insert_ans.html').read(),get_template=tempita.get_file_template)

mnck.destroy_allck()
mnck.set_ck(regid=reg,seskey=ses)
mnck.print_ck()
utils.to_stand_res()
print "\n\n"
print temphtml.substitute(locals())
