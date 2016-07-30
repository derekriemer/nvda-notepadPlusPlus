#addonGui.py
#A part of theNotepad++ addon for NVDA
#Copyright (C) 2016 Tuukka Ojala, Derek Riemer
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from threading import Thread
import time
import queueHandler
from queueHandler import registerGeneratorObject
import speech
import textInfos
import core

class IncrementalFind(object):
	cacheBookmark = 0

	def event_typedCharacter(self, ch):
		#We have to watch the editor until a change occurs, or until we decide it's unlikely a change will occur. 
		#We want to do this in a background thread to prevent NVDA from locking.
		def changeWatcher():
			edit = self.appModule.edit
			safety = .3
			while safety > 0:
				textInfo = edit.makeTextInfo(textInfos.POSITION_SELECTION)
				if textInfo.bookmark == self.cacheBookmark:
					time.sleep(.0625)
					safety -= .0625
					continue
				self.cacheBookmark = textInfo.bookmark
				textInfo.expand(textInfos.UNIT_LINE)
				def present():
					queueHandler.queueFunction(queueHandler.eventQueue, speech.speakMessage, (textInfo.text))
				core.callLater(present, 100) #Slightly delay presentation in case the status changes.
				return
		t = Thread(target=changeWatcher)
		t.start()

	def event_stateChange(self):
		#Squelch the "pressed" message as this gets quite annoying, I must say.
		pass
		
class LiveTextControl(object):
	_cache = None

	def event_nameChange(self):
		if LiveTextControl._cache and self._cache == self.name:
			return #No changes to the text, spurious nameChange.
		queueHandler.queueFunction(queueHandler.eventQueue, speech.speakMessage, (self.name))
		LiveTextControl._cache = self.name
