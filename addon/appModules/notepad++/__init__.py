#__init__.py
#A part of theNotepad++ addon for NVDA
#Copyright (C) 2016-2019 Tuukka Ojala, Derek Riemer
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.


# NVDA core imports
import appModuleHandler
import core
import config
import gui
import addonHandler
import controlTypes
import eventHandler
import speech
from NVDAObjects.IAccessible import OutlineItem
from NVDAObjects.IAccessible.sysTreeView32 import TreeViewItem
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
			if (obj.role == controlTypes.ROLE_LISTITEM and
				obj.parent.windowClassName == u'ListBox' and
				obj.parent.parent.parent.windowClassName == u'ListBoxX'):
				clsList.insert(0, autocomplete.AutocompleteList)
				return
			if obj.role == controlTypes.ROLE_TREEVIEWITEM and obj.parent.parent.parent.name == 'Function List':
				clsList.insert(0, FunctionListView)
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
		if obj.role == controlTypes.ROLE_PANE:
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

class FunctionListView(TreeViewItem, OutlineItem):
	def script_goToCurrentFunction(self, gesture):
		gesture.send()
		# it seems that is not possible to jump to a element that contains children, E.G. a class. So we don't set the focus in this case.
		if not (controlTypes.STATE_EXPANDED in self.states or controlTypes.STATE_COLLAPSED in self.states):
			self.appModule.edit.setFocus()

	#Translators: When pressed, set the cursor to the current element and set te focus in the edit window from notepad++.
	script_goToCurrentFunction.__doc__ = _("Set the focus in the editable text field, presumably with the cursor in the current element of function list.")
	script_goToCurrentFunction.category = "Notepad++"

	def script_goToEditWindow(self, gesture):
		self.appModule.edit.setFocus()

	#Translators: When pressed,  set te focus in the edit window from notepad++.
	script_goToEditWindow.__doc__ = _("Set the focus in the editable text field")
	script_goToEditWindow.category = "Notepad++"


	__gestures = {
		"kb:enter" : "goToCurrentFunction",
		"kb:escape" : "goToEditWindow",
	}
