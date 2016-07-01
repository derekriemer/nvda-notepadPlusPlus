import queueHandler
from queueHandler import registerGeneratorObject
import speech
import textInfos

class IncrementalFind(object):
	cacheBookmark = 0

	def event_typedCharacter(self, ch):
		def later():
			edit = self.appModule.edit
			textInfo = edit.makeTextInfo(textInfos.POSITION_SELECTION)
			if textInfo.bookmark == self.cacheBookmark:
				return #Nada has changed.
			self.cacheBookmark = textInfo.bookmark
			textInfo.expand(textInfos.UNIT_LINE)
			queueHandler.queueFunction(queueHandler.eventQueue, speech.speakMessage, (textInfo.text))
		core.callLater(100, later)

class LiveTextControl(object):
	_cache = None

	def event_nameChange(self):
		if LiveTextControl._cache and self._cache == self.name:
			return #No changes to the text, spurious nameChange.
		queueHandler.queueFunction(queueHandler.eventQueue, speech.speakMessage, (self.name))
		LiveTextControl._cache = self.name
