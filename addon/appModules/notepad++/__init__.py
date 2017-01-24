#__init__.py
#A part of theNotepad++ addon for NVDA
#Copyright (C) 2016 Tuukka Ojala, Derek Riemer
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
import core
import time
import appModuleHandler
import config
import os
import addonHandler
import addonGui
import controlTypes
import eventHandler
import speech
import nvwave
from NVDAObjects.window.scintilla  import Scintilla
from . import editWindow, incrementalFind, keyMapperDialog, autocomplete

addonHandler.initTranslation()

class AppModule(appModuleHandler.AppModule):
	def chooseNVDAObjectOverlayClasses(self,obj,clsList):
		if obj.windowClassName == u'Scintilla' and obj.windowControlID == 0:
			clsList.insert(0, editWindow.EditWindow)
			return
		try: 
			if obj.role == controlTypes.ROLE_LISTITEM and obj.parent.windowClassName == u'ListBox' and obj.parent.parent.parent.windowClassName == u'ListBoxX':
				clsList.insert(0, autocomplete.AutocompleteList)
				return
		except AttributeError:
			pass
	
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
			(obj.windowClassName == u'Button' and obj.windowControlID in  (1, 2602)) #Close and modify button
			or
			(obj.role == controlTypes.ROLE_TAB and obj.parent.childCount == 5)
			or
			(obj.role == controlTypes.ROLE_LISTITEM and obj.parent.parent.parent.role == controlTypes.ROLE_PANE)
			):
				clsList.insert(0, keyMapperDialog.KeyMapperTabber)
			if 			(obj.role == controlTypes.ROLE_TAB and obj.parent.childCount == 5):
				clsList.insert(0, keyMapperDialog.KeyMapperTabItem)
		except AttributeError:
			pass

	def __init__(self, *args, **kwargs):
		super(AppModule, self).__init__(*args, **kwargs)
		confspec = {
			"maxLineLength" : "integer(min=0, default=80)",
			"lineLengthIndicator" : "boolean(default=False)",
		}
		config.conf.spec["notepadPp"] = confspec
		self.guiManager = addonGui.GuiManager()
		self.requestEvents()
		self.isAutocomplete=False
	def terminate(self):
		del self.guiManager #deletes the object by way of reference count 0 

	def requestEvents(self):
		eventHandler.requestEvents("show", self.processID, u'ListBoxX')

	def event_show(self, obj, nextHandler):
		if obj.role == controlTypes.ROLE_PANE:
			nvwave.playWaveFile(os.path.join(os.path.dirname(__file__), "waves", "autocompleteOpen.wav"))
			self.isAutocomplete=True
			core.callLater(100, self.waitforAndReportDestruction,obj)
		nextHandler()


	def waitforAndReportDestruction(self, obj):
		if obj.parent: #None when no parent.
			core.callLater(100, self.waitforAndReportDestruction,obj)
			return
		#The object is dead.
		self.isAutocomplete=False
		nvwave.playWaveFile(os.path.join(os.path.dirname(__file__), "waves", "autocompleteClose.wav"))

