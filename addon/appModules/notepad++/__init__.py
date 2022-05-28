#__init__.py
#A part of theNotepad++ addon for NVDA
#Copyright (C) 2016-2022 Tuukka Ojala, Derek Riemer
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import os
import time
import weakref
# NVDA core imports
import appModuleHandler
import core
import config
import gui
import addonHandler
import eventHandler
from controlTypes import Role
import speech
import nvwave
from NVDAObjects.window.scintilla  import Scintilla
# Do not try an absolute import. Because I have to name this module notepad++,
# and + isn't a valid character in a normal python module,
# You need to use from . import foo, for now.
# ToDo: Hack NVDA core,  adding syntax for addons to map an executable name
# to a python module under a different name.
from . import addonSettingsPanel, editWindow, incrementalFind, autocomplete

addonHandler.initTranslation()

class AppModule(appModuleHandler.AppModule):
	def chooseNVDAObjectOverlayClasses(self,obj,clsList):
		if obj.windowClassName == u'Scintilla' and obj.windowControlID == 0:
			clsList.insert(0, editWindow.EditWindow)
			return
		try: 
			if (obj.role == Role.LISTITEM and
				obj.parent.windowClassName == u'ListBox' and
				obj.parent.parent.parent.windowClassName == u'ListBoxX'):
				clsList.insert(0, autocomplete.AutocompleteList)
				return
		except AttributeError:
			pass
	
		if (
		(obj.windowControlID == 1682 and obj.role == Role.EDITABLETEXT)
		or
		(obj.role == Role.BUTTON and obj.windowControlID in (1683, 1684))
		):
			clsList.insert(0, incrementalFind.IncrementalFind)
			return
		if obj.windowControlID == 1689 and obj.role == Role.STATICTEXT:
			clsList.insert(0, incrementalFind.LiveTextControl)
			return

	def __init__(self, *args, **kwargs):
		super(AppModule, self).__init__(*args, **kwargs)
		confspec = {
			"maxLineLength" : "integer(min=0, default=80)",
			"lineLengthIndicator" : "boolean(default=False)",
			"brailleAutocompleteSuggestions" : "boolean(default=True)",
		}
		config.conf.spec["notepadPp"] = confspec
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(
			addonSettingsPanel.SettingsPanel)
		self.requestEvents()
		self.isAutocomplete=False

	def terminate(self):
		try:
			gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(
				addonSettingsPanel.SettingsPanel)
		except IndexError:
			pass

	def requestEvents(self):
		#We need these for autocomplete
		eventHandler.requestEvents("show", self.processID, u'ListBoxX')

	def event_show(self, obj, nextHandler):
		if obj.role == Role.PANE:
			self.isAutocomplete=True
			core.callLater(100, self.waitforAndReportDestruction,obj)
			#get the edit field if the weak reference still has it.
			edit = self._edit()
			if not edit:
				return
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
		eventHandler.executeEvent("suggestionsClosed", edit)

