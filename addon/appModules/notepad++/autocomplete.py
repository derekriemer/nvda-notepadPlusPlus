# coding: utf-8
#autocomplete.py
#A part of theNotepad++ addon for NVDA
#Copyright (C) 2016-2022 Tuukka Ojala, Derek Riemer
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import ctypes

import braille
import config
from logHandler import log
import displayModel
import textInfos
import speech

# Win32 listbox messages, used as a fallback below. Scintilla's autocomplete
# popup (ListBoxX) hosts a genuine native listbox control as a child window
# (the "ListBox" ancestor closest to the LISTITEM in the object tree). Even
# when that control is owner-drawn/custom-themed so nothing is exposed via
# MSAA, it still normally stores each item's real string internally, since
# it needs that string for incremental filtering as the user types.
# LB_GETTEXT/LB_GETCURSEL read that stored string directly. Windows marshals
# these specific messages across process boundaries automatically for
# standard listbox controls, so this works even though Notepad++ is a
# separate process.
LB_GETCURSEL = 0x0188
LB_GETTEXT = 0x0189
LB_GETTEXTLEN = 0x018A


def _getNativeListboxSelectedText(hwnd):
	"""Read the currently selected item's text directly from a native Win32
	listbox control via SendMessage, bypassing MSAA/UIA and screen rendering
	entirely. Returns None if anything about this fails or looks wrong,
	rather than raising, so callers can fall back to other approaches.
	"""
	user32 = ctypes.windll.user32
	idx = user32.SendMessageW(hwnd, LB_GETCURSEL, 0, 0)
	if idx < 0:
		return None
	length = user32.SendMessageW(hwnd, LB_GETTEXTLEN, idx, 0)
	if length <= 0:
		return None
	buf = ctypes.create_unicode_buffer(length + 1)
	user32.SendMessageW(hwnd, LB_GETTEXT, idx, buf)
	return buf.value or None


# On current Notepad++/Scintilla builds, the autocomplete popup (ListBoxX)
# does not expose its item text through MSAA (name/value/description are
# all empty), and its content is not visible to NVDA's display-model screen
# scraping either (it appears to be rendered with a themed/DirectWrite path
# that classic GDI-hook-based scraping can't see). Both were confirmed empty
# via targeted diagnostic logging against a real Notepad++ 8.9.7 session.
#
# The reliable fix is to bypass the popup UI entirely and ask Scintilla
# itself for its own internal autocomplete state, via
# EditWindow.getAutocompleteCurrentText() (see editWindow.py), which uses
# the documented SCI_AUTOCGETCURRENTTEXT message. The native-listbox and
# display-model reads below are kept as fallbacks for older or differently
# themed builds where the Scintilla query might not be available or might
# fail for some other reason.
#
# This class used to subclass NVDAObjects.IAccessible.IAccessible directly.
# That's unnecessary (NVDA's overlay-class mechanism combines this mixin
# with whichever underlying API class - IAccessible or UIA - the real
# object actually uses) and ties the class to one specific accessibility
# API for no benefit, so it's now a plain mixin.
class AutocompleteList:

	# Fallback text source if nothing else works: read whatever is actually
	# rendered on screen within this item's bounding rectangle.
	TextInfo = displayModel.DisplayModelTextInfo

	def _getScintillaAutocompleteText(self):
		try:
			editRef = getattr(self.appModule, "_edit", None)
			edit = editRef() if editRef else None
			if edit is None:
				return None
			return edit.getAutocompleteCurrentText()
		except Exception:
			log.exception(
				"notepad++ addon: could not reach edit window for Scintilla query"
			)
			return None

	def _getNativeListboxText(self):
		# Find the nearest ancestor that is the real "ListBox" child window
		# (not the outer "ListBoxX" popup frame).
		try:
			ancestor = self.parent
			for _ in range(3):
				if ancestor is None:
					return None
				if ancestor.windowClassName == u'ListBox':
					return _getNativeListboxSelectedText(ancestor.windowHandle)
				ancestor = ancestor.parent
		except Exception:
			log.exception(
				"notepad++ addon: native listbox text extraction failed"
			)
		return None

	def _getDisplayModelText(self):
		try:
			info = self.makeTextInfo(textInfos.POSITION_ALL)
			return (info.text or "").strip()
		except Exception:
			log.exception(
				"notepad++ addon: displayModel text extraction failed"
			)
			return ""

	def _getSuggestionText(self):
		"""Try each available way of reading the currently highlighted
		suggestion's text, in order of reliability, and return the first
		one that produces something. Returns None if none of them do.
		"""
		for getText in (
			self._getScintillaAutocompleteText,
			lambda: self.name or getattr(self, "value", None) or getattr(self, "description", None),
			self._getNativeListboxText,
			self._getDisplayModelText,
		):
			text = getText()
			if text:
				return text
		return None

	def event_selection(self):
		try:
			text = self._getSuggestionText()
			log.debug(
				u"notepad++ addon: autocomplete selection changed, text=%r" % text
			)
			speech.cancelSpeech()
			if text:
				speech.speakText(text)
			if config.conf["notepadPp"]["brailleAutocompleteSuggestions"] and text:
				braille.handler.message(u'⣏ %s ⣹' % text)
		except Exception:
			# Log instead of silently swallowing, so future failures here
			# are visible in the NVDA log rather than invisible.
			log.exception(
				"notepad++ addon: failed to announce autocomplete suggestion"
			)
