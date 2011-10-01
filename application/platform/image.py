# coding:utf-8 vi:noet:ts=4

import os
import gtk

cache = {}

def button_icon(name):
	return icon_for_name(name, gtk.ICON_SIZE_BUTTON)

def dialog_icon(name):
	return icon_for_name(name, gtk.ICON_SIZE_DIALOG)

def menu_icon(name):
	return icon_for_name(name, gtk.ICON_SIZE_MENU)

def large_toolbar_icon(name):
	return icon_for_name(name, gtk.ICON_SIZE_LARGE_TOOLBAR)

def button_pixbuf(name):
	return pixbuf_for_name(name, gtk.ICON_SIZE_BUTTON)

def dialog_pixbuf(name):
	return pixbuf_for_name(name, gtk.ICON_SIZE_DIALOG)

def menu_pixbuf(name):
	return pixbuf_for_name(name, gtk.ICON_SIZE_MENU)

def large_toolbar_pixbuf(name):
	return pixbuf_for_name(name, gtk.ICON_SIZE_LARGE_TOOLBAR)

def pixbuf_for_name(name, size):
	ABOUT_SIZES = {
		gtk.ICON_SIZE_MENU:          16,
		gtk.ICON_SIZE_SMALL_TOOLBAR: 18,
		gtk.ICON_SIZE_LARGE_TOOLBAR: 24,
		gtk.ICON_SIZE_BUTTON:        24,
		gtk.ICON_SIZE_DND:           32,
		gtk.ICON_SIZE_DIALOG:        48 }
	# Use cache to load images from files only once for each name+size.
	key = name + str(ABOUT_SIZES[size])
	if key not in cache :
		pixbuf = None
		for ext in ["png", "svg"] :
			fname = "{0}.{1}".format(name, ext)
			fpath = os.path.join("images", str(ABOUT_SIZES[size]), fname)
			try:
				pixbuf = gtk.gdk.pixbuf_new_from_file(fpath)
				break
			except:
				pass
		cache[key] = pixbuf
	# Return icon from cache, if any.
	pixbuf = cache[key]
	if not pixbuf:
		print("icon not found: {0} {1}".format(name, ABOUT_SIZES[size]))
	return pixbuf

def icon_for_name(name, size):
	img = gtk.Image()
	theme = gtk.icon_theme_get_default()
	# Try to use icons from "Icon Theme" if possible. It's *nix-specific.
	if theme.has_icon(name):
		img.set_from_icon_name(name, size)
	else:
		pixbuf = pixbuf_for_name(name, size)
		if pixbuf:
			img.set_from_pixbuf(pixbuf)
		else:
			img.set_from_stock(gtk.STOCK_MISSING_IMAGE, size)
	return img

