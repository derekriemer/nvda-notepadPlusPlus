from __future__ import annotations

import builtins
import importlib.util
import sys
import types
import unittest
from pathlib import Path


class _BaseScintilla:
	TextInfo = "baseTextInfo"


class _BuiltinNppEdit(_BaseScintilla):
	def _get_TextInfo(self):
		if self.appModule.is64BitProcess and self.appModule.productVersion.startswith("8.95"):
			return "npp83TextInfo"
		return super().TextInfo


def _installNvdaStubs() -> None:
	addonHandler = types.ModuleType("addonHandler")

	def initTranslation():
		builtins._ = lambda message: message

	addonHandler.initTranslation = initTranslation
	sys.modules["addonHandler"] = addonHandler

	config = types.ModuleType("config")
	config.conf = {"notepadPp": {}}
	sys.modules["config"] = config

	nvdaObjects = types.ModuleType("NVDAObjects")
	nvdaObjects.__path__ = []
	sys.modules["NVDAObjects"] = nvdaObjects

	behaviors = types.ModuleType("NVDAObjects.behaviors")
	behaviors.EditableTextWithAutoSelectDetection = _BaseScintilla
	behaviors.EditableTextWithSuggestions = type("EditableTextWithSuggestions", (), {})
	sys.modules["NVDAObjects.behaviors"] = behaviors

	inputComposition = types.ModuleType("NVDAObjects.inputComposition")
	inputComposition.InputCompositionTextInfo = "compositionTextInfo"
	sys.modules["NVDAObjects.inputComposition"] = inputComposition

	nvdaBuiltin = types.ModuleType("nvdaBuiltin")
	nvdaBuiltin.__path__ = []
	sys.modules["nvdaBuiltin"] = nvdaBuiltin

	builtinAppModules = types.ModuleType("nvdaBuiltin.appModules")
	builtinAppModules.__path__ = []
	sys.modules["nvdaBuiltin.appModules"] = builtinAppModules

	builtinNpp = types.ModuleType("nvdaBuiltin.appModules.notepadPlusPlus")
	builtinNpp.NppEdit = _BuiltinNppEdit
	sys.modules["nvdaBuiltin.appModules.notepadPlusPlus"] = builtinNpp

	queueHandler = types.ModuleType("queueHandler")
	queueHandler.registerGeneratorObject = lambda generator: None
	sys.modules["queueHandler"] = queueHandler

	speech = types.ModuleType("speech")
	speech.speakMessage = lambda message: None
	sys.modules["speech"] = speech

	textInfos = types.ModuleType("textInfos")
	textInfos.POSITION_CARET = object()
	textInfos.POSITION_SELECTION = object()
	textInfos.UNIT_CHARACTER = object()
	textInfos.UNIT_LINE = object()
	sys.modules["textInfos"] = textInfos

	tones = types.ModuleType("tones")
	tones.beep = lambda hz, length: None
	sys.modules["tones"] = tones

	ui = types.ModuleType("ui")
	ui.message = lambda message: None
	sys.modules["ui"] = ui

	sys.modules["eventHandler"] = types.ModuleType("eventHandler")
	sys.modules["scriptHandler"] = types.ModuleType("scriptHandler")


def _loadEditWindowModule():
	_installNvdaStubs()
	modulePath = Path(__file__).parents[1] / "addon" / "appModules" / "notepad++" / "editWindow.py"
	spec = importlib.util.spec_from_file_location("addon_editWindow", modulePath)
	assert spec and spec.loader
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	return module


class EditWindowInputCompositionTest(unittest.TestCase):
	def test_composition_text_info_is_prioritized_over_npp83_text_info(self):
		module = _loadEditWindowModule()
		obj = module.EditWindow()
		obj.appModule = types.SimpleNamespace(is64BitProcess=True, productVersion="8.95.0.0")
		obj.compositionString = "\u70cf\u9f9c"
		obj.isReading = False

		self.assertEqual(obj._get_TextInfo(), "compositionTextInfo")

	def test_reading_string_counts_as_active_input_composition(self):
		module = _loadEditWindowModule()
		obj = module.EditWindow()
		obj.appModule = types.SimpleNamespace(is64BitProcess=True, productVersion="8.95.0.0")
		obj.compositionString = ""
		obj.readingString = "\u70cf\u9f9c"
		obj.isReading = True

		self.assertEqual(obj._get_TextInfo(), "compositionTextInfo")

	def test_npp83_text_info_is_used_without_composition(self):
		module = _loadEditWindowModule()
		obj = module.EditWindow()
		obj.appModule = types.SimpleNamespace(is64BitProcess=True, productVersion="8.95.0.0")
		obj.compositionString = ""
		obj.isReading = False

		self.assertEqual(obj._get_TextInfo(), "npp83TextInfo")

	def test_base_scintilla_text_info_is_kept_for_older_notepad_plus_plus(self):
		module = _loadEditWindowModule()
		obj = module.EditWindow()
		obj.appModule = types.SimpleNamespace(is64BitProcess=True, productVersion="8.21.0.0")
		obj.compositionString = ""
		obj.isReading = False

		self.assertEqual(obj._get_TextInfo(), "baseTextInfo")


if __name__ == "__main__":
	unittest.main()
