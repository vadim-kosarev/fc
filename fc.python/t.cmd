@echo off
set d=out
set suffix=_dnn.300x.jpeg

for /F %%F in ('dir /B %d%\*.jpg') do (
  python FacesImageProcessor.py --file=%d%/%%F --suffix=%suffix%
)