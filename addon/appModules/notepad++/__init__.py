from logHandler import log
import appModuleHandler
import config
from NVDAObjects.window.scintilla  import Scintilla
import speech
import ui
import controlTypes
import addonHandler
import addonGui

from . import editWindow, incrementalFind, keyMapperDialog

addonHandler.initTranslation()

class AppModule(appModuleHandler.AppModule):
	def chooseNVDAObjectOverlayClasses(self,obj,clsList):
		if obj.windowClassName == u'Scintilla' and obj.windowControlID == 0:
			clsList.insert(0,editWindow.EditWindow)
			return
		if (
			(obj.windowControlID == 1682 and obj.role == controlTypes.ROLE_EDITABLETEXT)
			or
			(obj.role == controlTypes.ROLE_BUTTON and obj.windowControlID in (67220, 67219))
			):
			clsList.insert(0, incrementalFind.IncrementalFind)
			return
		if obj.windowControlID == 1689 and obj.role == controlTypes.ROLE_STATICTEXT:
			clsList.insert(0, incrementalFind.LiveTextControl)
			return
		try:
			if obj.windowClassName == u'BABYGRID'  and  obj.firstChild and obj.firstChild.windowClassName == u'ListBox':
				#History lesson: I was depending on the presence of a scroll bar, and for tabs whith very few items, it doesn't appear.
				clsList.insert(0, keyMapperDialog.KeyMapperList)
		except AttributeError:
			pass
		try:
			if (
			(obj.windowClassName == u'Button' and obj.windowControlID == 1 and obj.location[0] == 430)
			or
			(obj.role == controlTypes.ROLE_TAB and obj.parent.childCount == 5)
			or
			(obj.role == controlTypes.ROLE_LISTITEM and obj.parent.parent.parent.role == controlTypes.ROLE_PANE)
			):
				clsList.insert(0, keyMapperDialog.KeyMapperTabber)
		except AttributeError:
			pass

	def __init__(self, *args, **kwargs):
		super(AppModule, self).__init__(*args, **kwargs)
		confspec = {
			"maxLineLength" : "integer(min=0, default=0)",
			"maxLineNotifications" : "boolean(default=False)",
		}
		config.conf.spec["notepadPp"] = confspec
		self.guiManager = addonGui.GuiManager()

	def terminate(self):
		self.guiManager = None #deletes the object by way of reference count 0 
