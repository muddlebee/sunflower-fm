# coding:utf-8 vi:noet:ts=4

import gtk

def button_icon(name):
	return from_icon_name(name, gtk.ICON_SIZE_BUTTON)

def dialog_icon(name):
	return from_icon_name(name, gtk.ICON_SIZE_DIALOG)

def menu_icon(name):
	return from_icon_name(name, gtk.ICON_SIZE_MENU)

def large_toolbar_icon(name):
	return from_icon_name(name, gtk.ICON_SIZE_LARGE_TOOLBAR)

def clone(src, dst):
	property = src.get_property('storage-type')
	if property == gtk.IMAGE_EMPTY:
		pass
	elif property == gtk.IMAGE_PIXMAP:
		dst.set_from_pixmap(*src.get_pixmap())
	elif property == gtk.IMAGE_IMAGE:
		dst.set_from_image(*src.get_image())
	elif property == gtk.IMAGE_PIXBUF:
		dst.set_from_pixbuf(src.get_pixbuf())
	elif property == gtk.IMAGE_STOCK:
		dst.set_from_stock(*src.get_stock())
	elif property == gtk.IMAGE_ICON_SET:
		dst.set_from_icon_set(*src.get_icon_set())
	elif property == gtk.IMAGE_ANIMATION:
		dst.set_from_icon_set(src.get_animation())
	elif property == gtk.IMAGE_ICON_NAME:
		dst.set_from_icon_name(*src.get_icon_name())
	else:
		raise Exception("Unknown image type.")

def from_icon_name(name, size):
	img = gtk.Image()
	theme = gtk.icon_theme_get_default()
	if theme.has_icon(name):
		img.set_from_icon_name(name, size)
	else:
		print("icon not found: {0}".format(name))
		img.set_from_stock(gtk.STOCK_MISSING_IMAGE, size)
	return img

