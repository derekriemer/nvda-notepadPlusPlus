# coding: utf-8
#autocomplete.py
#A part of theNotepad++ addon for NVDA
#Copyright (C) 2016-2022 Tuukka Ojala, Derek Riemer
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from NVDAObjects.IAccessible  import IAccessible
import speech
import braille
import config

import ctypes
from ctypes import wintypes


def isSuggestion(obj):
	# Inspect native window ancestry instead of the MSAA object tree.
	user32 = ctypes.windll.user32
	getParent = user32.GetParent
	getParent.argtypes = [wintypes.HWND]
	getParent.restype = wintypes.HWND
	hwnd = obj.windowHandle
	for _ in range(12):
		if not hwnd:
			break
		name = ctypes.create_unicode_buffer(256)
		user32.GetClassNameW(wintypes.HWND(hwnd), name, len(name))
		if name.value == "ListBoxX":
			return True
		hwnd = getParent(hwnd)
	return False


class AutocompleteList(IAccessible):
	def event_selection(self):
		self.appModule.reportCurrentSuggestion()

	def event_selectionAdd(self):
		self.event_selection()


# Scintilla exposes the current completion index and text directly.
# SCI_AUTOCGETCURRENTTEXT uses a pointer in the editor process, so use
# remote process memory rather than a local ctypes buffer.
def currentSuggestion(edit):
	from watchdog import cancellableSendMessage
	import ctypes
	hwnd = edit.windowHandle
	if not cancellableSendMessage(hwnd, 2102, 0, 0):  # SCI_AUTOCACTIVE
		return None
	index = cancellableSendMessage(hwnd, 2445, 0, 0)  # SCI_AUTOCGETCURRENT
	if index < 0 or index == 0xffffffff or index == 0xffffffffffffffff:
		return None
	length = cancellableSendMessage(hwnd, 2610, 0, 0)  # SCI_AUTOCGETCURRENTTEXT
	if not 0 < length < 65536:
		return None
	kernel = ctypes.WinDLL("kernel32", use_last_error=True)
	kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
	kernel.OpenProcess.restype = wintypes.HANDLE
	kernel.VirtualAllocEx.argtypes = [wintypes.HANDLE, ctypes.c_void_p, ctypes.c_size_t, wintypes.DWORD, wintypes.DWORD]
	kernel.VirtualAllocEx.restype = ctypes.c_void_p
	kernel.VirtualFreeEx.argtypes = [wintypes.HANDLE, ctypes.c_void_p, ctypes.c_size_t, wintypes.DWORD]
	kernel.ReadProcessMemory.argtypes = [wintypes.HANDLE, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]
	kernel.CloseHandle.argtypes = [wintypes.HANDLE]
	process = kernel.OpenProcess(0x0018 | 0x0020, False, edit.processID)
	if not process:
		return None
	address = None
	try:
		address = kernel.VirtualAllocEx(process, None, 65536, 0x3000, 4)
		if not address:
			return None
		count = cancellableSendMessage(hwnd, 2610, 0, address)
		if not 0 < count < 65536:
			return None
		buf = ctypes.create_string_buffer(count + 1)
		read = ctypes.c_size_t()
		if not kernel.ReadProcessMemory(process, address, buf, len(buf), ctypes.byref(read)):
			return None
		codepage = cancellableSendMessage(hwnd, 2137, 0, 0)
		encoding = "utf-8" if codepage == 65001 else ("cp%d" % codepage if codepage else "mbcs")
		return index, buf.value.decode(encoding, errors="replace")
	finally:
		if address:
			kernel.VirtualFreeEx(process, address, 0, 0x8000)
		kernel.CloseHandle(process)
