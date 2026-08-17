# coding: utf-8
#autocomplete.py
#A part of theNotepad++ addon for NVDA
#Copyright (C) 2016-2022 Tuukka Ojala, Derek Riemer
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import braille
import config
from logHandler import log
import speech

# On current Notepad++/Scintilla builds, the autocomplete popup (ListBoxX)
# does not expose its item text through MSAA - name/value/description are
# all empty. Confirmed via targeted diagnostic logging against a real
# Notepad++ 8.9.7 session.
#
# The reliable fix is to bypass the popup UI entirely and ask Scintilla
# itself for its own internal autocomplete state, via
# EditWindow.getAutocompleteCurrentText() (see editWindow.py), which uses
# the documented SCI_AUTOCGETCURRENTTEXT message - present in Scintilla
# since well before any Notepad++ version anyone is likely running today.
# The plain MSAA read below is kept as a cheap fallback in case that ever
# isn't available; it costs nothing to check.
#
# This class used to subclass NVDAObjects.IAccessible.IAccessible directly.
# That's unnecessary (NVDA's overlay-class mechanism combines this mixin
# with whichever underlying API class - IAccessible or UIA - the real
# object actually uses) and ties the class to one specific accessibility
# API for no benefit, so it's now a plain mixin.
class AutocompleteList:

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

	def _getSuggestionText(self):
		"""Try each available way of reading the currently highlighted
		suggestion's text, in order of reliability, and return the first
		one that produces something. Returns None if none of them do.
		"""
		for getText in (
			self._getScintillaAutocompleteText,
			lambda: self.name or getattr(self, "value", None) or getattr(self, "description", None),
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
