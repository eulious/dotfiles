#InstallKeybdHook
#USEHOOK

; CapsLockはレジストリを書き換えて潰す

; 起動時に実行
; Set-Location $HOME\Documents\HOME\Tools\AutoHotkey
; .\AutoHotkeyU64.exe autohotkey.ahk

; 変換、無変換キーでIME切り替え
; https://tex2e.github.io/blog/keyboard/ahk-mac-like-keyboard
vk1C::
imeoff:
  Gosub, IMEGetstate
  If (vimestate=0) {
    Send, {vkf3}
  }
  return
vk1D::
imeon:
  Gosub, IMEGetstate
  If (vimestate=1) {
    Send, {vkf3}
  }
  return
IMEGetstate:
  WinGet, vcurrentwindow, ID, A
  vimestate := DllCall("user32.dll\SendMessageA", "UInt", DllCall("imm32.dll\ImmGetDefaultIMEWnd", "Uint", vcurrentwindow), "UInt", 0x0283, "Int", 0x0005, "Int", 0)
  return

; PowerShellでUNIXのキーバインド
#IfWinActive , ahk_class ConsoleWindowClass
^a::SendInput {HOME}
^e::SendInput {END}
^u::SendInput {ESC}
^p::SendInput {UP}
^n::SendInput {DOWN}
^l::SendInput {ESC}cls{ENTER}
^f::SendInput {right}
^b::SendInput {left}
; ssh中に反応しなくなるので無効
; ^k::SendInput {F4}
#IfWinActive

#USEHOOK off