#import idc
import sys, os
from ctypes import wintypes, WinDLL
import imp

###################################################################################################

AttachConsole = WinDLL('kernel32.dll').AttachConsole
AttachConsole.argtypes = [wintypes.DWORD]
AttachConsole.restype = wintypes.BOOL

GetStdHandle = WinDLL('kernel32.dll').GetStdHandle
GetStdHandle.argtypes = [wintypes.DWORD]
GetStdHandle.restype = wintypes.HANDLE

FreeConsole = WinDLL('kernel32.dll').FreeConsole
FreeConsole.argtypes = []
FreeConsole.restype = wintypes.BOOL

WriteConsole = WinDLL('kernel32.dll').WriteConsoleA
WriteConsole.argtypes = [wintypes.HANDLE, wintypes.LPSTR, wintypes.DWORD, wintypes.POINTER(wintypes.DWORD), wintypes.LPVOID]
WriteConsole.restype = wintypes.BOOL

###################################################################################################

class ConsoleObject():
    def __init__(self):
        AttachConsole(-1)
        self.handle = GetStdHandle(0xFFFFFFF5)

    def write(self, data):
        size = wintypes.DWORD()
        size.value = len(data)
        buffer = (wintypes.c_char * size.value)()
        buffer.raw = data
        writen = wintypes.DWORD()
        reserved = wintypes.LPVOID()
        WriteConsole(self.handle, buffer, size, wintypes.pointer(writen), reserved)

    def __del__(self):
        FreeConsole()
        
def execute(callback, *args):
    console = ConsoleObject()
    origin = sys.stdout
    sys.stdout = console
    callback(*args)
    sys.stdout = origin
    idc.Exit(0)