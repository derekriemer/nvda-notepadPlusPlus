import controlTypes

class KeyMapperList(object):
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

class KeyMapperTabber(object):
	"""
	Manages the tab order of various controls, to manipulate them correctly.
	ToDO: When #5960 incubates into a stable version, use that functionality.
	"""

	@property
	def dialogRoot(self):
		"""Property to get the root dialog so that we can get the correct child window from it. Just return the foreground object, since that works. """
		return api.getForegroundObject()

	@property
	def nextTab(self):
		if self.role == controlTypes.ROLE_BUTTON:
			#We are on the close button
			#tab Control should get focus here.
			return self.dialogRoot.firstChild.firstChild
		elif self.role==controlTypes.ROLE_TAB:
			#This is one of the tabs.
			#We want to move to the list, by way of the pane.
			return self.dialogRoot.getChild(4).firstChild

	@property
	def previousTab(self):
		if self.role == controlTypes.ROLE_LISTITEM:
			return self.dialogRoot.firstChild #Focuses the tabList to focus the selected tab.
		elif self.role == controlTypes.ROLE_TAB:
			return self.dialogRoot.getChild(3).firstChild


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

