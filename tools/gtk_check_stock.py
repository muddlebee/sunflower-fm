#!/usr/bin/env python
# coding:utf-8 vi:noet:ts=4

import gtk, math

defined = [ s for s in dir( gtk ) if s.startswith( "STOCK_" ) ]
defined = [ eval( "gtk.{0}".format( s ) ) for s in defined ]
available = gtk.stock_list_ids()
defined_wrong = [ s for s in defined if s not in available ]
undefined = [ s for s in available if s not in defined ]

if not defined_wrong and not undefined :
	print( "Stock item definitions are correct." )
if defined_wrong :
	print( "Defined stock items that are not available:" )
	for s in defined_wrong :
		print( "  {0}".format( s ) )
if undefined :
	print( "Available stock items that are not defined:" )
	for s in undefined :
		print( "  {0}".format( s ) )

for s in available :
	o = gtk.Image()
	o.set_from_stock( s, gtk.ICON_SIZE_BUTTON )
	o = gtk.Button( stock = s )

def display_stock():
	wnd = gtk.Window()
	wnd.set_title( "stock icons" )
	edge = int( math.ceil( math.sqrt( len( available ) ) ) )
	table = gtk.Table( rows = edge, columns = edge )
	wnd.add( table )
	for i, s in enumerate( available ) :
		image = gtk.Image()
		image.set_from_stock( s, gtk.ICON_SIZE_BUTTON )
		button = gtk.Button()
		button.set_image( image )
		button.show()
		button.set_tooltip_text( s )
		row = i % edge
		col = i / edge
		table.attach( button, row, row + 1, col, col + 1 )
	table.show()
	wnd.show()

def display_named():
	l = [ 'go-jump', 'tab_new', 'computer', 'user-home', 'folder',
		'edit-find-replace', 'document-open-recent', 'terminal', 'reload',
		'gtk-missing-image' ]
	wnd = gtk.Window()
	wnd.set_title( "named icons" )
	edge = int( math.ceil( math.sqrt( len( l ) ) ) )
	table = gtk.Table( rows = edge, columns = edge )
	wnd.add( table )
	for i, s in enumerate( l ) :
		image = gtk.Image()
		image.set_from_icon_name( s, gtk.ICON_SIZE_BUTTON )
		button = gtk.Button()
		button.set_image( image )
		button.show()
		button.set_tooltip_text( s )
		row = i % edge
		col = i / edge
		table.attach( button, row, row + 1, col, col + 1 )
	table.show()
	wnd.show()

display_stock()
display_named()
gtk.main()

