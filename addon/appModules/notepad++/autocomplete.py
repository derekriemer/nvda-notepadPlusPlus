# coding: utf-8
#autocomplete.py
#A part of theNotepad++ addon for NVDA
#Copyright (C) 2016-2022 Tuukka Ojala, Derek Riemer
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from NVDAObjects.IAccessible  import IAccessible
import speech
import braille
import config

class AutocompleteList(IAccessible):

	def event_selection(self):
		speech.cancelSpeech()
		speech.speakText(self.name)
		if config.conf["notepadPp"]["brailleAutocompleteSuggestions"]:
			braille.handler.message(u'⣏ %s ⣹' % self.name)
