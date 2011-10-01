# coding:utf-8 vi:noet:ts=4

import sys
import os
import mimetypes

def d_mime_get_all_applications(mime_type):
	pass

def d_mime_get_default_application(mime_type):
	pass

def d_get_mime_type(path):
	if not mimetypes.inited:
		mimetypes.init()
	type = mimetypes.guess_type(path)[ 0 ]
	if type:
		return type
	if os.path.isdir( path ):
		return 'x-directory/normal'
	return 'text/plain'

def d_is_executable_command_string(path):
	pass

def d_mime_get_description(mime_type):
	pass

if sys.platform == 'linux2':
	# import linux modules
	try:
		from gnomevfs import *
	except:
		mime_get_all_applications    = d_mime_get_all_applications
		mime_get_default_application = d_mime_get_default_application
		get_mime_type                = d_get_mime_type
		is_executable_command_string = d_is_executable_command_string
		mime_get_description         = d_mime_get_description

	from os import statvfs

elif sys.platform == 'win32':
	# define methods for Windows

	mime_get_all_applications    = d_mime_get_all_applications
	mime_get_default_application = d_mime_get_default_application
	get_mime_type                = d_get_mime_type
	is_executable_command_string = d_is_executable_command_string
	mime_get_description         = d_mime_get_description

	def statvfs(path):
		class Stat(object):
			def __init__(self):
				self.f_bsize  = 0
				self.f_bavail = 0
				self.f_blocks = 0
		return Stat()

elif sys.platform == 'darwin':
	# define methods for OS/X

	mime_get_all_applications = d_mime_get_all_applications
	mime_get_default_application = d_mime_get_default_application
	get_mime_type = d_get_mime_type
	is_executable_command_string = d_is_executable_command_string
	mime_get_description = d_mime_get_description

	from os import statvfs

else:
	# unknown platform, stop executing
	raise Exception("Unknown platform.")

