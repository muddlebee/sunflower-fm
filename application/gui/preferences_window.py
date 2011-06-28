from gi.repository import GObject, Gtk
from gui.preferences.display import DisplayOptions
from gui.preferences.item_list import ItemListOptions
from gui.preferences.terminal import TerminalOptions
from gui.preferences.view_and_edit import ViewEditOptions
from gui.preferences.toolbar import ToolbarOptions
from gui.preferences.bookmarks import BookmarksOptions
from gui.preferences.tools import ToolsOptions
from gui.preferences.plugins import PluginsOptions
#from gui.preferences.accelerators import AcceleratorOptions

COL_NAME	= 0
COL_WIDGET	= 1


class PreferencesWindow(GObject.GObject):
	
	__gtype_name__ = 'Sunflower_PreferencesWindow'

	def __init__(self, parent):
		super(PreferencesWindow, self).__init__()

		self._parent = parent
		self._tab_names = {}

		# configure self
		self.window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
		self.window.set_title(_('Preferences'))
		self.window.set_size_request(640, 500)
		self.window.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
		self.window.set_modal(True)
		self.window.set_skip_taskbar_hint(True)
		self.window.set_transient_for(self._parent.window)
		self.window.set_wmclass('Sunflower', 'Sunflower')

		self.window.connect('delete_event', self._hide)

		# create GUI
		vbox = Gtk.VBox(homogeneous=False, spacing=7, border_width=7)
		hbox = Gtk.HBox(homogeneous=False, spacing=5)

		# create tab label container
		label_container = Gtk.ScrolledWindow()
		label_container.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
		label_container.set_shadow_type(Gtk.ShadowType.IN)
		label_container.set_size_request(130, -1)

		self._labels = Gtk.ListStore(str, int)
		self._tab_labels = Gtk.TreeView(model=self._labels)

		cell_label = Gtk.CellRendererText()
		col_label = Gtk.TreeViewColumn(None, cell_label, text=COL_NAME)

		self._tab_labels.append_column(col_label)
		self._tab_labels.set_headers_visible(False)
		self._tab_labels.connect('cursor-changed', self._handle_cursor_change)

		# create tabs
		self._tabs = Gtk.Notebook()
		self._tabs.set_show_tabs(False)
		self._tabs.set_show_border(False)
		self._tabs.connect('switch-page', self._handle_page_switch)

		DisplayOptions(self, parent)
		ItemListOptions(self, parent)
		TerminalOptions(self, parent)
		ViewEditOptions(self, parent)
		ToolbarOptions(self, parent)
		BookmarksOptions(self, parent)
		ToolsOptions(self, parent)
		PluginsOptions(self, parent)
		#AcceleratorOptions(self, parent)

		# select first tab
		path = self._labels.get_path(self._labels.get_iter_first())
		self._tab_labels.set_cursor(path, None, None)

		# create buttons
		hbox_controls = Gtk.HBox(homogeneous=False, spacing=5)

		btn_close = Gtk.Button(stock=Gtk.STOCK_CLOSE)
		btn_close.connect('clicked', self._hide)

		self._button_save = Gtk.Button(stock=Gtk.STOCK_SAVE)
		self._button_save.connect('clicked', self._save_options)

		btn_help = Gtk.Button(stock=Gtk.STOCK_HELP)
		btn_help.connect(
					'clicked',
					self._parent.goto_web,
					'code.google.com/p/sunflower-fm/wiki/WelcomePage?tm=6'
				)

		# restart label
		self._label_restart = Gtk.Label('<i>{0}</i>'.format(_('Program restart required!')))
		self._label_restart.set_alignment(0.5, 0.5)
		self._label_restart.set_use_markup(True)
		self._label_restart.set_property('no-show-all', True)

		# pack buttons
		label_container.add(self._tab_labels)

		hbox.pack_start(label_container, False, False, 0)
		hbox.pack_start(self._tabs, True, True, 0)

		hbox_controls.pack_start(btn_help, False, False, 0)
		hbox_controls.pack_start(self._label_restart, True, True, 0)
		hbox_controls.pack_end(btn_close, False, False, 0)
		hbox_controls.pack_end(self._button_save, False, False, 0)

		# pack UI
		vbox.pack_start(hbox, True, True, 0)
		vbox.pack_start(hbox_controls, False, False, 0)

		self.window.add(vbox)

	def _show(self, widget, tab_name=None):
		"""Show dialog and reload options"""
		self._load_options()
		self.window.show_all()

		if tab_name is not None and self._tab_names.has_key(tab_name):
			self._tabs.set_current_page(self._tab_names[tab_name])

	def _hide(self, widget, data=None):
		"""Hide dialog"""
		self.window.hide()
		return True  # avoid destroying components

	def _load_options(self):
		"""Change interface to present current state of configuration"""
		# call all tabs to load their options
		for i in range(self._tabs.get_n_pages()):
			page = self._tabs.get_nth_page(i)

			if hasattr(page, '_load_options'):
				page._load_options()

		# disable save button and hide label
		self._button_save.set_sensitive(False)
		self._label_restart.hide()

	def _save_options(self, widget, data=None):
		"""Save options"""
		# call all tabs to save their options
		for i in range(self._tabs.get_n_pages()):
			page = self._tabs.get_nth_page(i)

			if hasattr(page, '_save_options'):
				page._save_options()

		# disable save button
		self._button_save.set_sensitive(False)

		# call main window to propagate new settings
		self._parent.apply_settings()

		# write changes to configuration file
		self._parent.save_config()

	def _handle_cursor_change(self, widget, data=None):
		"""Change active tab when cursor is changed"""
		selection = self._tab_labels.get_selection()
		list_, iter_ = selection.get_selected()

		if iter_ is not None:
			new_tab = list_.get_value(iter_, COL_WIDGET)

			self._tabs.handler_block_by_func(self._handle_page_switch)
			self._tabs.set_current_page(new_tab)
			self._tabs.handler_unblock_by_func(self._handle_page_switch)

	def _handle_page_switch(self, widget, page, page_num, data=None):
		"""Handle changing page without user interaction"""
		self._tab_labels.handler_block_by_func(self._handle_cursor_change)
#		self._tab_labels.set_cursor((page_num,))
		self._tab_labels.handler_unblock_by_func(self._handle_cursor_change)

	def enable_save(self, widget=None, show_restart=None):
		"""Enable save button"""
		self._button_save.set_sensitive(True)

		# show label with message
		if show_restart is not None and show_restart:
			self._label_restart.show()

	def add_tab(self, name, label, tab):
		"""Add new tab to preferences window

		If you are using SettingsPage class there's no need to call this
		method manually, class constructor will do it automatically for you!

		"""
		tab_number = self._tabs.get_n_pages()

		self._tab_names[name] = tab_number
		self._labels.append((label, tab_number))
		self._tabs.append_page(tab, None)
