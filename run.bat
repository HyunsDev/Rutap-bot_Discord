@echo off
echo.
echo ==============================
echo Preparing... Please Wait
echo ==============================
title Run Rutap Bot 2019 Main Module
chcp 65001
color 0b
goto main

:main
cls
echo.
echo 1. Module Insatll OR Update
echo 2. Run Rutap Bot 2019
echo 3. Exit
echo.
set /p b=Input a number and press Enter. : 
if %b% == 1 goto Module_Install
if %b% == 2 goto Run
if %b% == 3 goto E-xit

:E-xit
exit

:Module_Install
cls
echo If you have Python 3.6 and you run this file as an administrator, press Enter.
pause
cls
python -m pip install --upgrade pip
python -m pip install discord
python -m pip install requests
python -m pip install datetime
python -m pip install BeautifulSoup4
python -m pip install Pillow
python -m pip install numpy
echo.
echo ==============================
echo Press Enter to return to Main.
echo ==============================
pause
goto main

:Run
cls
echo ==============================
echo Please Wait...
echo ==============================
python rutap.py
echo.
echo ==============================
echo Press Enter to return to Main.
echo ==============================
pause
goto main