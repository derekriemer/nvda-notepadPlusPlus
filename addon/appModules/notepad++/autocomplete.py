# coding: utf8
from NVDAObjects.IAccessible  import IAccessible
import nvwave
import speech
import braille, config
import os

class AutocompleteList(IAccessible):

	def event_selection(self):
		speech.cancelSpeech()
		speech.speakText(self.name)
		if config.conf["notepadPp"]["brailleAutocompleteSuggestions"]:
			braille.handler.message(u'⣏ %s ⣹' % self.name)
