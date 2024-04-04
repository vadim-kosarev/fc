@echo off
set d=out2
for /F %%F in ('dir /B %d%\*.jpg') do (
  python FacesImageProcessor.py --file=%d%/%%F
)