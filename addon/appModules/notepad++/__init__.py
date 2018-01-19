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
import weakref
import addonHandler
import addonGui
import controlTypes
import eventHandler
import speech
import nvwave
from NVDAObjects.window.scintilla  import Scintilla
from . import editWindow, incrementalFind, autocomplete

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

	def __init__(self, *args, **kwargs):
		super(AppModule, self).__init__(*args, **kwargs)
		confspec = {
			"maxLineLength" : "integer(min=0, default=80)",
			"lineLengthIndicator" : "boolean(default=False)",
			"brailleAutocompleteSuggestions" : "boolean(default=True)",
			"soundsAutocompleteSuggestions" : "boolean(default=True)",
		}
		config.conf.spec["notepadPp"] = confspec
		self.guiManager = addonGui.GuiManager()
		self.requestEvents()
		self.isAutocomplete=False

	def terminate(self):
		del self.guiManager #deletes the object by way of reference count 0 

	def requestEvents(self):
		#We need these for autocomplete
		eventHandler.requestEvents("show", self.processID, u'ListBoxX')

	def event_show(self, obj, nextHandler):
		if obj.role == controlTypes.ROLE_PANE:
			self.isAutocomplete=True
			core.callLater(100, self.waitforAndReportDestruction,obj)
			#get the edit field if the weak reference still has it.
			edit = self._edit()
			if not edit:
				return
			if config.conf["notepadPp"]["soundsAutocompleteSuggestions"]:
				eventHandler.executeEvent("suggestionsOpened", edit)
		nextHandler()


	def waitforAndReportDestruction(self, obj):
		if obj.parent: #None when no parent.
			core.callLater(100, self.waitforAndReportDestruction,obj)
			return
		#The object is dead.
		self.isAutocomplete=False
		#get the edit field if the weak reference still has it.
		edit = self._edit()
		if not edit:
			return
		if config.conf["notepadPp"]["soundsAutocompleteSuggestions"]:
			eventHandler.executeEvent("suggestionsClosed", edit)

