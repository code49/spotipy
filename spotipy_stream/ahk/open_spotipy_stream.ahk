#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

Run, cmd.exe, "c:\Users\David Chan\Desktop\spotipy\spotipy_stream"
WinWait, ahk_exe cmd.exe
Send python main.py {enter}
WinMinimize, A