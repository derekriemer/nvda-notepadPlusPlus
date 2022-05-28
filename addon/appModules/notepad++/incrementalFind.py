#incrementalFind.py
#A part of theNotepad++ addon for NVDA
#Copyright (C) 2016-2022 Tuukka Ojala, Derek Riemer
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
	cacheBookmark = None
	die = False

	def schedule(self):
		log.debug("Scheduling round.")
		if self.die:
			self.die=False
			return
		core.callLater(5, self.changeWatcher)
	
	def event_gainFocus(self):
		super(IncrementalFind, self).event_gainFocus()
		self.schedule()

	def event_loseFocus(self):
		self.die = True

	def changeWatcher(self):
		self.schedule()
		edit = self.appModule.edit
		if None is edit:
			#The editor gained focus. We're gonna die anyway on the next round.
			return
		textInfo = edit.makeTextInfo(textInfos.POSITION_SELECTION)
		if textInfo.bookmark == IncrementalFind.cacheBookmark:
			#Nothing has changed. Just go away.
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


class LiveTextControl(NVDAObject):
	_cache = None

	def event_nameChange(self):
		if LiveTextControl._cache and self._cache == self.name:
			return #No changes to the text, spurious nameChange.
		queueHandler.queueFunction(queueHandler.eventQueue, speech.speakMessage, (self.name))
		LiveTextControl._cache = self.name
