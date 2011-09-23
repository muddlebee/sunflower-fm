# coding:utf-8 vi:noet:ts=4

import sys

if 'win32' == sys.platform :

	def init( app_name ):
		pass

	def Notification( title, text, icon ):
		pass

elif 'darwin' == sys.platform :

	def init( app_name ):
		pass

	def Notification( title, text, icon ):
		pass

elif 'linux2' == sys.platform :
	from pynotify import *
else :
	raise Exception( "Unknown platform." )

