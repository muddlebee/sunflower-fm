import gobject

from threading import Event


class MonitorError(Exception): pass


class MonitorSignals:
	CHANGED = 0  # file changed
	CHANGES_DONE = 1  # a hint that this was probably the last change in a set
	DELETED = 2  # file was deleted
	CREATED = 3  # file was created
	ATTRIBUTE_CHANGED = 4  # attribute was changed
	PRE_UNMOUNT = 5  # location will soon be unmounted
	UNMOUNTED = 6  # location was unmounted
	MOVED = 7  # file was moved


class Monitor(gobject.GObject):
	"""File system monitor base class

	Monitors are used to watch over a specific path on file system
	specific to provider that created the monitor. They are created and
	destroyed automatically on each path change and mainly used by file
	lists but could have other usages.

	"""

	__gtype_name__ = 'Sunflower_Monitor'	
	__gsignals__ = {
				'changed': (gobject.SIGNAL_RUN_LAST, None, (int, str, str)),
			}
	
	def __init__(self, provider, path):
		gobject.GObject.__init__(self)

		self._path = path
		self._provider = provider
		self._monitor = None
		self._paused = Event()

	def _emit_signal(self, signal, path, other_path):
		"""Notify connected objects that monitored path was changed.

		Use other_path in cases where it seems logical, like moving files.
		Otherwise None should be used instead
		
		"""
		if not self._paused.is_set():
			self.emit('changed', signal, path, other_path)

	def pause(self):
		"""Pause monitoring"""
		self._paused.set()

	def resume(self):
		"""Resume monitoring"""
		self._paused.clear()

	def cancel(self):
		"""Cancel monitoring"""
		pass
