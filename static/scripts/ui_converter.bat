@echo off
 
set source_path=%1
set destination_path=%2

IF "%source_path%"=="" (
   set source_path=%CD%
)

IF NOT EXIST %source_path% (
   set source_path=%CD%
)

IF "%destination_path%"=="" (
   set destination_path=ui_generated
)

IF NOT EXIST %destination_path% (
   MD %destination_path%
)


FOR /R %source_path% %%f IN (*.ui) DO  (
   pyuic5 %%f -o %destination_path%\%%~nf.py
)