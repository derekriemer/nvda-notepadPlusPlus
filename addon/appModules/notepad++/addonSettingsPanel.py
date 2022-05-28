#addonGui.py
#A part of theNotepad++ addon for NVDA
#Copyright (C) 2016-2022 Tuukka Ojala, Derek Riemer
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import wx
import addonHandler
import config
import gui

addonHandler.initTranslation()

class SettingsPanel(gui.SettingsPanel):
	# Translators: Title for the settings panel in NVDA's multi-category settings
	title = _("Notepad++")

	def makeSettings(self, settingsSizer):
		# Translators: A setting for enabling/disabling line length indicator.
		self.lineLengthIndicatorCheckBox = wx.CheckBox(self,
			wx.NewId(),
			label=_("Enable &line length indicator"))
		self.lineLengthIndicatorCheckBox.SetValue(
			config.conf["notepadPp"]["lineLengthIndicator"])
		settingsSizer.Add(self.lineLengthIndicatorCheckBox, border=10, flag=wx.BOTTOM)
		maxLineLengthSizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: Setting for maximum line length used by line length indicator
		maxLineLengthLabel = wx.StaticText(self, -1, label=_("&Maximum line length:"))
		self.maxLineLengthEdit = wx.TextCtrl(self, wx.NewId())
		self.maxLineLengthEdit.SetValue(str(config.conf["notepadPp"]["maxLineLength"]))
		maxLineLengthSizer.AddMany([maxLineLengthLabel, self.maxLineLengthEdit])
		settingsSizer.Add(maxLineLengthSizer, border=10, flag=wx.BOTTOM)
		# Translators: A setting for enabling/disabling autocomplete suggestions in braille.
		self.brailleAutocompleteSuggestionsCheckBox = wx.CheckBox(self,
			wx.NewId(),
			label=_("Show autocomplete &suggestions in braille"))
		self.brailleAutocompleteSuggestionsCheckBox.SetValue(
			config.conf["notepadPp"]["brailleAutocompleteSuggestions"])
		settingsSizer.Add(self.brailleAutocompleteSuggestionsCheckBox,
			border=10,
			flag=wx.BOTTOM)

	def onSave(self):
		config.conf["notepadPp"]["lineLengthIndicator"] =self.lineLengthIndicatorCheckBox.IsChecked()
		config.conf["notepadPp"]["brailleAutocompleteSuggestions"] = self.brailleAutocompleteSuggestionsCheckBox.IsChecked()
		config.conf["notepadPp"]["maxLineLength"] = int(self.maxLineLengthEdit.Value)
