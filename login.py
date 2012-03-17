#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import os
import cgi
import cgitb
import urllib2
from Cookie import SimpleCookie
import tempita
from Model import SumParts

sys.stderr = sys.stdout
cgitb.enable

trans = SumParts.Transporter()
d = trans.assemble_ck2dict()

temp_path = "common/login_html_template.html"

chk = {"ureg":2,"login_e":0,"long_time":0}

for i in chk:
    if(i in d and d[i]=="1"):
        chk[i] = 1
    elif(i in d and d[i] == "0"):
        chk[i] = 0
trans.destroy_allck()
html_temp = tempita.HTMLTemplate(open(temp_path).read())

print("Content-type:text/html\n\n")
print(html_temp.substitute(chk))
#print(d)
