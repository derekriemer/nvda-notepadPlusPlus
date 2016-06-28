from logHandler import log
import appModuleHandler
import config
from NVDAObjects.window.scintilla  import Scintilla
from NVDAObjects.behaviors import EditableTextWithAutoSelectDetection
import textInfos
import speech
import ui
from queueHandler import registerGeneratorObject
import queueHandler
import controlTypes
import tones
import api
import core

class AppModule(appModuleHandler.AppModule):
	def chooseNVDAObjectOverlayClasses(self,obj,clsList):
		if obj.windowClassName == u'Scintilla' and obj.windowControlID == 0:
			clsList.insert(0,EditWindow)
			return
		if (
			(obj.windowControlID == 1682 and obj.role == controlTypes.ROLE_EDITABLETEXT)
			or
			(obj.role == controlTypes.ROLE_BUTTON and obj.windowControlID in (67220, 67219))
			):
			clsList.insert(0, IncrementalFind)
			return
		if obj.windowControlID == 1689 and obj.role == controlTypes.ROLE_STATICTEXT:
			clsList.insert(0, LiveTextControl)
			return
		try:
			if obj.windowClassName == u'BABYGRID'  and  obj.firstChild and obj.firstChild.windowClassName == u'ListBox':
				#History lesson: I was depending on the presence of a scroll bar, and for tabs whith very few items, it doesn't appear.
				clsList.insert(0, KeyMapperList)
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
				clsList.insert(0, KeyMapperTabber)
		except AttributeError:
			pass

	def __init__(self, *args, **kwargs):
		super(AppModule, self).__init__(*args, **kwargs)
		confspec = {
			"maxLineLength" : "integer(min=0, default=0)",
			"maxLineNotifications" : "boolean(default=False)",
		}
		config.conf.spec["notepadPp"] = confspec

class EditWindow(EditableTextWithAutoSelectDetection):
	"""An edit widnow that implements all of the scripts on the edit field for Notepad++"""

	def event_loseFocus(self):
		#Hack: finding the edit field from the foreground window is unreliable, so cache it here.
		self.appModule.edit = self

	def script_gotoMatchingBrace(self, gesture):
		gesture.send()
		info = self.makeTextInfo(textInfos.POSITION_CARET).copy()
		#Expand to line.
		info.expand(textInfos.UNIT_LINE)
		if info.text.strip() in ('{', '}'):
			#This line is only one brace. Not very helpful to read, lets read the previous and next line as well.
			#Move it's start back a line.
			info.move(textInfos.UNIT_LINE, -1, endPoint = "start")
			# Move it's end one line, forward.
			info.move(textInfos.UNIT_LINE, 1, endPoint = "end")
			#speak the info.
			registerGeneratorObject((speech.speakMessage(i) for i in info.text.split("\n")))
		else:
			speech.speakMessage(info.text)

	script_gotoMatchingBrace.__doc__ = "Goes to the brace that matches the one under the caret"
	script_gotoMatchingBrace.category = "Notepad++"

	def script_goToNextBookmark(self, gesture):
		self.speakActiveLineIfChanged(gesture)

	script_goToNextBookmark.__doc__ = "Goes to the next bookmark"
	script_goToNextBookmark.category = "Notepad++"

	def script_goToPreviousBookmark(self, gesture):
		self.speakActiveLineIfChanged(gesture)

	script_goToPreviousBookmark.__doc__ = "Goes to the previous bookmark"
	script_goToPreviousBookmark.category = "Notepad++"

	def speakActiveLineIfChanged(self, gesture):
		old = self.makeTextInfo(textInfos.POSITION_CARET)
		gesture.send()
		new = self.makeTextInfo(textInfos.POSITION_CARET)
		if new.bookmark.startOffset != old.bookmark.startOffset:
			new.expand(textInfos.UNIT_LINE)
			speech.speakMessage(new.text)

	def event_typedCharacter(self, ch):
		super(EditWindow, self).event_typedCharacter(ch)
		if not config.conf["notepadPp"]["maxLineNotifications"]:
			return
		textInfo = self.makeTextInfo(textInfos.POSITION_CARET)
		textInfo.expand(textInfos.UNIT_LINE)
		if textInfo.bookmark.endOffset - textInfo.bookmark.startOffset >= config.conf["notepadPp"]["maxLineLength"]:
			tones.beep(500, 50)

	def script_reportLineOverflow(self, gesture):
		self.script_caret_moveByLine(gesture)
		if not config.conf["notepadPp"]["maxLineNotifications"]:
			return
		info = self.makeTextInfo(textInfos.POSITION_CARET)
		info.expand(textInfos.UNIT_LINE)
		if len(info.text.strip('\r\n')) > config.conf["notepadPp"]["maxLineLength"]:
			tones.beep(500, 50)

	def script_reportCharacterOverflow(self, gesture):
		self.script_caret_moveByCharacter(gesture)
		if not config.conf["notepadPp"]["maxLineNotifications"]:
			return
		caretInfo = self.makeTextInfo(textInfos.POSITION_CARET)
		lineStartInfo = self.makeTextInfo(textInfos.POSITION_CARET).copy()
		caretInfo.expand(textInfos.UNIT_CHARACTER)
		lineStartInfo.expand(textInfos.UNIT_LINE)
		caretPosition = caretInfo.bookmark.startOffset -lineStartInfo.bookmark.startOffset
		if caretPosition > config.conf["notepadPp"]["maxLineLength"] -1 and caretInfo.text not in ['\r', '\n']:
			tones.beep(500, 50)

	def script_goToFirstOverflowingCharacter(self, gesture):
		info = self.makeTextInfo(textInfos.POSITION_CARET)
		info.expand(textInfos.UNIT_LINE)
		if len(info.text) > config.conf["notepadPp"]["maxLineLength"]:
			info.move(textInfos.UNIT_CHARACTER, config.conf["notepadPp"]["maxLineLength"], "start")
			info.updateCaret()
			info.collapse()
			info.expand(textInfos.UNIT_CHARACTER)
			speech.speakMessage(info.text)

	script_goToFirstOverflowingCharacter.__doc__ = "Moves to the first character that is after the maximum line length"
	script_goToFirstOverflowingCharacter.category = "Notepad++"

	def script_reportLineInfo(self, gesture):
		ui.message(self.parent.next.next.firstChild.getChild(2).name) 

	script_reportLineInfo.__doc__ = "speak the line info item on the status bar"
	script_reportLineInfo.category = "Notepad++"

	__gestures = {
		"kb:control+b" : "gotoMatchingBrace",
		"kb:f2": "goToNextBookmark",
		"kb:shift+f2": "goToPreviousBookmark",
		"kb:nvda+shift+\\": "reportLineInfo",
		"kb:leftArrow": "reportCharacterOverflow",
		"kb:rightArrow": "reportCharacterOverflow",
		"kb:upArrow": "reportLineOverflow",
		"kb:downArrow": "reportLineOverflow",
		"kb:nvda+g": "goToFirstOverflowingCharacter",
	}

class KeyMapperList:

	def event_gainFocus(self):
		obj = self.firstChild.firstChild
		try:
			obj.getChild(obj.IAccessibleObject.AccSelection-1).setFocus()
		except TypeError:
			#There is no selection, set focus to the first item.
			obj.firstChild.setFocus()
		except COMError:
			#We're screwed.
			obj.firstChild.setFocus()


class KeyMapperTabber(object):
	"""
	Manages the tab order of various controls, to manipulate them correctly.
	"""

	@property
	def dialogRoot(self):
		"""Property to get the root dialog so that we can get the correct child window from it. Just return the foreground object, since that works. """
		return api.getForegroundObject()

	@property
	def nextTab(self):
		if self.role == controlTypes.ROLE_BUTTON:
			#We are on the close button
			#tab Control should get focus here.
			return self.dialogRoot.firstChild.firstChild
		elif self.role==controlTypes.ROLE_TAB:
			#This is one of the tabs.
			#We want to move to the list, by way of the pane.
			return self.dialogRoot.getChild(4).firstChild

	@property
	def previousTab(self):
		if self.role == controlTypes.ROLE_LISTITEM:
			return self.dialogRoot.firstChild #Focuses the tabList to focus the selected tab.
		elif self.role == controlTypes.ROLE_TAB:
			return self.dialogRoot.getChild(3).firstChild


	def script_tab(self, gesture):
		try:
			self.nextTab.setFocus()
		except AttributeError:
			gesture.send()

	def script_shiftTab(self, gesture):
		try:
			self.previousTab.setFocus()
		except AttributeError:
			gesture.send()

	__gestures = {
		"kb:tab" : "tab",
		"kb:shift+tab" : "shiftTab",
	}

class IncrementalFind(object):

	cacheBookmark = 0

	def event_typedCharacter(self, ch):
		def later():
			edit = self.appModule.edit
			textInfo = edit.makeTextInfo(textInfos.POSITION_SELECTION)
			if textInfo.bookmark == self.cacheBookmark:
				return #Nada has changed.
			self.cacheBookmark = textInfo.bookmark
			textInfo.expand(textInfos.UNIT_LINE)
			queueHandler.queueFunction(queueHandler.eventQueue, speech.speakMessage, (textInfo.text))
		core.callLater(100, later)


class LiveTextControl(object):
	_cache = None

	def event_nameChange(self):
		if LiveTextControl._cache and self._cache == self.name:
			return #No changes to the text, spurious nameChange.
		queueHandler.queueFunction(queueHandler.eventQueue, speech.speakMessage, (self.name))
		LiveTextControl._cache = self.name
