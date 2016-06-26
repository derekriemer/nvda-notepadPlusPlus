from logHandler import log
import appModuleHandler
import config
from NVDAObjects.window.scintilla  import Scintilla
from NVDAObjects.behaviors import EditableTextWithAutoSelectDetection, EditableTextWithoutAutoSelectDetection
from editableText import EditableText
import textInfos
import speech
from queueHandler import registerGeneratorObject
import eventHandler
import controlTypes
import tones

class AppModule(appModuleHandler.AppModule):
	def chooseNVDAObjectOverlayClasses(self,obj,clsList):
		if obj.windowClassName == u'Scintilla':
			clsList.insert(0,EditWindow)
		elif obj.windowClassName == u'BABYGRID'  and  obj.firstChild and obj.firstChild.windowClassName == u'ListBox': 
			#History lesson: I was depending on the presence of a scroll bar, and for tabs whith very few items, it doesn't appear.
			clsList.insert(0, KeyMapperList)

	def __init__(self, *args, **kwargs):
		super(AppModule, self).__init__(*args, **kwargs)
		confspec = {
			"maxLineLength" : "integer(min=0, default=0)",
		}
		config.conf.spec["notepadPp"] = confspec


class EditWindow(EditableTextWithAutoSelectDetection):
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
		super(AppModule, self).event_typedCharacter(ch)
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


