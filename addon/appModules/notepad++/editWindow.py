#editWindow.py
#A part of theNotepad++ addon for NVDA
#Copyright (C) 2016-2022 Tuukka Ojala, Derek Riemer
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import weakref
import ctypes
import locale
import addonHandler
import config
import watchdog
import winKernel
from logHandler import log
try:
	from nvdaBuiltin.appModules.notepadPlusPlus import NppEdit as EditWindowBaseCls
except ImportError:
	from NVDAObjects.behaviors import EditableTextWithAutoSelectDetection as EditWindowBaseCls
from NVDAObjects.behaviors import EditableTextWithSuggestions
from NVDAObjects.inputComposition import InputCompositionTextInfo
from queueHandler import registerGeneratorObject
import speech
import textInfos
import tones
import ui
import eventHandler
import scriptHandler
import sys
import os

addonHandler.initTranslation()

# Scintilla message constants (from Scintilla.iface / Scintilla.h; these are
# stable across Scintilla versions - Notepad++ 8.9.7 uses Scintilla 5.x).
SCI_AUTOCACTIVE = 2102
# "get int AutoCGetCurrentText=2610(, stringresult text)" - a "stringresult"
# message: call once with lParam=0 to get the required buffer length
# (excluding the NUL terminator), then again with a big-enough buffer to
# fill it. This asks Scintilla's own internal autocomplete state directly
# for the currently-highlighted suggestion's text, bypassing the popup UI
# entirely - no dependency on MSAA, on how the popup is rendered, or on
# native listbox selection state, all of which were confirmed empty for
# this control via diagnostic logging.
SCI_AUTOCGETCURRENTTEXT = 2610
SCI_GETCODEPAGE = 2137
SC_CP_UTF8 = 65001


def _hasActiveInputComposition(obj):
	"""Return True when NVDA has current IME composition text for this object."""
	if getattr(obj, "isReading", False):
		return bool(getattr(obj, "readingString", ""))
	return bool(getattr(obj, "compositionString", ""))


class EditWindow(EditWindowBaseCls, EditableTextWithSuggestions):
	"""An edit window that implements all of the scripts on the edit field for Notepad++"""

	def getAutocompleteCurrentText(self):
		"""Ask Scintilla directly for the text of the currently selected
		autocomplete suggestion, via SCI_AUTOCGETCURRENTTEXT. Returns None if
		autocomplete isn't active, or if anything about the cross-process
		read fails, rather than raising - callers should treat None as
		"couldn't determine the text" and fall back to other approaches.
		"""
		try:
			hwnd = self.windowHandle
			processHandle = self.processHandle
			active = watchdog.cancellableSendMessage(hwnd, SCI_AUTOCACTIVE, 0, 0)
			if not active:
				return None
			# First call: lParam=0 asks Scintilla for the required length
			# (not including the NUL terminator), without writing anything.
			length = watchdog.cancellableSendMessage(hwnd, SCI_AUTOCGETCURRENTTEXT, 0, 0)
			if length <= 0:
				return None
			bufLen = length + 1
			# Scintilla will write into this buffer via lParam, but since
			# Notepad++ runs in a different process, the pointer we pass
			# must be valid in *its* address space, not ours - so we
			# allocate memory in the remote process, pass that address as
			# lParam, then copy the written bytes back into our own buffer
			# via ReadProcessMemory. This is the same technique NVDA core
			# uses to read this editor's own document text.
			remoteBuf = winKernel.virtualAllocEx(
				processHandle, None, bufLen, winKernel.MEM_COMMIT, winKernel.PAGE_READWRITE
			)
			try:
				watchdog.cancellableSendMessage(hwnd, SCI_AUTOCGETCURRENTTEXT, 0, remoteBuf)
				localBuf = ctypes.create_string_buffer(bufLen)
				winKernel.readProcessMemory(processHandle, remoteBuf, localBuf, bufLen, None)
			finally:
				winKernel.virtualFreeEx(processHandle, remoteBuf, 0, winKernel.MEM_RELEASE)
			# Match NVDA core's own ScintillaTextInfo._get_encoding: don't
			# assume UTF-8, ask the document what codepage it's actually
			# using (autocomplete suggestions can contain non-ASCII
			# identifiers in non-Unicode files too).
			codepage = watchdog.cancellableSendMessage(hwnd, SCI_GETCODEPAGE, 0, 0)
			if codepage == SC_CP_UTF8:
				encoding = "utf-8"
			else:
				encoding = locale.getlocale()[1] or "utf-8"
			text = localBuf.value.decode(encoding, errors="replace")
			return text or None
		except Exception:
			log.exception(
				"notepad++ addon: SCI_AUTOCGETCURRENTTEXT read failed"
			)
			return None

	def event_loseFocus(self):
		#Hack: finding the edit field from the foreground window is unreliable, so cache it here.
		# The object tree is all sorts of fubar,
		# And actually can have cycles (so it's not a tree).
		#We can't use the weakref cache, because NVDA probably (?) kill this object off when it loses focus.
		#Also, derek is too lazy to verify this when it already works.
		self.appModule.edit = self

	def event_gainFocus(self):
		super(EditWindow, self).event_gainFocus()
		#Hack: finding the edit field from the foreground window is unreliable. If we previously cached an object, this will clean it up, allowing it to be garbage collected.
		self.appModule.edit = None
		self.appModule._edit = weakref.ref(self)

	def initOverlayClass(self):
		#Notepad++ names the edit window "N" for some stupid reason.
		# Nuke it.
		self.name = ""

	def _get_TextInfo(self):
		if _hasActiveInputComposition(self):
			return InputCompositionTextInfo
		return super(EditWindow, self).TextInfo

	def script_goToMatchingBrace(self, gesture):
		gesture.send()
		info = self.makeTextInfo(textInfos.POSITION_CARET).copy()
		#Expand to line.
		info.expand(textInfos.UNIT_LINE)
		if info.text.strip() in ('{', '}'):
			#This line is only one brace. Not very helpful to read, lets read the previous and next line as well.
			#Move its start back a line.
			info.move(textInfos.UNIT_LINE, -1, endPoint = "start")
			# Move its end one line forward.
			info.move(textInfos.UNIT_LINE, 1, endPoint = "end")
			#speak the info.
			registerGeneratorObject((speech.speakMessage(i) for i in info.text.split("\n")))
		else:
			speech.speakMessage(info.text)

	#Translators: when pressed, goes to the matching brace in Notepad++
	script_goToMatchingBrace.__doc__ = _("Goes to the brace that matches the one under the caret")
	script_goToMatchingBrace.category = "Notepad++"

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
		if not config.conf["notepadPp"]["lineLengthIndicator"]:
			return
		textInfo = self.makeTextInfo(textInfos.POSITION_CARET)
		textInfo.expand(textInfos.UNIT_LINE)
		if textInfo.bookmark.endOffset - textInfo.bookmark.startOffset >= config.conf["notepadPp"]["maxLineLength"]:
			tones.beep(500, 50)

	def script_reportLineOverflow(self, gesture):
		if self.appModule.isAutocomplete:
			gesture.send()
			return
		self.script_caret_moveByLine(gesture)
		if not config.conf["notepadPp"]["lineLengthIndicator"]:
			return
		info = self.makeTextInfo(textInfos.POSITION_CARET)
		info.expand(textInfos.UNIT_LINE)
		if len(info.text.strip('\r\n\t ')) > config.conf["notepadPp"]["maxLineLength"]:
			tones.beep(500, 50)

	def event_caret(self):
		super(EditWindow, self).event_caret()
		if not config.conf["notepadPp"]["lineLengthIndicator"]:
			return
		caretInfo = self.makeTextInfo(textInfos.POSITION_CARET)
		lineStartInfo = self.makeTextInfo(textInfos.POSITION_CARET).copy()
		caretInfo.expand(textInfos.UNIT_CHARACTER)
		lineStartInfo.expand(textInfos.UNIT_LINE)
		caretPosition = caretInfo.bookmark.startOffset -lineStartInfo.bookmark.startOffset
		#Is it not a blank line, and are we further in the line than the marker position?
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

	#Translators: Script to move the cursor to the first character on the current line that exceeds the users maximum allowed line length.
	script_goToFirstOverflowingCharacter.__doc__ = _("Moves to the first character that is after the maximum line length")
	script_goToFirstOverflowingCharacter.category = "Notepad++"

	def script_reportLineInfo(self, gesture):
		ui.message(self.parent.next.next.firstChild.getChild(2).name)

	#Translators: Script that announces information about the current line.
	script_reportLineInfo.__doc__ = _("Speak the line info item on the status bar")
	script_reportLineInfo.category = "Notepad++"

	def script_reportFindResult(self, gesture):
		old = self.makeTextInfo(textInfos.POSITION_SELECTION)
		gesture.send()
		new = self.makeTextInfo(textInfos.POSITION_SELECTION)
		if new.bookmark.startOffset != old.bookmark.startOffset:
			new.expand(textInfos.UNIT_LINE)
			speech.speakMessage(new.text)
		else:
			#Translators: Message shown when there are no more search results in this direction using the notepad++ find command.
			speech.speakMessage(_("No more search results in this direction"))

	#Translators: when pressed, goes to the Next search result in Notepad++
	script_reportFindResult.__doc__ = _("Queries the next or previous search result and speaks the selection and current line.")
	script_reportFindResult.category = "Notepad++"

	__gestures = {
		"kb:control+b" : "goToMatchingBrace",
		"kb:f2": "goToNextBookmark",
		"kb:shift+f2": "goToPreviousBookmark",
		"kb:nvda+shift+\\": "reportLineInfo",
		"kb:upArrow": "reportLineOverflow",
		"kb:downArrow": "reportLineOverflow",
		"kb:nvda+g": "goToFirstOverflowingCharacter",
		"kb:f3" : "reportFindResult",
		"kb:shift+f3" : "reportFindResult",
	}
