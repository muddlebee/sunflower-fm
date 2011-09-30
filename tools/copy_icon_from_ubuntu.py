#!/usr/bin/env python
# coding:utf-8 vi:noet:ts=4

# Script for developers. Will copy specified icon from Ubuntu.

import os
import sys

if len(sys.argv) != 6 :
	print("usage: {0} <theme> <type> <name> <ext> <size>".format(__file__))
	exit( 0 )

self = {}
dir = os.path.dirname(os.path.realpath(__file__))
self['root']  = os.path.abspath("{0}/../".format(dir))
self['theme'] = sys.argv[1]
self['type']  = sys.argv[2]
self['name']  = sys.argv[3]
self['ext']   = sys.argv[4]
self['size']  = sys.argv[5]

cmd  = "VBoxManage guestcontrol ubuntu copyfrom"
cmd += " /usr/share/icons/{theme}/{type}/{size}/{name}.{ext}".format(** self)
cmd += " {root}/images/{size}".format(** self)
cmd += " --username eye --password password"

os.system( cmd )

