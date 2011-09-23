# coding:utf-8 vi:noet:ts=4

import sys

if sys.platform == 'linux2':
	# import linux native support
	from pynotify import init, Notification

elif sys.platform == 'win32':
	# define methods for Windows

	def init(app_name):
		pass

	def Notification(title, text, icon):
		pass

elif sys.platform == 'darwin':
	# define methods for OS/X

	def init(app_name):
		pass

	def Notification(title, text, icon):
		pass

else:
	# unknown platform, stop executing
	raise Exception("Unknown platform.")

