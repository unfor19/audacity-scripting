
### This script is used to initialize Audacity for the first time on Windows.
# It is used to click through the initial setup wizard

# Example usage:
# powershell -ExecutionPolicy Bypass -File init_audacity.ps1

$wshell = New-Object -ComObject wscript.shell;
Start-Sleep 0.5
$wshell.SendKeys('{TAB}')
Start-Sleep 0.5
$wshell.SendKeys('{TAB}')
Start-Sleep 0.5
$wshell.SendKeys('{TAB}')
Start-Sleep 0.5
$wshell.SendKeys('{TAB}')
Start-Sleep 0.5
$wshell.SendKeys('{ENTER}')

Start-Sleep 0.5
$wshell.SendKeys('{TAB}')
Start-Sleep 0.5
$wshell.SendKeys('{ENTER}')

Start-Sleep 0.5
$wshell.SendKeys('{TAB}')
Start-Sleep 0.5
$wshell.SendKeys('{ENTER}')

