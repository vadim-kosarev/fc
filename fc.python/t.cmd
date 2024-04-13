@echo off
set d=out
set suffix=.jpeg --debug=true

for /F %%F in ('dir /B %d%\*.jpg') do (
  python FacesImageProcessor.py --file=%d%/%%F --suffix=%suffix%
)