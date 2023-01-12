$ENV:Path="$HOME\Documents\WindowsPowerShell\concfg\bin;"+$ENV:Path

Set-Alias py python
Remove-Item alias:cd

function o() {
    explorer .
}

function so() {
    . $HOME\Documents\WindowsPowerShell\profile.ps1
}

function o($LOCATION = ".") {
    explorer $LOCATION
}

function prompt() {
  ">>> " + (Split-Path (Get-Location) -Leaf) + " $ "
}