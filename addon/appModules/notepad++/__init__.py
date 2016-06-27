from logHandler import log
import appModuleHandler
import config
from NVDAObjects.window.scintilla  import Scintilla
from NVDAObjects.behaviors import EditableTextWithAutoSelectDetection
import textInfos
import speech
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
		}
		config.conf.spec["notepadPp"] = confspec

class EditWindow(EditableTextWithAutoSelectDetection):

	def event_loseFocus(self):
		self.appModule.edit = self

	def script_gotoMatchingBrace(self, gesture):
		gesture.send()
		info = self.makeTextInfo(textInfos.POSITION_CARET).copy()
		#Expand to line.
		info.expand(textInfos.UNIT_LINE)
		if info.text.strip() in ('{', '}'): #This line has only one brace. Not very helpful to read, lets read the previous and next line as well.
			#Move it's start back a line.
			info.move(textInfos.UNIT_LINE, -1, endPoint = "start")
			# Move it's end one line, forward.
			info.move(textInfos.UNIT_LINE, 1, endPoint = "end")
			#speak the info.
			registerGeneratorObject((speech.speakMessage(i) for i in info.text.split("\n")))
		else:
			speech.speakMessage(info.text)

	def script_goToNextBookmark(self, gesture):
		#Goes to the next bookmark.
		self.speakActiveLineIfChanged(gesture)

	def script_goToPreviousBookmark(self, gesture):
		#Goes to the previous bookmark.
		self.speakActiveLineIfChanged(gesture)

	def speakActiveLineIfChanged(self, gesture):
		old = self.makeTextInfo(textInfos.POSITION_CARET)
		gesture.send()
		new = self.makeTextInfo(textInfos.POSITION_CARET)
		if new.bookmark.startOffset != old.bookmark.startOffset:
			new.expand(textInfos.UNIT_LINE)
			speech.speakMessage(new.text)

	def event_typedCharacter(self, ch):
		super(EditWindow, self).event_typedCharacter(ch)
		if config.conf["notepadPp"]["maxLineLength"] == 0:
			return
		textInfo = self.makeTextInfo(textInfos.POSITION_CARET)
		textInfo.expand(textInfos.UNIT_LINE)
		if textInfo.bookmark.endOffset - textInfo.bookmark.startOffset >= config.conf["notepadPp"]["maxLineLength"]:
			tones.beep(500, 50)

	__gestures = {
		"kb:control+b" : "gotoMatchingBrace",
		"kb:f2": "goToNextBookmark",
		"kb:shift+f2": "goToPreviousBookmark",
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
