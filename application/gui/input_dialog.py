import os
import time
import locale
import fnmatch
import user

from gi.repository import GObject, Gtk
from common import get_user_directory, USER_TEMPLATES_DIR

# constants
OPTION_RENAME		= 0
OPTION_NEW_NAME		= 1
OPTION_APPLY_TO_ALL	= 2


class InputDialog(GObject.GObject):
	"""Simple input dialog

	This class can be extended with additional custom controls
	by accessing locally stored objects. Initially this dialog
	contains single label and text entry, along with two buttons.

	"""
	
	__gtype_name__ = 'Sunflower_InputDialog'

	def __init__(self, application):
		super(InputDialog, self).__init__()

		self._application = application

		# create dialog
		self.dialog = Gtk.Dialog(self, parent=self._application.window)
		self.dialog.set_default_size(340, 10)
		self.dialog.set_resizable(True)
		self.dialog.set_skip_taskbar_hint(True)
		self.dialog.set_modal(True)
		self.dialog.set_transient_for(self._application.window)
		self.dialog.set_wmclass('Sunflower', 'Sunflower')

		self.dialog.vbox.set_spacing(0)

		self._container = Gtk.VBox(False, 0)
		self._container.set_border_width(5)

		# create interface
		vbox = Gtk.VBox(False, 0)
		self._label = Gtk.Label('Label')
		self._label.set_alignment(0, 0.5)

		self._entry = Gtk.Entry()
		self._entry.connect('activate', self._confirm_entry)

		button_ok = Gtk.Button(stock=Gtk.STOCK_OK)
		button_ok.connect('clicked', self._confirm_entry)
		button_ok.set_can_default(True)

		button_cancel = Gtk.Button(stock=Gtk.STOCK_CANCEL)

		# pack interface
		vbox.pack_start(self._label, False, False, 0)
		vbox.pack_start(self._entry, False, False, 0)

		self._container.pack_start(vbox, False, False, 0)

		self.dialog.add_action_widget(button_cancel, Gtk.ResponseType.CANCEL)
		self.dialog.action_area.pack_end(button_ok, False, False, 0)
		self.dialog.set_default_response(Gtk.ResponseType.OK)

		self.dialog.vbox.pack_start(self._container, True, True, 0)
		self.dialog.show_all()

	def _confirm_entry(self, widget, data=None):
		"""Enable user to confirm by pressing Enter"""
		if self._entry.get_text() != '':
			self.response(Gtk.ResponseType.OK)

	def set_label(self, label_text):
		"""Provide an easy way to set label text"""
		self._label.set_text(label_text)

	def set_text(self, entry_text):
		"""Set main entry text"""
		self._entry.set_text(entry_text)
		
	def set_title(self, title):
		"""Set dialog title"""
		self.dialog.set_title(title)

	def get_response(self):
		"""Return value and self-destruct

		This method returns tupple with response code and
		input text.

		"""
		code = self.run()
		result = self._entry.get_text()

		self.dialog.destroy()

		return (code, result)


class CreateDialog(InputDialog):
	"""Generic create file/directory dialog"""

	def __init__(self, application):
		super(CreateDialog, self).__init__(application)

		self._permission_updating = False
		self._mode = 0644
		self._dialog_size = None

		self._container.set_spacing(5)

		# create advanced options expander
		expander = Gtk.Expander(_('Advanced options'))
		expander.connect('activate', self._expander_event)
		expander.set_border_width(0)

		self._advanced = Gtk.VBox(False, 5)
		self._advanced.set_border_width(5)

		table = Gtk.Table(4, 4, False)

		# create widgets
		label = Gtk.Label(_('User:'))
		label.set_alignment(0, 0.5)
		table.attach(label, 0, 1, 0, 1)

		label = Gtk.Label(_('Group:'))
		label.set_alignment(0, 0.5)
		table.attach(label, 0, 1, 1, 2)

		label = Gtk.Label(_('Others:'))
		label.set_alignment(0, 0.5)
		table.attach(label, 0, 1, 2, 3)

		# owner checkboxes
		self._permission_owner_read = Gtk.CheckButton(_('Read'))
		self._permission_owner_read.connect('toggled', self._update_octal, (1 << 2) * 100)
		table.attach(self._permission_owner_read, 1, 2, 0, 1)

		self._permission_owner_write = Gtk.CheckButton(_('Write'))
		self._permission_owner_write.connect('toggled', self._update_octal, (1 << 1) * 100)
		table.attach(self._permission_owner_write, 2, 3, 0, 1)

		self._permission_owner_execute = Gtk.CheckButton(_('Execute'))
		self._permission_owner_execute.connect('toggled', self._update_octal, (1 << 0) * 100)
		table.attach(self._permission_owner_execute, 3, 4, 0, 1)

		# group checkboxes
		self._permission_group_read = Gtk.CheckButton(_('Read'))
		self._permission_group_read.connect('toggled', self._update_octal, (1 << 2) * 10)
		table.attach(self._permission_group_read, 1, 2, 1, 2)

		self._permission_group_write = Gtk.CheckButton(_('Write'))
		self._permission_group_write.connect('toggled', self._update_octal, (1 << 1) * 10)
		table.attach(self._permission_group_write, 2, 3, 1, 2)

		self._permission_group_execute = Gtk.CheckButton(_('Execute'))
		self._permission_group_execute.connect('toggled', self._update_octal, (1 << 0) * 10)
		table.attach(self._permission_group_execute, 3, 4, 1, 2)

		# others checkboxes
		self._permission_others_read = Gtk.CheckButton(_('Read'))
		self._permission_others_read.connect('toggled', self._update_octal, (1 << 2))
		table.attach(self._permission_others_read, 1, 2, 2, 3)

		self._permission_others_write = Gtk.CheckButton(_('Write'))
		self._permission_others_write.connect('toggled', self._update_octal, (1 << 1))
		table.attach(self._permission_others_write, 2, 3, 2, 3)

		self._permission_others_execute = Gtk.CheckButton(_('Execute'))
		self._permission_others_execute.connect('toggled', self._update_octal, (1 << 0))
		table.attach(self._permission_others_execute, 3, 4, 2, 3)

		# octal representation
		label = Gtk.Label(_('Octal:'))
		label.set_alignment(0, 0.5)
		table.attach(label, 0, 1, 3, 4)

		self._permission_octal_entry = Gtk.Entry(4)
		self._permission_octal_entry.set_width_chars(5)
		self._permission_octal_entry.connect('activate', self._entry_activate)
		table.attach(self._permission_octal_entry, 1, 2, 3, 4)
		table.set_row_spacing(2, 10)

		# pack interface
		self._advanced.pack_start(table, False, False, 0)
		expander.add(self._advanced)
		self._container.pack_start(expander, False, False, 0)

		self.update_mode()
		expander.show_all()

	def _entry_activate(self, widget, data=None):
		"""Handle octal mode change"""
		self._mode = int(widget.get_text(), 8)
		self.update_mode()

	def _update_octal(self, widget, data=None):
		"""Update octal entry box"""
		if self._permission_updating: return

		data = int(str(data), 8)
		self._mode += (-1, 1)[widget.get_active()] * data

		self.update_mode()

	def _update_checkboxes(self, widget=None, data=None):
		"""Update checkboxes accordingly"""
		self._permission_updating = True
		self._permission_owner_read.set_active(self._mode & 0b100000000)
		self._permission_owner_write.set_active(self._mode & 0b010000000)
		self._permission_owner_execute.set_active(self._mode & 0b001000000)
		self._permission_group_read.set_active(self._mode & 0b000100000)
		self._permission_group_write.set_active(self._mode & 0b000010000)
		self._permission_group_execute.set_active(self._mode & 0b000001000)
		self._permission_others_read.set_active(self._mode & 0b000000100)
		self._permission_others_write.set_active(self._mode & 0b000000010)
		self._permission_others_execute.set_active(self._mode & 0b000000001)
		self._permission_updating = False

	def _expander_event(self, widget, data=None):
		"""Return dialog size back to normal"""
		if widget.get_expanded():
			self.set_size_request(1, 1)
			self.resize(*self._dialog_size)

		else:
			self._dialog_size = self.get_size()
			self.set_size_request(-1, -1)

	def get_mode(self):
		"""Returns default directory/file creation mode"""
		return self._mode

	def set_mode(self, mode):
		"""Set directory/file creation mode"""
		self._mode = mode
		self.update_mode()

	def update_mode(self):
		"""Update widgets"""
		self._permission_octal_entry.set_text('{0}'.format(oct(self._mode)))
		self._update_checkboxes()


class FileCreateDialog(CreateDialog):

	def __init__(self, application):
		super(FileCreateDialog, self).__init__(application)

		self.set_title(_('Create empty file'))
		self.set_label(_('Enter new file name:'))

		# create option to open file in editor
		self._checkbox_edit_after = Gtk.CheckButton(_('Open file in editor'))

		# create template list
		vbox_templates = Gtk.VBox(False, 0)
		label_templates = Gtk.Label(_('Template:'))
		label_templates.set_alignment(0, 0.5)

		cell_icon = Gtk.CellRendererPixbuf()
		cell_name = Gtk.CellRendererText()

		self._templates = Gtk.ListStore(str, str, str)
		self._template_list = Gtk.ComboBox(self._templates)
		self._template_list.set_row_separator_func(self._row_is_separator)
		self._template_list.connect('changed', self._template_changed)
		self._template_list.pack_start(cell_icon, False)
		self._template_list.pack_start(cell_name, True)

		self._template_list.add_attribute(cell_icon, 'icon-name', 2)
		self._template_list.add_attribute(cell_name, 'text', 0)

		# pack interface
		vbox_templates.pack_start(label_templates, False, False, 0)
		vbox_templates.pack_start(self._template_list, False, False, 0)

		self._container.pack_start(self._checkbox_edit_after, False, False, 0)
		self._container.pack_start(vbox_templates, False, False, 0)

		self._container.reorder_child(self._checkbox_edit_after, 1)
		self._container.reorder_child(vbox_templates, 1)

		# populate template list
		self._populate_templates()

		# show all widgets
		self.show_all()

	def _populate_templates(self):
		"""Populate templates list"""
		self._templates.clear()

		# add items from templates directory
		directory = get_user_directory(USER_TEMPLATES_DIR)
		file_list = []

		if directory is not None:
			file_list = os.listdir(directory)
			file_list = filter(lambda file_: file_[0] != '.', file_list)  # skip hidden files

		# add empty file
		self._templates.append((_('Empty File'), '', 'document'))
		if len(file_list) > 0:
			self._templates.append(('', '', ''))  # separator

		for file_ in file_list:
			name = os.path.splitext(file_)[0]
			full_path = os.path.join(user.home, 'Templates', file_)
			icon_name = self._application.icon_manager.get_icon_for_file(full_path)

			self._templates.append((name, full_path, icon_name))

		# select default item
		self._template_list.set_active(0)

	def _row_is_separator(self, model, row, data=None):
		"""Determine if row being drawn is a separator"""
		return model.get_value(row, 0) == ''

	def _template_changed(self, widget, data=None):
		"""Handle changing template"""
		file_name = os.path.splitext(self._entry.get_text())
		active_item = self._template_list.get_active()

		# change extension only if specific template is selected
		if active_item > 0:
			extension = os.path.splitext(self._templates[active_item][1])[1]
			self._entry.set_text('{0}{1}'.format(file_name[0], extension))

	def get_edit_file(self):
		"""Get state of 'edit after creating' checkbox"""
		return self._checkbox_edit_after.get_active()

	def get_template_file(self):
		"""Return full path to template file

		In case when 'Empty File' is selected, return None

		"""
		result = None
		active_item = self._template_list.get_active()

		if active_item > 0:
			result = self._templates[active_item][1]

		return result


class DirectoryCreateDialog(CreateDialog):

	def __init__(self, application):
		super(DirectoryCreateDialog, self).__init__(application)

		self.set_title(_('Create directory'))
		self.set_label(_('Enter new directory name:'))
		self.set_mode(0755)


class CopyDialog(GObject.GObject):
	"""Dialog which will ask user for additional options before copying"""
	
	__gtype_name__ = 'Sunflower_CopyDialog'

	def __init__(self, application, provider, path):
		super(CopyDialog, self).__init__()

		self._application = application
		self._provider = provider

		# create dialog
		self.dialog = Gtk.Dialog(self, parent=self._application.window)
		self.dialog.set_default_size(340, 10)
		self.dialog.set_resizable(True)
		self.dialog.set_skip_taskbar_hint(True)
		self.dialog.set_modal(True)
		self.dialog.set_transient_for(application)

		self.dialog.vbox.set_spacing(0)

		# create additional UI
		vbox = Gtk.VBox(False, 0)
		vbox.set_border_width(5)

		self.label_destination = Gtk.Label()
		self.label_destination.set_alignment(0, 0.5)
		self.label_destination.set_use_markup(True)
		self._update_label()

		self.entry_destination = Gtk.Entry()
		self.entry_destination.set_text(path)
		self.entry_destination.set_editable(False)
		self.entry_destination.connect('activate', self._confirm_entry)

		# additional options
		advanced = Gtk.Frame('<span size="small">' + _('Advanced options') + '</span>')
		advanced.set_label_align(1, 0.5)
		label_advanced = advanced.get_label_widget()
		label_advanced.set_use_markup(True)

		vbox2 = Gtk.VBox(False, 0)
		vbox2.set_border_width(5)

		label_type = Gtk.Label(_('Only files of this type:'))
		label_type.set_alignment(0, 0.5)

		self.entry_type = Gtk.Entry()
		self.entry_type.set_text('*')
		self.entry_type.connect('activate', self._update_label)

		self.checkbox_owner = Gtk.CheckButton(_('Set owner on destination'))
		self.checkbox_mode = Gtk.CheckButton(_('Set access mode on destination'))
		self.checkbox_silent = Gtk.CheckButton(_('Silent mode'))

		self.checkbox_mode.set_active(True)

		self.checkbox_silent.set_tooltip_text(_(
										'Silent mode will enable operation to finish '
										'without disturbing you. If any errors occur, '
										'they will be presented to you after completion.'
									))

		self._create_buttons()

		# pack UI
		advanced.add(vbox2)

		vbox2.pack_start(label_type, False, False, 0)
		vbox2.pack_start(self.entry_type, False, False, 0)
		vbox2.pack_start(self.checkbox_owner, False, False, 0)
		vbox2.pack_start(self.checkbox_mode, False, False, 0)
		vbox2.pack_start(self.checkbox_silent, False, False, 0)

		vbox.pack_start(self.label_destination, False, False, 0)
		vbox.pack_start(self.entry_destination, False, False, 0)
		vbox.pack_start(advanced, False, False, 5)

		self.dialog.vbox.pack_start(vbox, True, True, 0)

		self.dialog.set_default_response(Gtk.ResponseType.OK)
		self.dialog.show_all()

	def _get_text_variables(self, count):
		"""Get text variables for update"""
		title = ngettext(
					'Copy item',
					'Copy items',
					count
				)
		label = ngettext(
					'Copy <b>{0}</b> item to:',
					'Copy <b>{0}</b> items to:',
					count
				)

		return title, label

	def _create_buttons(self):
		"""Create action buttons"""
		button_cancel = Gtk.Button(_('Cancel'))
		button_copy = Gtk.Button(_('Copy'))
		button_copy.set_flags(Gtk.DialogFlags.CAN_DEFAULT)

		self.dialog.add_action_widget(button_cancel, Gtk.ResponseType.CANCEL)
		self.dialog.add_action_widget(button_copy, Gtk.ResponseType.OK)

	def _confirm_entry(self, widget, data=None):
		"""Enable user to confirm by pressing Enter"""
		if self.entry_destination.get_text() != '':
			self.response(Gtk.ResponseType.OK)

	def _get_item_count(self):
		"""Count number of items to copy"""
		list_ = self._provider.get_selection()
		result = len(list_)

		if hasattr(self, 'entry_type'):
			matches = fnmatch.filter(list_, self.entry_type.get_text())
			result = len(matches)

		return result

	def _update_label(self, widget=None, data=None):
		"""Update label based on file type and selection"""
		# get item count
		item_count = self._get_item_count()

		# get label text
		title, label = self._get_text_variables(item_count)

		# apply text
		self.set_title(title)
		self.label_destination.set_markup(label.format(item_count))

	def get_response(self):
		"""Return value and self-destruct

		This method returns tupple with response code and
		dictionary with other selected options.

		"""
		code = self.dialog.run()
		options = (
				self.entry_type.get_text(),
				self.entry_destination.get_text(),
				self.checkbox_owner.get_active(),
				self.checkbox_mode.get_active()
			)

		self.dialog.destroy()

		return (code, options)


class MoveDialog(CopyDialog):
	"""Dialog which will ask user for additional options before moving"""

	def _get_text_variables(self, count):
		"""Get text variables for update"""
		title = ngettext(
					'Move item',
					'Move items',
					count
				)
		label = ngettext(
					'Move <b>{0}</b> item to:',
					'Move <b>{0}</b> items to:',
					count
				)

		return title, label

	def _create_buttons(self):
		"""Create action buttons"""
		button_cancel = Gtk.Button(_('Cancel'))
		button_move = Gtk.Button(_('Move'))
		button_move.set_flags(Gtk.DialogFlags.CAN_DEFAULT)

		self.dialog.add_action_widget(button_cancel, Gtk.ResponseType.CANCEL)
		self.dialog.add_action_widget(button_move, Gtk.ResponseType.OK)


class RenameDialog(InputDialog):
	"""Dialog used for renaming file/directory"""

	def __init__(self, application, selection):
		super(RenameDialog, self).__init__(application)

		self.set_title(_('Rename file/directory'))
		self.set_label(_('Enter a new name for this item:'))
		self.set_text(selection)

		self._entry.select_region(0, len(os.path.splitext(selection)[0]))


class OverwriteDialog(GObject.GObject):
	"""Dialog used for confirmation of file/directory overwrite"""

	__gtype_name__ = 'Sunflower_OverwriteDialog'

	def __init__(self, application, parent):
		super(OverwriteDialog, self).__init__()

		self._application = application
		self._rename_value = ''
		self._time_format = application.options.get('main', 'time_format')

		# create dialog
		self.dialog = Gtk.Dialog(parent=self._application.window)
		self.dialog.set_default_size(400, 10)
		self.dialog.set_resizable(True)
		self.dialog.set_skip_taskbar_hint(False)
		self.dialog.set_modal(True)
		self.dialog.set_transient_for(parent)
		self.dialog.set_urgency_hint(True)

		self.dialog.vbox.set_spacing(0)

		hbox = Gtk.HBox(False, 10)
		hbox.set_border_width(10)

		vbox = Gtk.VBox(False, 10)
		vbox_icon = Gtk.VBox(False, 0)

		# create interface
		icon = Gtk.Image()
		icon.set_from_stock(Gtk.STOCK_DIALOG_WARNING, Gtk.IconSize.DIALOG)

		self._label_title = Gtk.Label()
		self._label_title.set_use_markup(True)
		self._label_title.set_alignment(0, 0.5)
		self._label_title.set_line_wrap(True)

		self._label_message = Gtk.Label()
		self._label_message.set_alignment(0, 0.5)
		self._label_message.set_line_wrap(True)

		# inner hbox for original file
		hbox_original = Gtk.HBox(False, 0)

		self._icon_original = Gtk.Image()
		self._label_original = Gtk.Label()
		self._label_original.set_use_markup(True)
		self._label_original.set_alignment(0, 0.5)

		# inner hbox for source file
		hbox_source = Gtk.HBox(False, 0)

		self._icon_source = Gtk.Image()
		self._label_source = Gtk.Label()
		self._label_source.set_use_markup(True)
		self._label_source.set_alignment(0, 0.5)

		# rename expander
		self._expander_rename = Gtk.Expander(label=_('Select a new name for the destination'))
		self._expander_rename.connect('activate', self._rename_toggled)
		hbox_rename = Gtk.HBox(False, 10)

		self._entry_rename = Gtk.Entry()
		button_reset = Gtk.Button(_('Reset'))
		button_reset.connect('clicked', self._reset_rename_field)

		# apply to all check box
		self._checkbox_apply_to_all = Gtk.CheckButton(_('Apply this action to all files'))
		self._checkbox_apply_to_all.connect('toggled', self._apply_to_all_toggled)

		# pack interface
		vbox_icon.pack_start(icon, False, False, 0)

		hbox_original.pack_start(self._icon_original, False, False, 10)
		hbox_original.pack_start(self._label_original, True, True, 0)

		hbox_source.pack_start(self._icon_source, False, False, 10)
		hbox_source.pack_start(self._label_source, True, True, 0)

		self._expander_rename.add(hbox_rename)

		hbox_rename.pack_start(self._entry_rename, False, False, 0)
		hbox_rename.pack_start(button_reset, False, False, 0)

		vbox.pack_start(self._label_title, False, False, 0)
		vbox.pack_start(self._label_message, False, False, 0)
		vbox.pack_start(hbox_original, False, False, 0)
		vbox.pack_start(hbox_source, False, False, 0)
		vbox.pack_start(self._expander_rename, False, False, 0)
		vbox.pack_start(self._checkbox_apply_to_all, False, False, 0)

		hbox.pack_start(vbox_icon, False, False, 0)
		hbox.pack_start(vbox, True, True, 0)

		self.dialog.vbox.pack_start(hbox, True, True, 0)

		self._create_buttons()
		self.dialog.show_all()

	def _create_buttons(self):
		"""Create basic buttons"""
		button_cancel = Gtk.Button(stock=Gtk.STOCK_CANCEL)
		button_skip = Gtk.Button(label=_('Skip'))

		self.dialog.add_action_widget(button_cancel, Gtk.ResponseType.CANCEL)
		self.dialog.add_action_widget(button_skip, Gtk.ResponseType.NO)

	def _apply_to_all_toggled(self, widget, data=None):
		"""Event called upon clicking on "apply to all" check box"""
		checked = widget.get_active()
		self._expander_rename.set_sensitive(not checked)

	def _rename_toggled(self, widget, data=None):
		"""Event called upon activating expander"""
		expanded = widget.get_expanded()
		self._checkbox_apply_to_all.set_sensitive(expanded)

	def _reset_rename_field(self, widget, data=None):
		"""Reset rename field to predefined value"""
		self._entry_rename.set_text(self._rename_value)

	def _get_data(self, provider, path, relative_to=None):
		"""Return information for specified path using provider"""
		stat = provider.get_stat(path, relative_to=relative_to)

		if provider.is_dir(path, relative_to=relative_to):
			size = len(provider.list_dir(path, relative_to=relative_to))
			icon = 'folder'

		else:
			size = stat.st_size
			icon = self._application.icon_manager.get_icon_for_file(
																os.path.join(
																			provider.get_path(),
																			path
																		))

		str_size = locale.format('%d', size, True)
		str_date = time.strftime(self._time_format, time.localtime(stat.st_mtime))

		return (str_size, str_date, icon)

	def set_title_element(self, element):
		"""Set title label with appropriate formatting"""
		pass

	def set_message_element(self, element):
		"""Set message element"""
		pass

	def set_original(self, provider, path, relative_to=None):
		"""Set original element data"""
		data = self._get_data(provider, path, relative_to)

		self._icon_original.set_from_icon_name(data[2], Gtk.IconSize.DIALOG)
		self._label_original.set_markup(
									'<b>{2}</b>\n'
									'<i>{3}</i>\t\t{0}\n'
									'<i>{4}</i>\t{1}'.format(
														data[0],
														data[1],
														_('Original'),
														_('Size:'),
														_('Modified:')
													)
								)

	def set_source(self, provider, path, relative_to=None):
		"""Set source element data"""
		data = self._get_data(provider, path, relative_to)

		self._icon_source.set_from_icon_name(data[2], Gtk.IconSize.DIALOG)
		self._label_source.set_markup(
									'<b>{2}</b>\n'
									'<i>{3}</i>\t\t{0}\n'
									'<i>{4}</i>\t{1}'.format(
														data[0],
														data[1],
														_('Replace with'),
														_('Size:'),
														_('Modified:')
													)
								)

	def set_rename_value(self, name):
		"""Set rename default rename value"""
		self._rename_value = name
		self._entry_rename.set_text(name)

	def get_response(self):
		"""Return value and self-destroy

		This method returns tuple with response code and
		dictionary with other selected options.

		"""
		code = self.dialog.run()
		options = (
				self._expander_rename.get_expanded(),
				self._entry_rename.get_text(),
				self._checkbox_apply_to_all.get_active()
				)

		self.dialog.destroy()

		return (code, options)


class OverwriteFileDialog(OverwriteDialog):

	def __init__(self, application, parent):
		super(OverwriteFileDialog, self).__init__(application, parent)

		self.dialog.set_title(_('File conflict'))

	def _create_buttons(self):
		"""Create dialog specific button"""
		button_replace = Gtk.Button(label=_('Replace'))
		button_replace.set_can_default(True)

		super(OverwriteFileDialog, self)._create_buttons()
		self.dialog.add_action_widget(button_replace, Gtk.ResponseType.YES)

		self.dialog.set_default_response(Gtk.ResponseType.YES)

	def set_title_element(self, element):
		"""Set title label with appropriate formatting"""
		message = _('Replace file "{0}"?').format(element.replace('&', '&amp;'))
		self._label_title.set_markup('<span size="large" weight="bold">{0}</span>'.format(message))

	def set_message_element(self, element):
		"""Set message element"""
		message = _(
				'Another file with the same name already exists in '
				'"{0}". Replacing it will overwrite its content.'
			)

		self._label_message.set_text(message.format(element))


class OverwriteDirectoryDialog(OverwriteDialog):

	def __init__(self, application, parent):
		super(OverwriteDirectoryDialog, self).__init__(application, parent)

		self._entry_rename.set_sensitive(False)
		self.dialog.set_title(_('Directory conflict'))

	def _create_buttons(self):
		"""Create dialog specific button"""
		button_merge = Gtk.Button(label=_('Merge'))
		button_merge.set_can_default(True)

		super(OverwriteDirectoryDialog, self)._create_buttons()
		self.dialog.add_action_widget(button_merge, Gtk.ResponseType.YES)

		self.dialog.set_default_response(Gtk.ResponseType.YES)

	def set_title_element(self, element):
		"""Set title label with appropriate formatting"""
		message = _('Merge directory "{0}"?').format(element)
		self._label_title.set_markup('<span size="large" weight="bold">{0}</span>'.format(message))

	def set_message_element(self, element):
		"""Set message element"""
		message = _(
				'Directory with the same name already exists in '
				'"{0}". Merging will ask for confirmation before '
				'replacing any files in the directory that conflict '
				'with the files being copied.'
			)

		self._label_message.set_text(message.format(element))


class AddBookmarkDialog(GObject.GObject):
	"""This dialog enables user to change data before adding new bookmark"""
	
	__gtype_name__ = 'Sunflower_AddBookmarkDialog'

	def __init__(self, application, path):
		super(AddBookmarkDialog, self).__init__()

		self._application = application

		# configure dialog
		self.dialog = Gtk.Dialog(parent=self._application.window)
		self.dialog.set_title(_('Add bookmark'))
		self.dialog.set_default_size(340, 10)
		self.dialog.set_resizable(True)
		self.dialog.set_skip_taskbar_hint(True)
		self.dialog.set_modal(True)
		self.dialog.set_transient_for(self._application.window)

		self.dialog.vbox.set_spacing(0)

		# create component container
		vbox = Gtk.VBox(False, 5)
		vbox.set_border_width(5)

		# bookmark name
		label_name = Gtk.Label(_('Name:'))
		label_name.set_alignment(0, 0.5)
		self._entry_name = Gtk.Entry()
		self._entry_name.connect('activate', self._confirm_entry)

		vbox_name = Gtk.VBox(False, 0)

		# bookmark path
		label_path = Gtk.Label(_('Location:'))
		label_path.set_alignment(0, 0.5)
		self._entry_path = Gtk.Entry()
		self._entry_path.set_text(path)
		self._entry_path.set_editable(False)

		vbox_path = Gtk.VBox(False, 0)

		# controls
		button_ok = Gtk.Button(stock=Gtk.STOCK_OK)
		button_ok.connect('clicked', self._confirm_entry)
		button_ok.set_can_default(True)

		button_cancel = Gtk.Button(stock=Gtk.STOCK_CANCEL)

		self.dialog.add_action_widget(button_cancel, Gtk.ResponseType.CANCEL)
		self.dialog.action_area.pack_end(button_ok, False, False, 0)
		self.dialog.set_default_response(Gtk.ResponseType.OK)

		# pack interface
		vbox_name.pack_start(label_name, False, False, 0)
		vbox_name.pack_start(self._entry_name, False, False, 0)

		vbox_path.pack_start(label_path, False, False, 0)
		vbox_path.pack_start(self._entry_path, False, False, 0)

		vbox.pack_start(vbox_name, False, False, 0)
		vbox.pack_start(vbox_path, False, False, 0)

		self.dialog.vbox.pack_start(vbox, False, False, 0)

		self.dialog.show_all()

	def _confirm_entry(self, widget, data=None):
		"""Enable user to confirm by pressing Enter"""
		if self._entry_name.get_text() != '':
			self.response(Gtk.ResponseType.OK)

	def get_response(self):
		"""Return value and self-destruct

		This method returns tupple with response code and
		input text.

		"""
		code = self.dialog.run()

		name = self._entry_name.get_text()
		path = self._entry_path.get_text()

		self.dialog.destroy()

		return (code, name, path)


class OperationError(GObject.GObject):
	"""Dialog used to ask user about error occurred during certain operation."""
	
	__gtype_name__ = 'Sunflower_OperationErrorDialog'

	def __init__(self, application):
		super(OperationError, self).__init__()

		self._application = application

		# create dialog
		self.dialog = Gtk.Dialog(parent=self._application.window)
		self.dialog.set_title(_('Operation error'))
		self.dialog.set_default_size(340, 10)
		self.dialog.set_resizable(True)
		self.dialog.set_skip_taskbar_hint(True)
		self.dialog.set_modal(True)
		self.dialog.set_transient_for(self._application.window)

		self.dialog.vbox.set_spacing(0)

		# create component container
		hbox = Gtk.HBox(False, 10)
		hbox.set_border_width(5)

		vbox = Gtk.VBox(False, 10)
		vbox_icon = Gtk.VBox(False, 0)

		# create interface
		icon = Gtk.Image()
		icon.set_from_stock(Gtk.STOCK_DIALOG_ERROR, Gtk.IconSize.DIALOG)

		self._label_message = Gtk.Label()
		self._label_message.set_alignment(0, 0)
		self._label_message.set_use_markup(True)
		self._label_message.set_line_wrap(True)
		self._label_message.set_size_request(340, -1)
		self._label_message.set_selectable(True)

		self._label_error = Gtk.Label()
		self._label_error.set_alignment(0,0)
		self._label_error.set_line_wrap(True)
		self._label_error.set_size_request(340, -1)
		self._label_error.set_selectable(True)

		# create controls
		button_cancel = Gtk.Button(label=_('Cancel'))
		button_skip = Gtk.Button(label=_('Skip'))
		button_retry = Gtk.Button(label=_('Retry'))

		self.dialog.add_action_widget(button_cancel, Gtk.ResponseType.CANCEL)
		self.dialog.add_action_widget(button_skip, Gtk.ResponseType.NO)
		self.dialog.add_action_widget(button_retry, Gtk.ResponseType.YES)

		button_skip.set_can_default(True)
		self.dialog.set_default_response(Gtk.ResponseType.NO)

		# pack interface
		vbox_icon.pack_start(icon, False, False, 0)

		vbox.pack_start(self._label_message, False, False, 0)
		vbox.pack_start(self._label_error, False, False, 0)

		hbox.pack_start(vbox_icon, False, False, 0)
		hbox.pack_start(vbox, True, True, 0)

		self.dialog.vbox.pack_start(hbox, False, False, 0)

		# show all components
		self.dialog.show_all()

	def set_message(self, message):
		"""Set dialog message"""
		self._label_message.set_markup(message)

	def set_error(self, error):
		"""Set error text"""
		self._label_error.set_markup(error)

	def get_response(self):
		"""Return dialog response and self-destruct"""
		code = self.dialog.run()
		self.dialog.destroy()

		return code


class CreateToolbarWidgetDialog(GObject.GObject):
	"""Create widget persistent dialog."""
	
	__gtype_name__ = 'Sunflower_CreateToolbarWidgetDialog'

	def __init__(self, application):
		super(CreateToolbarWidgetDialog, self).__init__()

		self._application = application

		# create dialog
		self.dialog = Gtk.Dialog(parent=self._application.window)
		self.dialog.set_title(_('Add toolbar widget'))
		self.dialog.set_default_size(340, 10)
		self.dialog.set_resizable(True)
		self.dialog.set_skip_taskbar_hint(True)
		self.dialog.set_modal(True)
		self.dialog.set_transient_for(self._application.window)

		self.dialog.vbox.set_spacing(0)

		# create component container
		vbox = Gtk.VBox(False, 5)
		vbox.set_border_width(5)

		# create interface
		vbox_name = Gtk.VBox(False, 0)

		label_name = Gtk.Label(_('Name:'))
		label_name.set_alignment(0, 0.5)

		self._entry_name = Gtk.Entry(max=30)

		vbox_type = Gtk.VBox(False, 0)

		label_type = Gtk.Label(_('Type:'))
		label_type.set_alignment(0, 0.5)

		cell_renderer_icon = Gtk.CellRendererPixbuf()
		cell_renderer_text = Gtk.CellRendererText()
		cell_renderer_text.set_property('xalign', 0)
		self._type_list = Gtk.ListStore(str, str, str)

		self._combobox_type = Gtk.ComboBox(self._type_list)
		self._combobox_type.pack_start(cell_renderer_icon, False)
		self._combobox_type.pack_start(cell_renderer_text, True)
		self._combobox_type.add_attribute(cell_renderer_icon, 'icon-name', 2)
		self._combobox_type.add_attribute(cell_renderer_text, 'text', 1)

		# create controls
		button_add = Gtk.Button(stock=Gtk.STOCK_ADD)
		button_add.set_can_default(True)
		button_cancel = Gtk.Button(stock=Gtk.STOCK_CANCEL)

		self.dialog.add_action_widget(button_cancel, Gtk.ResponseType.CANCEL)
		self.dialog.add_action_widget(button_add, Gtk.ResponseType.ACCEPT)

		self.dialog.set_default_response(Gtk.ResponseType.ACCEPT)

		# pack interface
		vbox_name.pack_start(label_name, False, False, 0)
		vbox_name.pack_start(self._entry_name, False, False, 0)

		vbox_type.pack_start(label_type, False, False, 0)
		vbox_type.pack_start(self._combobox_type, False, False)

		vbox.pack_start(vbox_name, False, False, 0)
		vbox.pack_start(vbox_type, False, False, 0)

		self.dialog.vbox.pack_start(vbox, False, False, 0)

		# show all widgets
		self.dialog.show_all()

	def update_type_list(self, widgets):
		"""Update type list store"""
		self._type_list.clear()

		for key in widgets.keys():
			# get data
			data = widgets[key]

			# extract data from tuple
			text = data[0]
			icon = data[1]

			# add new item to the list
			self._type_list.append((key, text, icon))

	def get_response(self):
		"""Return dialog response and self-destruct"""
		name = None
		widget_type = None

		# clear text entry before showing
		self._entry_name.set_text('')

		# show dialog
		code = self.dialog.run()

		if code is Gtk.ResponseType.ACCEPT and len(self._type_list) > 0:
			# get name and type
			name = self._entry_name.get_text()
			widget_type = self._type_list[self._combobox_type.get_active()][0]

		self.dialog.hide()

		return code, name, widget_type
