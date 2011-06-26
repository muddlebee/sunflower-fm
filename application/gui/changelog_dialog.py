import os

from gi.repository import GObject, Gtk, Pango


class ChangeLogDialog(GObject.GObject):
	"""Window used to display application change log"""
	
	__gtype_name__ = 'Sunflower_ChangeLog'

	def __init__(self, parent, modifications, show_modifications=False):
		super(ChangeLogDialog, self).__init__()
		self.dialog = Gtk.Dialog()
		
		self._parent = parent

		self.dialog.set_title(_('Version Overview'))
		self.dialog.set_size_request(500, 400)
		self.dialog.set_resizable(False)
		self.dialog.set_modal(True)
		self.dialog.set_wmclass('Sunflower', 'Sunflower')

		self.vbox.set_border_width(0)

		# set window icon
		self._parent.icon_manager.set_window_icon(self.dialog)

		# create dummy menu to get color style
		main_menu = Gtk.MenuBar()

		# pack it and realize it
		self.vbox.pack_start(main_menu)
		main_menu.realize()

		# grab style and destroy the menu
		style = main_menu.get_style().copy()
		self.vbox.remove(main_menu)
		main_menu.destroy()

		# program logo
		image_file = os.path.abspath(os.path.join(
								'images',
								'sunflower_hi-def_64x64.png'
							))
		image = Gtk.Image()
		image.set_from_file(image_file)
		image.set_size_request(70, 70)

		# program label
		program_label = Gtk.Label(
							'<span size="x-large" weight="bold">'
							'{1}</span>\n{2} {0[major]}.{0[minor]}{0[stage]} '
							'<span size="small"><i>({0[build]})</i>'
							'</span>'.format(
										parent.version,
										_('Sunflower'),
										_('Version')
									)
							)
		program_label.set_use_markup(True)
		program_label.modify_fg(Gtk.StateType.NORMAL, style.fg[Gtk.StateType.NORMAL])
		program_label.set_alignment(0, 0.5)

		# notebook which contains change log and modifications tab
		notebook = Gtk.Notebook()
		notebook.set_border_width(5)

		# modifications
		if show_modifications:
			vbox = Gtk.VBox(False, 7)
			vbox.set_border_width(7)

			# label to give some more information
			label_info = Gtk.Label(_(
								'Selected modifications will be applied before starting program. '
								'Applying all modifications is strongly suggested. If you manually '
								'changed configuration files this is a good time to backup them.'
							))
			label_info.set_alignment(0, 0.5)
			label_info.set_justify(Gtk.Justification.LEFT)
			label_info.connect('size-allocate', self._adjust_label)
			label_info.set_line_wrap(True)

			# create viewport to hold all the options for modifications
			modifications_label = Gtk.Label(_('Modifications'))
			modifications_window = Gtk.ScrolledWindow()
			modifications_window.add_with_viewport(modifications)
			modifications_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

			vbox.pack_start(label_info, False, False, 0)
			vbox.pack_start(modifications_window, True, True, 0)

			notebook.append_page(vbox, modifications_label)

		# change log
		font = Pango.FontDescription('monospace 9')
		changelog = Gtk.TextView()
		changelog.set_editable(False)
		changelog.set_cursor_visible(False)
		changelog.set_wrap_mode(Gtk.WrapMode.WORD)
		changelog.modify_font(font)

		# load change log if it exists
		changelog_file = os.path.abspath('change.log')
		if os.path.isfile(changelog_file):
			data = open(changelog_file, 'r').read()
		else:
			# change log was not found
			data = _('Change log was not found!')

		changelog.get_buffer().set_text(data)

		# create tab and container
		changelog_label = Gtk.Label(_('Change log'))
		changelog_window = Gtk.ScrolledWindow()
		changelog_window.set_shadow_type(Gtk.ShadowType.IN)
		changelog_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)
		changelog_window.set_border_width(5)
		changelog_window.add(changelog)

		notebook.append_page(changelog_window, changelog_label)

		# top horizontal box containing image and program title
		hbox1 = Gtk.HBox(False, 0)
		frame = Gtk.EventBox()
		frame.modify_bg(Gtk.StateType.NORMAL, style.bg[Gtk.StateType.NORMAL])
		frame.add(hbox1)

		hbox1.set_border_width(5)

		hbox1.pack_start(image, False, False, 0)
		hbox1.pack_start(program_label, True, True, 5)

		# actions buttons
		button_close = Gtk.Button(stock=Gtk.STOCK_CLOSE)
		button_close.set_can_default(True)

		# pack interface
		self.dialog.vbox.pack_start(frame, False, False, 0)
		self.dialog.vbox.pack_start(notebook, True, True, 0)

		self.add_action_widget(button_close, Gtk.ResponseType.CLOSE)

		self.dialog.show_all()

	def get_response(self):
		"""Show dialog and return response"""
		code = self.run()

		self.destroy()

		return code

	def _adjust_label(self, widget, data=None):
		"""Adjust label size"""
		widget.set_size_request(data.width-1, -1)
