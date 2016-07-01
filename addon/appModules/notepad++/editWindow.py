import addonHandler
import config
from NVDAObjects.behaviors import EditableTextWithAutoSelectDetection
from queueHandler import registerGeneratorObject
import speech
import textInfos
import tones
import ui

addonHandler.initTranslation()

class EditWindow(EditableTextWithAutoSelectDetection):
	"""An edit widnow that implements all of the scripts on the edit field for Notepad++"""

	def event_loseFocus(self):
		#Hack: finding the edit field from the foreground window is unreliable, so cache it here.
		self.appModule.edit = self

	def event_gainFocus(self):
		super(EditWindow, self).event_gainFocus()
		#Hack: finding the edit field from the foreground window is unreliable. If we previously cached an object, this will clean it up.
		self.appModule.edit = None

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

	#Translators: when pressed, goes to    the matching brace in Notepad++
	script_gotoMatchingBrace.__doc__ = _("Goes to the brace that matches the one under the caret")
	script_gotoMatchingBrace.category = "Notepad++"

	def script_goToNextBookmark(self, gesture):
		self.speakActiveLineIfChanged(gesture)

	#Translators: Script to move to the next bookmark in Notepad++.
	script_goToNextBookmark.__doc__ = _("Goes to the next bookmark")
	script_goToNextBookmark.category = "Notepad++"

	def script_goToPreviousBookmark(self, gesture):
		self.speakActiveLineIfChanged(gesture)

	#Translators: Script to move to the next bookmark in Notepad++.
	script_goToPreviousBookmark.__doc__ = _("Goes to the previous bookmark")
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

	#Translators: Script to move the cursor to the first character on the current line that excedes the users maximum allowed line length.
	script_goToFirstOverflowingCharacter.__doc__ = _("Moves to the first character that is after the maximum line length")
	script_goToFirstOverflowingCharacter.category = "Notepad++"

	def script_reportLineInfo(self, gesture):
		ui.message(self.parent.next.next.firstChild.getChild(2).name) 

	#Translators: Script that announces information about the current line.
	script_reportLineInfo.__doc__ = _("speak the line info item on the status bar")
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
