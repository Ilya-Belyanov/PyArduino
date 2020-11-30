@echo off

set destination_path=%1


IF "%destination_path%"=="" (
   set destination_path=%CD%
)

MD %destination_path%\data

MD %destination_path%\src
MD %destination_path%\src\core
MD %destination_path%\src\obj

MD %destination_path%\gui
MD %destination_path%\gui\ui
MD %destination_path%\gui\windows
MD %destination_path%\gui\widgets

MD %destination_path%\statis
MD %destination_path%\statis\img
MD %destination_path%\statis\language
MD %destination_path%\statis\scripts
MD %destination_path%\statis\style


