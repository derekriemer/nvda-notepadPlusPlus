import wx
import gui

"""File for managing GUI for the appModule for notepad++"""

class GuiManager(object):

	def __init__(self):
		def _popupMenu(evt):
			#do popup work here, referencing the item if need be, like showing the dialog. Hint: Inherit  from gui.SettingsDialog
			pass
		self.prefsMenuItem  = item = gui.mainFrame.sysTrayIcon.preferencesMenu.Append(wx.ID_ANY, _("Notepad++..."))
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, _popupMenu, item)

	def enableItem(self):
		self.prefsMenuItem.Enable(True)

	def disableItem(self):
		self.prefsMenuItem.Enable(False)

	def __del__(self):
		try:
			gui.mainFrame.sysTrayIcon.preferencesMenu.RemoveItem(self.prefsMenuItem)
		except wx.PyDeadObjectError:
			pass
