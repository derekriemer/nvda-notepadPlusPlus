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
		if obj.role == Role.LISTITEM and autocomplete.isSuggestion(obj):
			if isinstance(obj, autocomplete.IAccessible):
				clsList.insert(0, autocomplete.AutocompleteList)
				return

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
		self.isAutocomplete=False
		self._lastSuggestion = None
		self._suggestionErrorLogged = False
		self._edit = lambda: None
		self.edit = None
		self.requestEvents()

	def terminate(self):
		try:
			gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(
				addonSettingsPanel.SettingsPanel)
		except ValueError:
			pass

	def requestEvents(self):
		for event, window in (("show", "ListBoxX"), ("selection", "ListBox"), ("selection", "ListBoxX")):
			eventHandler.requestEvents(event, self.processID, window)

	def event_show(self, obj, nextHandler):
		try:
			if obj.windowClassName == "ListBoxX" and not self.isAutocomplete:
				self.isAutocomplete = True
				self._lastSuggestion = None
				core.callLater(100, self.waitforAndReportDestruction, obj)
				edit = self._edit()
				if edit:
					eventHandler.executeEvent("suggestionsOpened", edit)
		finally:
			nextHandler()

	def waitforAndReportDestruction(self, obj):
		import ctypes
		user32 = ctypes.windll.user32
		if user32.IsWindow(obj.windowHandle) and user32.IsWindowVisible(obj.windowHandle):
			self.reportCurrentSuggestion()
			core.callLater(100, self.waitforAndReportDestruction, obj)
			return
		self.isAutocomplete = False
		edit = self._edit()
		if edit:
			eventHandler.executeEvent("suggestionsClosed", edit)


	def reportCurrentSuggestion(self):
		if not self.isAutocomplete:
			return
		edit = self._edit() or self.edit
		if not edit:
			return
		try:
			current = autocomplete.currentSuggestion(edit)
			if not current or current == self._lastSuggestion:
				return
			self._lastSuggestion = current
			speech.cancelSpeech()
			speech.speakMessage(current[1])
			if config.conf["notepadPp"]["brailleAutocompleteSuggestions"]:
				import braille
				braille.handler.message("⣏ %s ⣹" % current[1])
		except Exception:
			if not self._suggestionErrorLogged:
				from logHandler import log
				log.exception("NotepadPlusPlus: failed to read Scintilla autocomplete")
				self._suggestionErrorLogged = True
