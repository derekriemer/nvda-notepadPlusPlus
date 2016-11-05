#keyMapperDialog.py
#A part of theNotepad++ addon for NVDA
#Copyright (C) 2016 Tuukka Ojala, Derek Riemer
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import time
import controlTypes
import api
import winUser
import speech
from NVDAObjects import NVDAObject

class KeyMapperList(NVDAObject):
	def event_gainFocus(self):
		obj = self.firstChild.firstChild
		try:
			obj.getChild(obj.IAccessibleObject.AccSelection-1).setFocus()
		except TypeError:
			#There is no selection, set focus to the first item.
			obj.firstChild.setFocus()
		except COMError:
			#We're screwed.
			obj.firstChild.setFocus()

class KeyMapperTabItem(NVDAObject):
	def click(self):
		speech.cancelSpeech()
		left, top, width, height = self.location
		x = left+(width/2)
		y = top+(height/2)
		#click the middle of the screen after moving to this location.
		winUser.setCursorPos(x,y)
		winUser.mouse_event(winUser.MOUSEEVENTF_LEFTDOWN,0,0,None,None)
		winUser.mouse_event(winUser.MOUSEEVENTF_LEFTUP,0,0,None,None)
		speech.cancelSpeech()

	def event_gainFocus(self):
		self.click()
		time.sleep(.025)
		super(KeyMapperTabItem, self).event_gainFocus()
			


class KeyMapperTabber(NVDAObject):
	"""
	Manages the tab order of various controls, to manipulate them correctly.
	ToDO: When #5960 incubates into a stable version, use that functionality.
	"""

	def _get_dialogRoot(self):
		"""Property to get the root dialog so that we can get the correct child window from it. Just return the foreground object, since that works. """
		return api.getForegroundObject()

	def _get_nextTab(self):
		if self.role == controlTypes.ROLE_BUTTON and self.windowControlID == 1:
			#We are on the close button
			#tab Control should get focus here.
			return self.dialogRoot.firstChild.firstChild
		elif self.role==controlTypes.ROLE_TAB:
			#This is one of the tabs.
			#We want to move to the list, by way of the pane.
			return self.dialogRoot.getChild(4).firstChild

	def _get_previousTab(self):
		if self.role == controlTypes.ROLE_LISTITEM:
			return self.dialogRoot.firstChild #Focuses the tabList to focus the selected tab.
		elif self.role == controlTypes.ROLE_TAB:
			return self.dialogRoot.getChild(3).firstChild
		elif self.role == controlTypes.ROLE_BUTTON and self.windowControlID == 2602:
				return self.dialogRoot.getChild(4).firstChild


	def script_tab(self, gesture):
		try:
			self.nextTab.setFocus()
		except AttributeError:
			gesture.send()

	def script_shiftTab(self, gesture):
		try:
			self.previousTab.setFocus()
		except AttributeError:
			gesture.send()

	__gestures = {
		"kb:tab" : "tab",
		"kb:shift+tab" : "shiftTab",
	}

