from gi.repository import GObject, Gtk


class SettingsPage(GObject.GObject):
	"""Abstract class used to build pages in preferences window."""
	
	__gtype_name__ = 'Sunflower_Settings_page'
	
	def __init__(self, parent, application, name, title):
		super(SettingsPage, self).__init__()
		
		self.vbox = Gtk.VBox(homogeneous=False, spacing=0)

		self._parent = parent
		self._application = application
		self._page_name = name
		self._page_title = title

		# configure self
		self.vbox.set_spacing(5)
		self.vbox.set_border_width(0)
		
		# add page to preferences window
		self._parent.add_tab(self._page_name, self._page_title, self.vbox)
		
	def _load_options(self):
		"""Load options and update interface"""
		pass

	def _save_options(self):
		"""Method called when save button is clicked"""
		pass