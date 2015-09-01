#!/usr/bin/env python

#--- const
# author: zunc
# 2015/08

import netstat

APP = 'const'
VER = '0.1'

print '[+] %s %s' % (APP, VER)

netst = netstat.Netstat()
netst.refresh()

print '[+] DONE'