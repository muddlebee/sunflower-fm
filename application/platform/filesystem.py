# coding:utf-8 vi:noet:ts=4

import sys

if sys.platform == 'linux2':
	# import linux modules
	from gnomevfs import *
	from os import statvfs

elif sys.platform == 'win32':
	# define methods for Windows

	def mime_get_all_applications(mime_type):
		pass

	def mime_get_default_application(mime_type):
		pass

	def get_mime_type(path):
		pass

	def is_executable_command_string(path):
		pass

	def mime_get_description(mime_type):
		pass

	def statvfs(path):
		class Stat(object):
			def __init__(self):
				self.f_bsize  = 0
				self.f_bavail = 0
				self.f_blocks = 0
		return Stat()

elif sys.platform == 'darwin':
	# define methods for OS/X

	def mime_get_all_applications(mime_type):
		pass

	def mime_get_default_application(mime_type):
		pass

	def get_mime_type(path):
		pass

	def is_executable_command_string(path):
		pass

	def mime_get_description(mime_type):
		pass

	from os import statvfs

else:
	# unknown platform, stop executing
	raise Exception("Unknown platform.")

