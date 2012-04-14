#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import os
import cgi
import cgitb
import tempita
import utils

sys.stderr = sys.stdout
cgitb.enable

mnck = utils.ManageCookie()
d = mnck.assemble_ck2dict()

temp_path = "common/login_tmpl.html"

chk = {"ureg":-1,"login_e":-1,"long_time":-1}

for i in chk:
    if((i in d) and d[i]=="1"):
        chk[i] = 1
    elif((i in d) and d[i] == "0"):
        chk[i] = 0
    elif((i in d) and d[i] == "-1"):
        chk[i] = -1
    elif((i in d) and d[i] == "2"):
        chk[i] = 2
html_temp = tempita.HTMLTemplate(open(temp_path).read())

utils.to_stand_res()
mnck.destroy_allck()
mnck.set_ck(ureg="-1",login_e="-1",long_time="-1")
mnck.print_ck()
print("\n\n")
print(html_temp.substitute(chk))
