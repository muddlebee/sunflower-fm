import os

from gi.repository import GObject, Gtk, Gdk

COL_NAME		= 0
COL_PATH		= 1
COL_TIMESTAMP	= 2


class HistoryList(GObject.GObject):
	"""History list is used to display complete browsing history."""

	def __init__(self, parent, application):
		# create main window
		super(HistoryList, self).__init__()
		self.window = Gtk.Window(Gtk.WindowType.TOPLEVEL)

		# store parameters locally, we'll need them later
		self._parent = parent
		self._application = application

		# configure dialog
		self.window.set_title(_('History'))
		self.window.set_size_request(500, 300)
		self.window.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
		self.window.set_resizable(True)
		self.window.set_skip_taskbar_hint(True)
		self.window.set_modal(True)
		self.window.set_transient_for(self._application.window)
		self.window.set_wmclass('Sunflower', 'Sunflower')
		self.window.set_border_width(7)

		# create UI
		vbox = Gtk.VBox(False, 7)

		list_container = Gtk.ScrolledWindow()
		list_container.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
		list_container.set_shadow_type(Gtk.ShadowType.IN)

		self._history = Gtk.ListStore(str, str)

		cell_name = Gtk.CellRendererText()
		cell_path = Gtk.CellRendererText()

		col_name = Gtk.TreeViewColumn(_('Name'), cell_name, text=COL_NAME)
		col_path = Gtk.TreeViewColumn(_('Path'), cell_path, text=COL_PATH)

		self._history_list = Gtk.TreeView(self._history)
		self._history_list.connect('key-press-event', self._handle_key_press)
		self._history_list.append_column(col_name)
		self._history_list.append_column(col_path)

		# create controls
		hbox_controls = Gtk.HBox(False, 5)

		btn_close = Gtk.Button(stock=Gtk.STOCK_CLOSE)
		btn_close.connect('clicked', self._close)

		image_jump = Gtk.Image()
		image_jump.set_from_icon_name('go-jump', Gtk.IconSize.BUTTON)

		btn_jump = Gtk.Button()
		btn_jump.set_image(image_jump)
		btn_jump.set_label(_('Go to'))
		btn_jump.set_can_default(True)
		btn_jump.connect('clicked', self._change_path)

		image_new_tab = Gtk.Image()
		image_new_tab.set_from_icon_name('tab-new', Gtk.IconSize.BUTTON)

		btn_new_tab = Gtk.Button()
		btn_new_tab.set_image(image_new_tab)
		btn_new_tab.set_label(_('New tab'))
		btn_new_tab.set_tooltip_text(_('Open selected path in new tab'))
		btn_new_tab.connect('clicked', self._open_in_new_tab)

		# pack UI
		list_container.add(self._history_list)

		hbox_controls.pack_end(btn_close, False, False, 0)
		hbox_controls.pack_end(btn_jump, False, False, 0)
		hbox_controls.pack_start(btn_new_tab, False, False, 0)

		vbox.pack_start(list_container, True, True, 0)
		vbox.pack_start(hbox_controls, False, False, 0)

		self.window.add(vbox)

		# populate history list
		self._populate_list()

		# show all elements
		self.window.show_all()

	def _close(self, widget=None, data=None):
		"""Handle clicking on close button"""
		self.window.destroy()

	def _change_path(self, widget=None, data=None):
		"""Change to selected path"""
		selection = self._history_list.get_selection()
		list_, iter_ = selection.get_selected()

		# if selection is valid, change to selected path
		if iter_ is not None:
			path = list_.get_value(iter_, COL_PATH)

			# change path
			self._parent._handle_history_click(path=path)

			# close dialog
			self._close()

	def _open_in_new_tab(self, widget=None, data=None):
		"""Open selected item in new tab"""
		selection = self._history_list.get_selection()
		list_, iter_ = selection.get_selected()

		# if selection is valid, change to selected path
		if iter_ is not None:
			path = list_.get_value(iter_, COL_PATH)

			# create new tab
			self._application.create_tab(
							self._parent._notebook,
							self._parent.__class__,
							path
						)

			# close dialog
			self._close()

	def _handle_key_press(self, widget, event, data=None):
		"""Handle pressing keys in history list"""
		result = False
		key_name = Gdk.keyval_name(event.keyval)

		if key_name == 'Return':
			if event.state & Gdk.CONTROL_MASK:
				# open path in new tab
				self._open_in_new_tab()

			else:
				# open path in existing tab
				self._change_path()

			result = True

		elif key_name == 'Escape':
			# close window on escape
			self._close()
			result = True

		return result

	def _populate_list(self):
		"""Populate history list"""
		for path in self._parent.history[1:]:
			name = os.path.basename(path)
			if name == '':
				name = path

			self._history.append((name, path))

		# select first item
		self._history_list.set_cursor((0,))
