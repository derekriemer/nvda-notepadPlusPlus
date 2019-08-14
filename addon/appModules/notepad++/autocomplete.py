# coding: utf-8
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
