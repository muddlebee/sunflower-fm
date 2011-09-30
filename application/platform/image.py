# coding:utf-8 vi:noet:ts=4

import os
import gtk

cache = {}

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
	# Try to use icons from "Icon Theme" if possible. It's *nix-specific.
	if theme.has_icon(name):
		img.set_from_icon_name(name, size)
	else:
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
		if pixbuf:
			img.set_from_pixbuf(pixbuf)
		else:
			print("icon not found: {0} {1}".format(name, ABOUT_SIZES[size]))
			img.set_from_stock(gtk.STOCK_MISSING_IMAGE, size)
	return img

