#incrementalFind.py
#A part of theNotepad++ addon for NVDA
#Copyright (C) 2016 Tuukka Ojala, Derek Riemer
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import queueHandler
import speech
import config
import textInfos
import core
from NVDAObjects import NVDAObject
from scriptHandler import script
from logHandler import log


class IncrementalFind(NVDAObject):
	debug = False
	cacheBookmark = None
	die = False
	debug=False

	def schedule(self):
		log.debug("may schedule a round.")
		if self.die:
			log.debug("Not rescheduling")
			self.die=False
			return
		log.debug("Scheduling change watcher in 5 ms")
		core.callLater(5, self.changeWatcher)
	
	def event_gainFocus(self):
		super(IncrementalFind, self).event_gainFocus()
		log.debug("Gain focus fired")
		self.schedule()

	def event_loseFocus(self):
		self.die = True
		log.debug("Scheduling distruction.")

	def changeWatcher(self):
		
		self.schedule()
		log.debug("Preparing change watcher.")
		edit = self.appModule.edit
		if None is edit:
			#The editor gained focus. We're gonna die anyway on the next round.
			return
		textInfo = edit.makeTextInfo(textInfos.POSITION_SELECTION)
		if textInfo.bookmark == IncrementalFind.cacheBookmark:
			#Nothing has changed. Just go away.
			log.debug("Nothing has changed since the last round.")
			return
		IncrementalFind.cacheBookmark = textInfo.bookmark
		textInfo.expand(textInfos.UNIT_LINE)
		#Reporting indentation here is not really necessary.
		idt = speech.splitTextIndentation(textInfo.text)[0]
		textInfo.move(textInfos.UNIT_CHARACTER, len(idt), "start")
		def present():
			queueHandler.queueFunction(queueHandler.eventQueue, speech.speakTextInfo, (textInfo))
		core.callLater(100, present) #Slightly delay presentation in case the status changes.

	def event_stateChange(self):
		#Squelch the "pressed" message as this gets quite annoying, I must say.
		pass

	#Debug script for testing why the thing isn't firing.
	@script(gesture = 'kb:nvda+d')
	def script_debug(self, gesture):
		speech.speakMessage("Prepare for log spam")
	

class LiveTextControl(NVDAObject):
	_cache = None

	def event_nameChange(self):
		if LiveTextControl._cache and self._cache == self.name:
			return #No changes to the text, spurious nameChange.
		queueHandler.queueFunction(queueHandler.eventQueue, speech.speakMessage, (self.name))
		LiveTextControl._cache = self.name
