from NVDAObjects.IAccessible  import IAccessible
import nvwave
import speech
import os

class AutocompleteList(IAccessible):

	def event_selection(self):
		speech.speakText(self.name)
	
