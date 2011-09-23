# coding:utf-8 vi:noet:ts=4

import sys

if 'win32' == sys.platform :

	def mime_get_all_applications( mime_type ):
		pass

	def mime_get_default_application( mime_type ):
		pass

	def get_mime_type( path ):
		pass

	def is_executable_command_string( path ):
		pass

	def mime_get_description( mime_type ):
		pass

	def statvfs( path ) :
		class Stat( object ) :
			def __init__( self ) :
				self.f_bsize  = 0
				self.f_bavail = 0
				self.f_blocks = 0
		return Stat()

elif 'darwin' == sys.platform :

	def mime_get_all_applications( mime_type ):
		pass

	def mime_get_default_application( mime_type ):
		pass

	def get_mime_type( path ):
		pass

	def is_executable_command_string( path ):
		pass

	def mime_get_description( mime_type ):
		pass

	from os import statvfs

elif 'linux2' == sys.platform :
	from gnomevfs import *
	from os import statvfs
else :
	raise Exception( "Unknown platform." )

